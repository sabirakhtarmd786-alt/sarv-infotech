# Sarv-Infotech — Engineering Platform & Integrated Web Tools

A multi-project repository developed by **Md Sabir Akhtar** featuring an interactive developer blogging platform with categorized engineering sections, user authentication, and an integrated **Modern Web Calculator**.

---

## 📂 Repository Structure

The repository is modularly organized into two distinct project folders, alongside a unified launcher:

```text
sarv-infotech/
├── README.md                      # Monorepo Hub README
├── server.py                      # Root unified launcher serving both projects
├── requirements.txt               # Dependencies
├── Procfile                       # Render.com deployment entrypoint
├── render.yaml                    # Cloud blueprint
│
├── calculator/                    # 🧮 Standalone Web Calculator
│   ├── index.html                 # Calculator UI
│   ├── style.css                  # CSS Grid styles & dark theme
│   ├── script.js                  # Math engine & keyboard navigation
│   ├── verify_calculator.py       # Automated unit test suite (12/12 passed)
│   └── README.md                  # Calculator documentation & requirements checklist
│
└── techblog/                      # 📝 Standalone TechBlog Platform
    ├── server.py                  # Python HTTP & REST API server
    ├── database.py                # SQLite database model & migrations
    ├── test_blog.py               # Blog unit test suite (10/10 passed)
    ├── README.md                  # TechBlog documentation & API routes
    └── static/                    # Frontend assets
        ├── index.html             # Blog feed & navigation
        ├── auth.html              # Login & registration modal
        ├── create-post.html       # Post editor & category selector
        ├── profile.html           # User profile & my-posts view
        ├── style.css              # Responsive styles
        ├── app.js                 # Dynamic UI logic
        └── assets/                # SVG category banners
```

---

## 📌 Projects Overview

### 1. 📝 TechBlog Platform ([`techblog/`](./techblog))
* **Categorized Sections**: **Software**, **Hardware & IoT** (merged), **Internship**, **Jobs**, and **General**.
* **Visual Post Banners**: Pre-bundled vector SVG illustrations for all technical domains.
* **Interactive Engagement**: Real-time Like/Heart counter (`❤️`), 1-click link sharing (`🔗`), and calculated reading time estimates.
* **Full-Text Live Search**: Real-time search bar with 300ms debouncing filtering across titles, content, and categories.
* **User Authentication**: Secure registration and login with salted **PBKDF2-SHA256** password hashing and session tokens.
* **Commenting System**: Nested article discussion threads for authenticated users.

### 2. 🧮 Interactive Web Calculator ([`calculator/`](./calculator))
* **Keypad Alignment**: Built strictly using the **CSS Grid system** (`display: grid; grid-template-columns: repeat(4, 1fr)`).
* **Dual-Line Display Screen**: Upper sub-display for previous operations/expression history, lower primary display for active input & computed results.
* **Defensive Arithmetic Engine**: Safe division-by-zero protection (`"Cannot divide by 0"`), floating-point precision correction (e.g. `0.1 + 0.2 = 0.3`), and seamless operator replacement.
* **Full Keyboard Navigation**: Supports physical keyboard input (Numpad, Enter, Backspace, Esc, %, .).

---

## 🚀 How to Run

### Option A: Run Both Projects Together (Unified Hub)
From the repository root:
```bash
python3 server.py --port 8080
```
* **TechBlog Platform**: [http://localhost:8080](http://localhost:8080)
* **Web Calculator**: [http://localhost:8080/calculator](http://localhost:8080/calculator)

### Option B: Run TechBlog Standalone
```bash
cd techblog
python3 server.py --port 8080
```
* Access at [http://localhost:8080](http://localhost:8080)

### Option C: Run Calculator Standalone
No server needed! Simply open `calculator/index.html` in your browser:
```bash
cd calculator
open index.html        # macOS
start index.html       # Windows
xdg-open index.html    # Linux
```
Or start a simple local server:
```bash
python3 -m http.server 3000
```

---

## 🧪 Automated Testing

Both projects include comprehensive, automated test suites:

### 1. TechBlog Tests (10/10 Passed)
```bash
cd techblog
python3 test_blog.py
```
Output:
```text
Ran 10 tests in 0.088s
OK
```

### 2. Calculator Tests (12/12 Passed)
```bash
cd calculator
python3 verify_calculator.py
```
Output:
```text
ALL 12 UNIT TESTS PASSED SUCCESSFULLY!
```

---

## 🌐 Free Cloud Deployment (Render.com)

1. Connect your GitHub repository **`sabirakhtarmd786-alt/sarv-infotech`** on [Render.com](https://render.com).
2. Configure:
   - **Runtime**: `Python`
   - **Start Command**: `python server.py --port $PORT`
   - **Plan**: `Free`
3. Your platform will be live with both TechBlog and Calculator fully operational!

---

## 👨‍💻 Developer Profile

- **Developer**: Md Sabir Akhtar
- **Institution**: Bakhtiyarpur College of Engineering, Patna
- **Specialization**: Computer Science & Engineering (Internet of Things)
- **GitHub**: [github.com/sabirakhtarmd786-alt](https://github.com/sabirakhtarmd786-alt)
- **LinkedIn**: [linkedin.com/in/md-sabir-akhtar-87a525351](https://www.linkedin.com/in/md-sabir-akhtar-87a525351)
- **Email**: [sabirakhtarmd786@gmail.com](mailto:sabirakhtarmd786@gmail.com)
