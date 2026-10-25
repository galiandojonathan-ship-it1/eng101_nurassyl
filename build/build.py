"""Build the ENG 101 study site.

Runs every trace drill to confirm its expected output, then writes
../index.html (a standalone page) with all content embedded as JSON.

Usage: python3 build/build.py [--artifact PATH]
  --artifact PATH  also write a copy without the <!doctype> wrapper,
                   for publishing as a claude.ai artifact.
"""
import contextlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from content_drills import DRILLS  # noqa: E402
from content_quiz import QUIZ  # noqa: E402
from content_ref import CARDS, CHECKLIST, SHEET  # noqa: E402
from content_weeks import WEEKS  # noqa: E402


def check_drills():
    failures = []
    for drill in DRILLS:
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                exec(drill["code"], {})
        except Exception as error:  # report, don't hide
            failures.append(f"{drill['title']}: raised {error!r}")
            continue
        got = buffer.getvalue().rstrip("\n")
        if got != drill["out"]:
            failures.append(f"{drill['title']}: expected {drill['out']!r}, got {got!r}")
    return failures


def check_quiz():
    week_ids = {w["id"] for w in WEEKS}
    problems = []
    for q in QUIZ:
        if not 0 <= q["a"] < len(q["o"]):
            problems.append(f"bad answer index: {q['q']}")
        if q["week"] not in week_ids:
            problems.append(f"unknown week {q['week']}: {q['q']}")
    return problems


def main():
    problems = check_drills() + check_quiz()
    if problems:
        print("\n".join(problems))
        sys.exit(1)

    data = {
        "weeks": WEEKS,
        "drills": DRILLS,
        "quiz": QUIZ,
        "cards": [{"week": w, "term": t, "def": d} for w, t, d in CARDS],
        "sheet": SHEET,
        "checklist": CHECKLIST,
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
        body = f.read().replace("/*DATA*/", payload)

    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>html{color-scheme:light dark}body{margin:0}[hidden]{display:none!important}'
            'img{max-width:100%}</style>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
    out_path = os.path.join(HERE, "..", "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)

    if "--artifact" in sys.argv:
        artifact_path = sys.argv[sys.argv.index("--artifact") + 1]
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(body)

    print(f"{len(DRILLS)} drills verified, {len(QUIZ)} quiz questions, "
          f"{len(CARDS)} cards. Wrote index.html")


if __name__ == "__main__":
    main()
