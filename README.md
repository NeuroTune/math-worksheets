# Math Worksheets (2023)

A tool for generating endless math practice worksheets (addition,
subtraction, multiplication, division, and one-variable algebra) with an
answer key. Pick an operation, choose the difficulty, and print or save a PDF.


**▶ Live demo:** https://neurotune.github.io/math-worksheets/

js code was created with the help of claude code from the original project (2023). 

## What it does

- **Five worksheet types:** Addition, Subtraction, Multiplication, Division, Algebra
- **Difficulty by digit count**; 1-3 digits
- **1–18 questions**, laid out in 1–3 columns
- **Answer key** generated with every worksheet (division shows the remainder)
- **Download a PDF** to hand out endless worksheets to students

## Two versions in this repo

| Version | Where | Run it |
| --- | --- | --- |
| **Live Demo**  | `index.html`, `app.js`, `styles.css` | Open `index.html`, or visit the live demo |
| **Desktop** (original code) | [`python/math_worksheets.py`](python/math_worksheets.py) | `python python/math_worksheets.py` |

The web app is a faithful browser port of the original Python/Tkinter desktop
tool — same number ranges, the same subtraction swap that keeps answers
non-negative, the same division-with-remainder, and the same algebra equation
generator and solver.

### Running the desktop version

```bash
pip install reportlab
python python/math_worksheets.py
```

It opens a small window; choose your options and it writes a `Math_Practice.pdf`
with the worksheet on page 1 and the answer key on page 2.


## License

MIT — see [LICENSE](LICENSE).
