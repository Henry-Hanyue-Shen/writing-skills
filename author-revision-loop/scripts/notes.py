"""Read the author's highlight notes from the reading PDF.

usage: notes.py PDF [--since D:YYYYMMDDHHMMSS] [--exclude-author NAME] [--json OUT.json]

Prints notes front to back (page, then position): time, author, note text, the
exact words under the highlight ("MARKED") and the full line(s) around it.
Also prints `extracted_at D:...` (local time) to record as the cutoff for carry.py,
and a `key` per note (page|y|note prefix) usable in carry.py --keep files.
"""
import argparse, json, sys, time
import fitz


def marked_words(page, annot, words):
    rects = []
    v = annot.vertices
    if v and len(v) >= 4:
        rects = [fitz.Quad(v[i:i + 4]).rect for i in range(0, len(v), 4)]
    else:
        rects = [annot.rect]
    out = []
    for w in words:
        r = fitz.Rect(w[:4])
        c = fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
        if any(q.contains(c) for q in rects):
            out.append(w[4])
    return " ".join(out), rects


def line_text(page, rects):
    if not rects:
        return ""
    y0 = min(r.y0 for r in rects) - 1
    y1 = max(r.y1 for r in rects) + 1
    clip = fitz.Rect(0, y0, page.rect.width, y1)
    return " ".join(page.get_text("text", clip=clip).split())


def note_key(pno, annot):
    return f"{pno + 1}|{round(annot.rect.y0)}|{(annot.info.get('content') or '')[:30]}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--since", default="")
    ap.add_argument("--exclude-author", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    rows = []
    for page in doc:
        words = page.get_text("words")
        for an in page.annots() or []:
            info = an.info
            author = info.get("title", "")
            if author in a.exclude_author:
                continue
            date = (info.get("modDate") or info.get("creationDate") or "")[:16]
            if a.since and date <= a.since[:16]:
                continue
            marked, rects = marked_words(page, an, words)
            rows.append({
                "key": note_key(page.number, an),
                "page": page.number + 1,
                "y": round(an.rect.y0),
                "x": round(an.rect.x0),
                "type": an.type[1],
                "date": date,
                "author": author,
                "note": (info.get("content") or "").strip(),
                "marked": marked,
                "line": line_text(page, rects)[:400],
            })
    rows.sort(key=lambda r: (r["page"], r["y"], r["x"]))
    stamp = time.strftime("D:%Y%m%d%H%M%S")
    print(f"extracted_at {stamp}  notes {len(rows)}  pdf {a.pdf}")
    for i, r in enumerate(rows, 1):
        print(f"\n[{i}] p{r['page']} y{r['y']} {r['date']} {r['author']}")
        print(f"  NOTE:   {r['note']}")
        print(f"  MARKED: {r['marked']}")
        print(f"  LINE:   {r['line']}")
        print(f"  key:    {r['key']}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"extracted_at": stamp, "pdf": a.pdf, "notes": rows}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
