/* Math Worksheets — browser port of the original Python/tkinter generator.
   Faithfully mirrors the number ranges, subtraction swap, division remainder,
   and the algebra equation generator/solver from python/math_worksheets.py. */

"use strict";

// ── Small helpers ────────────────────────────────────────────────────────────
const randint = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo; // inclusive
const randbool = () => Math.random() < 0.5;
const choice = (arr) => arr[Math.floor(Math.random() * arr.length)];

// randint(10^(d-1), 10^d) — same inclusive range the Python used
const randRange = (d) => randint(Math.pow(10, d - 1), Math.pow(10, d));

// ── Core generation ──────────────────────────────────────────────────────────
// Returns { title, subtitle, problems: [{label, lines}], answers: [str] }
function buildWorksheet(operation, digits, questions) {
  const problems = [];
  const answers = [];
  let title = operation;
  let subtitle = "";

  if (operation === "Algebra") {
    title = "Algebra";
    for (let i = 0; i < questions; i++) {
      const { text, answer } = makeAlgebra();
      problems.push({ label: `${i + 1})`, lines: [text], algebra: true });
      answers.push(`${i + 1}) ${answer}`);
    }
    return { title, subtitle, problems, answers };
  }

  const d = parseInt(digits, 10);
  subtitle = { 1: "One Digit", 2: "Two Digits", 3: "Three Digits" }[d] || "";

  for (let i = 0; i < questions; i++) {
    let a, b;
    if (operation === "Division") {
      a = randRange(d);
      b = d <= 2 ? randint(1, 10) : randint(1, 50);
    } else {
      a = randRange(d);
      b = randRange(d);
    }

    if (operation === "Subtraction" && a < b) {
      [a, b] = [b, a]; // keep the answer non-negative
    }

    let sign, answer;
    switch (operation) {
      case "Addition":       sign = "+"; answer = a + b; break;
      case "Subtraction":    sign = "−"; answer = a - b; break; // − minus sign
      case "Multiplication": sign = "×"; answer = a * b; break; // × times sign
      case "Division":       sign = "÷"; answer = null; break;
    }

    if (operation === "Division") {
      const q = Math.floor(a / b);
      const r = a % b;
      problems.push({ label: `${i + 1})`, lines: [`${b} ÷ ${a}`], division: true, a, b });
      answers.push(`${i + 1}) ${q}; R: ${r}`);
    } else {
      problems.push({ label: `${i + 1})`, a, b, sign });
      answers.push(`${i + 1}) ${answer}`);
    }
  }
  return { title, subtitle, problems, answers };
}

// Algebra: ax (+/- b) = (cx) +/- d  → solve for x. Mirrors the Python branch.
function makeAlgebra() {
  const coeffs = [-5, -4, -3, -2, -1, 1, 2, 4, 5];

  let x1Val = choice(coeffs);

  const num1 = randbool();
  let num1ValPos = false, num1Val = 0;
  if (num1) { num1ValPos = randbool(); num1Val = randint(1, 21); }

  const x2 = randbool();
  let x2Val = 0;
  if (x2) { x2Val = choice(coeffs); }

  const num2ValPos = randbool();
  const num2Val = randint(1, 21);

  // Build the printed equation
  let eq = `${x1Val}x `;
  if (num1) eq += (num1ValPos ? "+ " : "- ") + `${num1Val} `;
  eq += "= ";
  if (x2) eq += `${x2Val}x `;
  eq += (num2ValPos ? "+ " : "- ") + `${num2Val}`;

  // Solve
  let num2TrueVal = num2ValPos ? num2Val : -num2Val;
  if (x2) x1Val += -x2Val;
  if (num1) num2TrueVal += num1ValPos ? -num1Val : num1Val;

  let answer;
  if (x1Val !== 0) {
    answer = String(Math.round((num2TrueVal / x1Val) * 100) / 100);
  } else if (num2TrueVal === 0) {
    answer = "All Real Numbers";
  } else {
    answer = "No Solution";
  }
  return { text: eq, answer };
}

// ── Rendering to the on-screen preview ───────────────────────────────────────
function columnsFor(questions) {
  if (questions > 12) return 3;
  if (questions > 6) return 2;
  return 1;
}

