# TechBlog — Full-Stack Developer Blogging Platform

A responsive, feature-rich blogging platform built with **Python 3**, **SQLite**, **HTML5**, **CSS3**, and **vanilla JavaScript**.

---

## 📌 Features

- **Categorized Sections**: `Software`, `Hardware & IoT`, `Internship`, `Jobs`, and `General`.
- **Media & Banners**: Category-specific SVG banners and custom image support for blog articles.
- **Authentication**: Salted PBKDF2-SHA256 password hashing, token-based sessions.
- **Interactivity**: Likes counter, link sharing, nested comments, reading time calculation, live debounced search.
- **Responsive UI**: Clean desktop and mobile layouts.

---

## 🚀 How to Run TechBlog Independently

### 1. Prerequisites
Python 3.8+ (no third-party pip dependencies required).

### 2. Start the TechBlog Server
```bash
cd techblog
python3 server.py --port 8080
```

### 3. Open in Browser
Visit: **[http://localhost:8080](http://localhost:8080)**

---

## 🧪 Running Automated Tests

```bash
cd techblog
python3 test_blog.py
```
Outputs:
```text
Ran 10 tests in 0.088s
OK
```
