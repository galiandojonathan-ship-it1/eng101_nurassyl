# ENG 101 Final Prep

A study website for ENG 101 (Programming for Engineers), built from the Week 7 and Week 9–14 Detailed Reading Notes. Week 14 reviews Weeks 1–6, so those foundations are included.

Open `index.html` in any browser. It works offline as a single file.

## What's inside

- **Weeks**: key ideas, common mistakes and explain-it questions with answers for each week.
- **Trace drills**: 57 predict-the-output Python snippets. Every expected output is checked by running the code during the build.
- **Quiz**: 65 multiple-choice questions with explanations, by week or mixed.
- **Flashcards**: 70 glossary terms.
- **Cheat sheet**: operators, list/dict operations, exceptions, growth classes, counting rules, search/sort costs and a cross-language table.

Progress (drills, cards, checklist, best quiz score) is saved in your browser only.

## Editing

Content lives in `build/content_*.py`; layout in `build/template.html`. Rebuild with:

```
python3 build/build.py
```

The build fails if any drill's expected output doesn't match what Python prints.
