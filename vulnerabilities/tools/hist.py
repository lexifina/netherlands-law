"""Hand-check helper: an act file's full history across the 13 November 2026 folder move.
index/changes already maps old folders to new ones (map_moved.py), so one query gives every version.
  python -X utf8 hist.py <path> [--show N|all] [--diff]
  python -X utf8 hist.py --commit <sha>      (subject, trailers, files)
  python -X utf8 hist.py --grep <regex> <path-prefix>   (text at the pin)"""
import sys, os, json, subprocess, re, difflib
import duckdb

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gl", "vulnerabilities", "scripts")
GIT = os.path.join(S, "sources", "corpus", "netherlands-law.git")
CH = os.path.join(S, "index", "changes", "netherlands-law.parquet").replace("\\", "/")
CM = os.path.join(S, "index", "commits", "netherlands-law.parquet").replace("\\", "/")
PIN = "d13d9e1e39eb0153f8dda04ca291bf6ecae8558b"


def blob(b):
    if not b or set(b) == {"0"}:
        return ""
    return subprocess.run(["git", "cat-file", "blob", b], cwd=GIT, capture_output=True).stdout.decode("utf-8", "replace")


def rows(path):
    return duckdb.sql(f"""select c.commit, c.status, c.old_blob, c.new_blob, c.old_path, m.subject, m.trailers
        from '{CH}' c left join '{CM}' m using (commit) where c.path = ? or c.old_path = ?
        order by c.author_date""", params=[path, path]).fetchall()


a = sys.argv[1:]
if a and a[0] == "--commit":
    r = duckdb.sql(f"select author_date, subject, trailers from '{CM}' where commit like ?", params=[a[1] + "%"]).fetchall()
    for x in r:
        print(x[0], x[1]); print(x[2])
    f = duckdb.sql(f"select status, path from '{CH}' where commit like ?", params=[a[1] + "%"]).fetchall()
    print(len(f), "files"); [print(" ", s, p) for s, p in f[:60]]
    raise SystemExit
if a and a[0] == "--grep":
    out = subprocess.run(["git", "grep", "-n", "-E", a[1], PIN, "--", a[2]], cwd=GIT, capture_output=True)
    print(out.stdout.decode("utf-8", "replace")[:20000]); raise SystemExit
path = a[0]
R = rows(path)
show = a[a.index("--show") + 1] if "--show" in a else None
prev = ""
for i, (c, st, ob, nb, op, subj, tr) in enumerate(R):
    t = json.loads(tr or "{}")
    print(f"[{i}] {c[:10]} {st} {t.get('In-force', '')} | {subj[:150]}" + (f" (from {op})" if op != path else ""))
    txt = blob(nb)
    if "--diff" in a:
        for l in difflib.unified_diff(prev.splitlines(), txt.splitlines(), lineterm="", n=0):
            if not l.startswith(("---", "+++", "@@")):
                print("    " + l[:400])
    if show == "all" or show == str(i):
        print(txt)
    prev = txt
