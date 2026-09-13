# Sarv-Infotech — Engineering Platform & Integrated Web Tools

A full-stack web application developed by **Md Sabir Akhtar** featuring an interactive developer blogging platform with categorized engineering sections, user authentication, and an integrated **Modern Web Calculator**.

---

## 📌 Features & Architecture

### 1. Developer Blog & Knowledge Hub
* **Categorized Sections**: Organized topics covering **Software**, **Hardware & IoT** (merged), **Internship**, **Jobs**, and **General**.
* **Visual Post Banners**: Vector SVG banners pre-bundled for all technical categories.
* **Interactive Engagement**: Real-time Like/Heart counter (`❤️`), 1-click link sharing (`🔗`), and calculated reading time estimates.
* **Full-Text Live Search**: Real-time search bar with 300ms debouncing filtering across titles, content, and categories.
* **User Authentication**: Secure registration and login with salted **PBKDF2-SHA256** password hashing and session tokens.
* **Commenting System**: Nested article discussion threads for authenticated users.

### 2. Integrated Modern Web Calculator (`/calculator`)
* **Keypad Alignment**: Built strictly using the **CSS Grid system** (`display: grid; grid-template-columns: repeat(4, 1fr)`).
* **Dual-Line Display Screen**: Upper sub-display for previous operations/expression history, lower primary display for active input & computed results.
* **Defensive Arithmetic Engine**: Safe division-by-zero protection (`"Cannot divide by 0"`), floating-point precision correction (e.g. `0.1 + 0.2 = 0.3`), and seamless operator replacement.
* **Full Keyboard Navigation**: Supports physical keyboard input (Numpad, Enter, Backspace, Esc, %, .).

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.8+ installed (zero external `pip` dependencies required!).

### 2. Start the Server
```bash
cd sarv-infotech
python3 server.py --port 8080
```

### 3. Open in Browser
* **Main Platform (Blog Hub)**: **[http://localhost:8080](http://localhost:8080)**
* **Web Calculator**: **[http://localhost:8080/calculator](http://localhost:8080/calculator)**

> **Default Seeded Account**:
> - **Username**: `sabir_akhtar`
> - **Password**: `demo1234`
> - *(Or click "Register" on the site to create your own account instantly!)*

---

## 🌐 Deploying Free to Cloud (Render.com)

1. **Push your code to GitHub**:
   ```bash
   git remote add origin https://github.com/sabirakhtarmd786-alt/sarv-infotech.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Sign up at [https://render.com](https://render.com) (free).
   - Click **"New +"** → **"Web Service"**.
   - Connect your GitHub repository `sabirakhtarmd786-alt/sarv-infotech`.
   - Settings:
     - **Name**: `sarv-infotech`
     - **Runtime**: `Python`
     - **Start Command**: `python server.py --port $PORT`
     - **Plan**: `Free`
   - Click **"Create Web Service"**.
3. Your platform will be live at: `https://sarv-infotech.onrender.com`!

---

## 🧪 Automated Testing

Run the included unit test suite:

```bash
python3 test_blog.py
```
Output:
```text
..........
Ran 10 tests in 0.088s
OK
```

---

## 👨‍💻 Developer Profile

- **Developer**: Md Sabir Akhtar
- **Institution**: Bakhtiyarpur College of Engineering, Patna
- **Specialization**: Computer Science & Engineering (Internet of Things)
- **GitHub**: [github.com/sabirakhtarmd786-alt](https://github.com/sabirakhtarmd786-alt)
- **LinkedIn**: [linkedin.com/in/md-sabir-akhtar-87a525351](https://www.linkedin.com/in/md-sabir-akhtar-87a525351)
- **Email**: [sabirakhtarmd786@gmail.com](mailto:sabirakhtarmd786@gmail.com)