function renderPreview(sheet, questions) {
  const worksheet = document.getElementById("worksheet");
  const cols = columnsFor(questions);
  worksheet.style.setProperty("--cols", cols);

  const heading = sheet.subtitle
    ? `${sheet.title} <span class="subtitle">/ ${sheet.subtitle}</span>`
    : sheet.title;
  document.getElementById("sheet-title").innerHTML = heading;

  const grid = document.getElementById("problem-grid");
  grid.innerHTML = "";
  for (const p of sheet.problems) {
    const cell = document.createElement("div");
    cell.className = "problem";

    if (p.algebra) {
      cell.innerHTML = `<span class="pnum">${p.label}</span><span class="algebra">${p.lines[0]}</span>`;
    } else if (p.division) {
      cell.innerHTML =
        `<span class="pnum">${p.label}</span>` +
        `<span class="division"><span class="divisor">${p.b}</span>` +
        `<span class="dividend">${p.a}</span></span>`;
    } else {
      cell.innerHTML =
        `<span class="pnum">${p.label}</span>` +
        `<span class="stack">` +
        `<span class="operand">${p.a}</span>` +
        `<span class="operand"><span class="op">${p.sign}</span>${p.b}</span>` +
        `<span class="rule"></span>` +
        `</span>`;
    }
    grid.appendChild(cell);
  }

  const answers = document.getElementById("answer-list");
  answers.innerHTML = "";
  for (const a of sheet.answers) {
    const li = document.createElement("li");
    li.textContent = a;
    answers.appendChild(li);
  }

  document.getElementById("output").hidden = false;
}

// ── PDF (jsPDF) — mirrors the two-page layout of the Python reportlab code ────
function downloadPDF(sheet, questions) {
  if (!window.jspdf || !window.jspdf.jsPDF) {
    alert("PDF library did not load (offline?). Use “Print / Save as PDF” instead.");
    return;
  }
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: "pt", format: "letter" }); // 612 x 792 pt
  const pageW = doc.internal.pageSize.getWidth();

  doc.setFont("helvetica", "bold").setFontSize(16);
  doc.text("MATH WORKSHEETS", pageW / 2, 52, { align: "center" });
  const heading = sheet.subtitle ? `${sheet.title} / ${sheet.subtitle}` : sheet.title;
  doc.text(heading, pageW / 2, 72, { align: "center" });
  doc.setLineWidth(1).line(100, 92, 512, 92);

  const cols = columnsFor(questions);
  const rows = Math.ceil(questions / cols);
  const colW = (pageW - 100) / cols;
  const topY = 130;
  const rowH = Math.min(90, (720 - topY) / rows);

  doc.setFont("helvetica", "normal").setFontSize(14);
  sheet.problems.forEach((p, i) => {
    const x = 60 + (i % cols) * colW;
    const y = topY + Math.floor(i / cols) * rowH;

    if (p.algebra) {
      doc.text(`${p.label}  ${p.lines[0]}`, x, y);
    } else if (p.division) {
      doc.text(p.label, x, y);
      doc.text(String(p.b), x + 55, y + 4, { align: "right" });
      doc.text(String(p.a), x + 62, y + 4);
      doc.line(x + 58, y - 10, x + 110, y - 10);
      doc.line(x + 58, y - 10, x + 58, y + 8);
    } else {
      doc.text(p.label, x, y);
      doc.text(String(p.a), x + 98, y, { align: "right" });
      doc.text(p.sign, x + 40, y + 18);
      doc.text(String(p.b), x + 98, y + 18, { align: "right" });
      doc.line(x + 30, y + 24, x + 100, y + 24);
    }
  });

  // Answer key on page 2
  doc.addPage();
  doc.setFont("helvetica", "bold").setFontSize(14);
  doc.text("Answer Key", pageW / 2, 52, { align: "center" });
  doc.setFont("helvetica", "normal").setFontSize(11);
  sheet.answers.forEach((a, i) => {
    const perCol = 20;
    const col = Math.floor(i / perCol);
    const row = i % perCol;
    doc.text(a, 60 + col * 160, 90 + row * 30);
  });

  doc.save("Math_Practice.pdf");
}

// ── Wire up the UI ───────────────────────────────────────────────────────────
let currentSheet = null;
let currentQuestions = 0;

document.addEventListener("DOMContentLoaded", () => {
  const opSel = document.getElementById("operation");
  const digSel = document.getElementById("digits");
  const qSel = document.getElementById("questions");
  const status = document.getElementById("status");

  // Populate the questions dropdown 1..18
  for (let n = 1; n <= 18; n++) {
    const o = document.createElement("option");
    o.value = String(n);
    o.textContent = String(n);
    qSel.appendChild(o);
  }

  // Disable digits when Algebra is chosen
  opSel.addEventListener("change", () => {
    const isAlg = opSel.value === "Algebra";
    digSel.disabled = isAlg;
    digSel.parentElement.classList.toggle("disabled", isAlg);
  });

  function generate() {
    const operation = opSel.value;
    const digits = digSel.value;
    const questions = parseInt(qSel.value, 10);

    if (!operation) { status.textContent = "Pick an operation first."; return; }
    if (operation !== "Algebra" && !digits) { status.textContent = "Pick the number of digits."; return; }
    if (!questions) { status.textContent = "Pick how many questions."; return; }

    status.textContent = "";
    currentSheet = buildWorksheet(operation, digits, questions);
    currentQuestions = questions;
    renderPreview(currentSheet, questions);
  }

  document.getElementById("generate").addEventListener("click", generate);
  document.getElementById("download").addEventListener("click", () => {
    if (currentSheet) downloadPDF(currentSheet, currentQuestions);
  });
  document.getElementById("print").addEventListener("click", () => window.print());
});
