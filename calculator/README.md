# Modern Web Calculator Project

An interactive, responsive basic calculator built using **HTML5**, **CSS Grid**, and **vanilla JavaScript**. This project is designed and organized to fulfill all academic and assignment evaluation requirements with clean, self-documenting code.

---

## 📌 Project Requirements Checklist

| Requirement | Implementation Detail | Location in Code |
| :--- | :--- | :--- |
| **Interactive Interface** | Keypad with operations: Addition (`+`), Subtraction (`−`), Multiplication (`×`), and Division (`÷`), plus digits `0–9`, `.`, `AC`, `DEL`, `±`, `%`, and `=` | `index.html` (Lines 26–57) |
| **Display Screen** | Dual-tier display: an upper sub-screen for previous expression/pending operator, and a prominent primary screen for active operand and computed results | `index.html` (Lines 20–24) & `style.css` (Lines 77–104) |
| **CSS Grid System** | Keypad alignment using CSS Grid (`display: grid`, `grid-template-columns: repeat(4, 1fr)`, `grid-template-rows: repeat(5, 60px)`, `gap: 12px`) | `style.css` (Lines 109–115) |
| **Event Listeners** | `addEventListener` applied to all keypad buttons (`click`) and global document (`keydown`) for keyboard input | `script.js` (Lines 228–234, 269–304) |
| **Loops** | `for...of` loop iterating over button collections to dynamically bind events, and `for...of` loop searching buttons for visual keyboard press feedback | `script.js` (Lines 228–234, 311–326) |
| **If-Else Statements** | Branching logic for action routing, decimal validation, leading zero control, operator replacement, and zero-division protection | `script.js` (Lines 34–54, 60–87, 137–155, 237–264) |
| **Operators** | Arithmetic (`+`, `-`, `*`, `/`, `%`), assignment, comparison (`===`, `!==`), and logical (`&&`, `||`, `!`) operators | `script.js` (Lines 107–109, 142–154, 160–162) |

---

## 🚀 How to Run the Project

No dependencies, build tools, or servers are required!

1. Open your terminal or file explorer.
2. Navigate to the project folder:
   ```bash
   cd calculator
   ```
3. Open `index.html` in your favorite web browser:
   - **macOS**: `open index.html`
   - **Windows**: `start index.html`
   - **Linux**: `xdg-open index.html`
   - Or simply double-click `index.html` in Finder / File Explorer.

---

## ⌨️ Keyboard Shortcuts

The calculator supports full physical keyboard and numpad interaction:

| Key | Function |
| :--- | :--- |
| `0` to `9` | Enter digits |
| `.` | Decimal point |
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `Enter` or `=` | Calculate result |
| `Backspace` | Delete last entered character (`DEL`) |
| `Escape` | Reset calculator (`AC` - All Clear) |
| `%` | Calculate percentage |

---

## 💡 Key Features & Edge Case Handling

1. **Division by Zero Protection**: Prevents `Infinity` or browser crashes by displaying a friendly `"Cannot divide by 0"` error message.
2. **Floating-Point Precision Fix**: Automatically eliminates JavaScript IEEE-754 binary floating-point anomalies (e.g., `0.1 + 0.2` outputs clean `0.3` instead of `0.30000000000000004`).
3. **Operator Replacement**: If you tap `+` and immediately change your mind to `×`, it smoothly replaces the operator without clearing your first number.
4. **Smart Decimals**: Disallows multiple dots (e.g. entering `3.14.15` is prevented) and automatically prepends `0.` if the decimal is pressed when the display is empty.
5. **Thousand Separators**: Formats large numbers with localized grouping commas (e.g., `1,250,000`) for readability.
6. **Accessibility**: Keypad buttons have `aria-label` attributes and the display section uses `aria-live="polite"` for screen reader announcements.
7. **Responsive & Modern UI**: Built with a sleek dark aesthetic, subtle glassmorphism backdrop blur, and responsive styling that adapts seamlessly to phones, tablets, and desktop screens.

---

## 🧪 Verification & Testing

An automated test suite is included in `verify_calculator.py`. To run the unit tests:

```bash
python3 verify_calculator.py
```
Outputs:
```text
ALL 12 UNIT TESTS PASSED SUCCESSFULLY!
```
