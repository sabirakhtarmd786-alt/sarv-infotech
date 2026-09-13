# TechBlog — Modern Full-Stack Developer Blogging Platform

An interactive, responsive full-stack blogging platform built by **Md Sabir Akhtar** using **Python**, **SQLite**, and **HTML5/CSS Grid/JavaScript**.

---

## 📌 Features & Architecture

| Feature | Technical Implementation |
| :--- | :--- |
| **Design & Navigation** | Sticky header with brand logo, search bar, category filter pills, responsive card feeds, and post reader modal. |
| **Backend Development** | RESTful HTTP server handling JSON APIs and static asset routing; SQLite relational database with cascading foreign keys. |
| **Front-End Development** | Dynamic client interface built with vanilla JavaScript, modern CSS Grid/Flexbox, and responsive card layouts. |
| **User Authentication** | Secure user registration and login with salted **PBKDF2-SHA256** password hashing and token-based session management. |
| **Blog Post Creation** | Authenticated editor with cover image support, 1-click presets, live preview, live word count, and instant feed updates. |
| **Commenting System** | Nested article discussion threads allowing authenticated users to post real-time comments. |
| **Interactive Engagement** | Real-time Like/Heart counter (`❤️`), 1-click link sharing, and calculated reading time estimates. |
| **Search Functionality** | Real-time live search bar with 300ms debouncing that filters across titles, content, and categories. |
| **Categorized Sections** | Organized topics: **Software**, **Hardware & IoT** (merged), **Internship**, **Jobs**, and **General**. |
| **Mobile-Friendly Design** | 100% responsive interface with fluid breakpoints (desktop, tablet, mobile), card skeletons, and touch-friendly controls. |
| **Free Cloud Hosting** | Pre-configured with `render.yaml`, `Procfile`, and `requirements.txt` for 1-click deployment on Render.com or PythonAnywhere. |

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.8+ installed (no external `pip` packages required!).

### 2. Start the Server
```bash
cd tech-blog
python3 server.py --port 8080
```

### 3. Open in Browser
Visit **[http://localhost:8080](http://localhost:8080)** in your browser.

> **Default Seeded Account**:
> - **Username**: `sabir_akhtar`
> - **Password**: `demo1234`
> - *(Or click "Register" on the site to create your own account instantly!)*

---

## 🌐 Deploying Free to Cloud (Render.com)

1. **Push your code to GitHub**:
   ```bash
   git remote add origin https://github.com/sabirakhtarmd786-alt/tech-blog.git
   git branch -M main
   git push -u origin main
   ```
2. **Deploy on Render**:
   - Sign up at [https://render.com](https://render.com) (free).
   - Click **"New +"** → **"Web Service"**.
   - Connect your GitHub repository `sabirakhtarmd786-alt/tech-blog`.
   - Set the settings:
     - **Name**: `tech-blog`
     - **Runtime**: `Python`
     - **Build Command**: *(leave empty)*
     - **Start Command**: `python server.py --port $PORT`
     - **Plan**: `Free`
   - Click **"Create Web Service"**.
3. Your platform will be live at: `https://tech-blog.onrender.com`!

---

## 🧪 Automated Testing

Run the included unit test suite to verify all business logic, database tables, password hashing, post creation, comments, and search:

```bash
python3 test_blog.py
```
Output:
```text
..........
Ran 10 tests in 0.101s
OK
```

---

## 👨‍💻 Developer Profile

- **Author**: Md Sabir Akhtar
- **Institution**: Bakhtiyarpur College of Engineering, Patna
- **Specialization**: Computer Science & Engineering (Internet of Things)
- **GitHub**: [github.com/sabirakhtarmd786-alt](https://github.com/sabirakhtarmd786-alt)
- **LinkedIn**: [linkedin.com/in/md-sabir-akhtar-87a525351](https://www.linkedin.com/in/md-sabir-akhtar-87a525351)
- **Email**: [sabirakhtarmd786@gmail.com](mailto:sabirakhtarmd786@gmail.com)
