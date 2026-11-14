"""Put away-mode (proxy author) notes into the reading PDF as highlights.

usage: proxy_annotate.py PDF NOTES.json [--out OUT.pdf]

NOTES.json:
{"author": "Claude (as author)",
 "notes": [{"id": "T3", "type": "FIX|CUT|QUESTION", "status": "applied|held|rejected",
            "anchor": "words as they appear in the NEW pdf", "page": 6,   # page optional
            "note": "<= 15 words, author's voice"}]}

Colours: applied = blue, held = orange, rejected = grey. Each highlight's note reads
"[applied CUT T3] rm clause: repeats Eq. (3)". If the anchor is not found, shorter
prefixes are tried; failing that, a sticky note is put at the top of the given page
(or page 1) and the note is listed as UNANCHORED. Existing proxy marks by the same
author are removed first, so re-running replaces them. The author's own marks are kept.
"""
import argparse, json, os, shutil, sys, tempfile
import fitz

COLORS = {"applied": (0.55, 0.75, 1.0), "held": (1.0, 0.7, 0.3), "rejected": (0.75, 0.75, 0.75)}


def find(doc, anchor, page_hint):
    words = anchor.split()
    pages = list(range(len(doc)))
    if page_hint and 1 <= page_hint <= len(doc):
        pages.remove(page_hint - 1)
        pages.insert(0, page_hint - 1)
    for k in sorted({len(words), 8, 5, 3}, reverse=True):
        if k < 1 or k > len(words):
            continue
        probe = " ".join(words[:k])
        for pno in pages:
            hits = doc[pno].search_for(probe, quads=True)
            if hits:
                # one quad per line piece, for every occurrence: keep the first
                # occurrence, i.e. following quads that wrap onto the next line
                run = [hits[0]]
                for q in hits[1:]:
                    prev = run[-1].rect
                    h = prev.height or 10
                    if 0 < q.rect.y0 - prev.y0 < 1.8 * h and q.rect.x0 < prev.x0:
                        run.append(q)
                    else:
                        break
                return pno, run, probe
    return None, None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("notes"); ap.add_argument("--out")
    a = ap.parse_args()
    spec = json.load(open(a.notes, encoding="utf-8"))
    author = spec.get("author", "Claude (as author)")
    doc = fitz.open(a.pdf)
    for page in doc:  # drop earlier proxy marks
        for an in list(page.annots() or []):
            if an.info.get("title") == author:
                page.delete_annot(an)
    placed, loose = 0, []
    for n in spec["notes"]:
        status = n.get("status", "applied")
        text = f"[{status} {n.get('type', '')} {n.get('id', '')}] {n.get('note', '')}".strip()
        pno, quads, probe = find(doc, n.get("anchor", ""), n.get("page"))
        if pno is None:
            page = doc[(n.get("page") or 1) - 1]  # keep the page object alive while annotating
            an = page.add_text_annot(fitz.Point(20, 20 + 14 * len(loose)), "[unanchored] " + text)
            loose.append(n.get("id"))
        else:
            page = doc[pno]
            an = page.add_highlight_annot(quads)
            if probe != n.get("anchor"):
                text += f"  (anchored on: {probe})"
            placed += 1
        an.set_info(title=author, content=text)
        an.set_colors(stroke=COLORS.get(status, COLORS["applied"]))
        an.update()
    out = a.out or a.pdf
    fd, tmp = tempfile.mkstemp(suffix=".pdf"); os.close(fd)
    doc.save(tmp); doc.close()
    shutil.move(tmp, out)
    print(f"placed {placed}, unanchored {len(loose)} {loose} -> {out}")


if __name__ == "__main__":
    sys.exit(main())
