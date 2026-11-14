"""Carry the author's unhandled marks from the old annotated PDF onto a new build.

usage: carry.py OLD_ANNOTATED.pdf NEW_BUILD.pdf OUT.pdf --cutoff D:YYYYMMDDHHMMSS
                [--keep KEYS.txt] [--exclude-author "Claude (as author)"]

Copied: author marks changed after --cutoff (made while the batch was being fixed),
plus marks whose key (from notes.py) is listed in --keep (held for discussion).
Not copied: everything else (handled) and proxy marks (--exclude-author).
Marks are placed at the same page and position; text may have moved, so the
summary lists each copied mark for a visual check. OUT may equal the reading PDF
(write is done via a temporary file).
"""
import argparse, os, shutil, sys, tempfile
import fitz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old"); ap.add_argument("new"); ap.add_argument("out")
    ap.add_argument("--cutoff", required=True)
    ap.add_argument("--keep")
    ap.add_argument("--exclude-author", action="append", default=["Claude (as author)"])
    a = ap.parse_args()
    keep = set()
    if a.keep and os.path.exists(a.keep):
        keep = {l.strip() for l in open(a.keep, encoding="utf-8") if l.strip()}
    src, dst = fitz.open(a.old), fitz.open(a.new)
    n = 0
    for pno, page in enumerate(src):
        for an in page.annots() or []:
            info = an.info
            if info.get("title", "") in a.exclude_author:
                continue
            date = (info.get("modDate") or info.get("creationDate") or "")[:16]
            key = f"{pno + 1}|{round(an.rect.y0)}|{(info.get('content') or '')[:30]}"
            if date <= a.cutoff[:16] and key not in keep:
                continue
            if pno >= len(dst):
                print(f"SKIPPED (page {pno + 1} no longer exists): {info.get('content', '')[:80]}")
                continue
            p = dst[pno]
            t = an.type[0]
            if t == fitz.PDF_ANNOT_HIGHLIGHT and an.vertices:
                quads = [fitz.Quad(an.vertices[i:i + 4]) for i in range(0, len(an.vertices), 4)]
                na = p.add_highlight_annot(quads)
            elif t == fitz.PDF_ANNOT_INK:
                na = p.add_ink_annot(an.vertices)
            elif t == fitz.PDF_ANNOT_TEXT:
                na = p.add_text_annot(an.rect.tl, info.get("content", ""))
            else:
                na = p.add_rect_annot(an.rect)
            na.set_info(content=info.get("content", ""), title=info.get("title", ""),
                        modDate=info.get("modDate", ""), creationDate=info.get("creationDate", ""))
            if an.colors.get("stroke"):
                na.set_colors(stroke=an.colors["stroke"])
            na.update()
            n += 1
            why = "held" if key in keep else "new"
            print(f"carried ({why}) p{pno + 1} y{round(an.rect.y0)}: {info.get('content', '')[:80]}")
    fd, tmp = tempfile.mkstemp(suffix=".pdf"); os.close(fd)
    dst.save(tmp); dst.close(); src.close()
    shutil.move(tmp, a.out)
    print(f"carried {n} -> {a.out}")


if __name__ == "__main__":
    sys.exit(main())
