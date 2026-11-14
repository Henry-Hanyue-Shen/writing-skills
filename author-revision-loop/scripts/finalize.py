"""Make a clean source copy for submission: drop deletions, unwrap red.

usage: finalize.py IN.tex OUT.tex [--unwrap rn,rev] [--drop rdel,rdelnote]

Removes \\rdel{...} and \\rdelnote{...} (balanced braces) and the commented
RDEL-BEGIN/RDEL-END blocks; replaces \\rn{X} and \\rev{X} by X. Never overwrites IN.
Simpler alternative for a black PDF: \\markupfalse in the preamble.
"""
import argparse, re, sys


def strip_macro(src, name, keep_arg):
    out, i, pat = [], 0, re.compile(r"\\" + name + r"\s*\{")
    while True:
        m = pat.search(src, i)
        if not m:
            out.append(src[i:]); break
        out.append(src[i:m.start()])
        j, depth = m.end(), 1
        while j < len(src) and depth:
            c = src[j]
            if c == "\\":
                j += 2; continue
            depth += (c == "{") - (c == "}")
            j += 1
        if depth:
            raise SystemExit(f"unbalanced \\{name} at offset {m.start()}")
        if keep_arg:
            out.append(strip_macro(src[m.end():j - 1], name, keep_arg))
        i = j
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--unwrap", default="rn,rev")
    ap.add_argument("--drop", default="rdel,rdelnote")
    a = ap.parse_args()
    if a.inp == a.out:
        raise SystemExit("OUT must differ from IN")
    s = open(a.inp, encoding="utf-8").read()
    s = re.sub(r"^[ \t]*% RDEL-BEGIN.*?^[ \t]*% RDEL-END[^\n]*\n?", "", s, flags=re.S | re.M)
    for name in filter(None, a.drop.split(",")):
        s = strip_macro(s, name, keep_arg=False)
    for name in filter(None, a.unwrap.split(",")):
        s = strip_macro(s, name, keep_arg=True)
    open(a.out, "w", encoding="utf-8").write(s)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    sys.exit(main())
