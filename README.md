# DevLog — Full-Stack Modern Blogging Platform

A responsive, full-stack blogging platform developed using **Python**, **SQLite**, and **HTML5/CSS Grid/JavaScript**. Engineered to fulfill all requirements of modern web development and software engineering submissions.

---

## 📌 Features & Requirements Checklist

| Requirement | Implementation Detail | Location in Project |
| :--- | :--- | :--- |
| **Design & Navigation** | Clean navigation header with brand logo, search bar, category filter pills, responsive card feeds, and post reader modal. | `static/index.html` & `static/style.css` |
| **Backend Development** | RESTful HTTP server handling JSON APIs and static asset routing; SQLite relational database with cascading foreign keys. | `server.py` & `database.py` |
| **Front-End Development** | Dynamic Single-Page Application (SPA) feel built with vanilla JavaScript, modern CSS Grid/Flexbox, and responsive card layouts. | `static/index.html`, `static/style.css`, `static/app.js` |
| **User Authentication** | Secure user registration and login with salted PBKDF2-SHA256 password hashing and token-based session management. | `static/auth.html`, `database.py` (Lines 118–226) |
| **Blog Post Creation** | Authenticated editor with live word count, category selection, validation, and instantaneous publishing to the feed. | `static/create-post.html` & `server.py` (Lines 150–165) |
| **Commenting System** | Nested discussion threads for each article allowing authenticated users to post real-time comments. | `static/index.html` (Lines 77–104) & `database.py` (Lines 279–310) |
| **Search Functionality** | Real-time live search bar with 300ms debouncing that filters articles across titles, content, and categories. | `static/app.js` (Lines 163–182) & `database.py` (Lines 240–266) |
| **Mobile-Friendly Design** | 100% responsive interface with fluid breakpoints (desktop, tablet, mobile), card skeletons, and touch-friendly controls. | `static/style.css` (Lines 835–880) |
| **Free Cloud Hosting** | Configured with `Procfile`, `render.yaml`, and `requirements.txt` for 1-click free deployment on Render.com or PythonAnywhere. | `render.yaml`, `Procfile`, `requirements.txt` |

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.8+ installed (no external `pip` packages required!).

### 2. Start the Server
```bash
cd /Users/sabir/.gemini/antigravity/scratch/fullstack-blog
python3 server.py --port 8080
```

### 3. Open in Browser
Visit **[http://localhost:8080](http://localhost:8080)** in your browser.

> **Default Seeded Account**:
> - **Username**: `sabir_akhtar`
> - **Password**: `demo1234`
> - *(Or click "Register" on the site to create your own account instantly!)*

---

## 🌐 How to Host Free on the Cloud

You can deploy this full-stack blog online for free in under 3 minutes using either **Render.com** or **PythonAnywhere**.

### Option A: Deploy on Render.com (Recommended Free Cloud Host)
1. **Push your code to GitHub**:
   - Create a new GitHub repository (e.g. `devlog-blog`).
   - Push the files in this folder to GitHub.
2. **Deploy on Render**:
   - Sign up at [https://render.com](https://render.com) (free).
   - Click **"New +"** → **"Web Service"**.
   - Connect your GitHub repository.
   - Set the settings:
     - **Name**: `devlog-blog`
     - **Runtime**: `Python`
     - **Build Command**: *(leave empty)*
     - **Start Command**: `python server.py --port $PORT`
     - **Plan**: `Free`
   - Click **"Create Web Service"**.
3. Your platform will be live at: `https://devlog-blog.onrender.com`!

---

### Option B: Deploy on PythonAnywhere (100% Free Forever)
1. Register for a free account at [https://www.pythonanywhere.com](https://www.pythonanywhere.com).
2. Open a **Bash Console** in your PythonAnywhere dashboard.
3. Clone or upload your project folder.
4. Set up a Web App pointing to `server.py` or run it as a background task.

---

## 🧪 Automated Testing

Run the included unit test suite to verify all business logic, database tables, password hashing, and post/comment operations:

```bash
python3 test_blog.py
```
Output:
```text
.........
Ran 9 tests in 0.084s
OK
```
