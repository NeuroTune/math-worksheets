# Math Worksheets

A tiny tool for generating printable math practice worksheets — addition,
subtraction, multiplication, division, and one-variable algebra — each with an
answer key. Pick an operation, choose the difficulty, and print or save a PDF.

**▶ Live demo:** https://neurotune.github.io/math-worksheets/

## What it does

- **Five worksheet types:** Addition, Subtraction, Multiplication, Division, Algebra
- **Difficulty by digit count** (1–3 digits); division uses friendlier divisors
- **1–18 questions**, laid out in 1–3 columns automatically
- **Answer key** generated alongside every worksheet (division shows the remainder)
- **Print or download a PDF** — nothing leaves your browser

## Two versions in this repo

| Version | Where | Run it |
| --- | --- | --- |
| **Web** (this demo) | `index.html`, `app.js`, `styles.css` | Open `index.html`, or visit the live demo |
| **Desktop** (original) | [`python/`](python/) | `python python/math_worksheets.py` |

The web app is a faithful browser port of the original Python/Tkinter desktop
tool I wrote in 2022 — same number ranges, the same subtraction swap that keeps
answers non-negative, the same division-with-remainder, and the same algebra
equation generator and solver.

### Running the desktop version

```bash
pip install reportlab
python python/math_worksheets.py
```

It opens a small window; choose your options and it writes a `Math_Practice.pdf`
with the worksheet on page 1 and the answer key on page 2.

## Running the web version locally

No build step. Just serve the folder:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

(Opening `index.html` directly also works; a local server just lets the PDF
library load cleanly.)

## How it works

`app.js` generates the problems and answer key in plain JavaScript, renders the
worksheet as HTML, and produces the PDF client-side with
[jsPDF](https://github.com/parallax/jsPDF). There is no backend — the whole
thing is static files, which is why it hosts for free on GitHub Pages.

## License

MIT — see [LICENSE](LICENSE).
