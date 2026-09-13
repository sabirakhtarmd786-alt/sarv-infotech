import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta, timezone

DB_FILE = os.environ.get("BLOG_DB_FILE", "blog.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str, salt: str = None) -> tuple:
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return key.hex(), salt

def verify_password(stored_hash: str, salt: str, password: str) -> bool:
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(stored_hash, new_hash)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            bio TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sessions Table (Authentication Tokens)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Blog Posts Table with image_url and likes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            image_url TEXT DEFAULT '',
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Comments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()

    # Seed demo user & initial sample posts if database is empty
    cursor.execute("SELECT COUNT(*) AS count FROM users")
    if cursor.fetchone()['count'] == 0:
        seed_initial_data(conn)

    conn.close()

def seed_initial_data(conn):
    cursor = conn.cursor()
    # Create default demo user
    pwd_hash, salt = hash_password("demo1234")
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, salt, bio)
        VALUES (?, ?, ?, ?, ?)
    ''', ("sabir_akhtar", "sabirakhtarmd786@gmail.com", pwd_hash, salt, 
          "2nd Year CSE-IoT student @ BCE Patna. Exploring Java, DSA, Web Development, and IoT."))
    
    author_id = cursor.lastrowid

    # Seed Sample Posts across categories:
    # Software, Hardware & IoT (merged!), Internship, Jobs, General
    posts_data = [
        (
            author_id,
            "Mastering Object-Oriented Design in Java: A Beginner's Guide",
            "Writing clean software is about more than just syntax. In this guide, we dive into the four pillars of OOP—Encapsulation, Abstraction, Inheritance, and Polymorphism—and explore how they translate into production code in Java. Structuring classes properly makes codebases easier to maintain, test, and scale over time.",
            "Software",
            "/assets/software-banner.svg",
            14
        ),
        (
            author_id,
            "ESP32 & Microcontrollers: Building an End-to-End IoT Pipeline with MQTT",
            "Hardware meets software! In this article, we merge microcontroller circuits with cloud IoT pipelines. We explore how to wire sensors to an ESP32 board, read telemetry (temperature, humidity, pressure), publish data over lightweight MQTT topics, and ingest the packets with Python to plot real-time environmental metrics.",
            "Hardware & IoT",
            "/assets/hardware-iot-banner.svg",
            27
        ),
        (
            author_id,
            "How 2nd-Year College Students Can Land Remote Internships",
            "Landing your first software internship early in college comes down to building proof of work. Rather than relying solely on your college syllabus, build 2-3 end-to-end projects, document them clearly on GitHub, write about your learning journey on LinkedIn, and connect with engineering founders and alumni with specific questions.",
            "Internship",
            "/assets/internship-banner.svg",
            32
        ),
        (
            author_id,
            "Cracking the Tech Resume: What Engineering Recruiters Actually Look For",
            "A software engineering resume has 6-10 seconds to make an impression. Focus on quantifiable impacts: mention the exact technologies used (Java, Python, HTML/CSS), link to live deployed projects and active GitHub repositories, and highlight your problem-solving experience in Data Structures & Algorithms.",
            "Jobs",
            "/assets/jobs-banner.svg",
            19
        ),
        (
            author_id,
            "Learning by Doing: Why Building Projects Beats Passive Watching",
            "Tutorial hell is a common trap for new developers. Watching hours of coding videos creates an illusion of competence, but true learning happens when you face compiler errors, debug tricky edge cases, and design solutions from scratch. Embrace the struggle—it is where real growth occurs!",
            "General",
            "/assets/general-banner.svg",
            23
        )
    ]

    for post in posts_data:
        cursor.execute('''
            INSERT INTO posts (author_id, title, content, category, image_url, likes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', post)
        post_id = cursor.lastrowid
        
        # Seed comments
        if post[3] == "Software":
            cursor.execute('''
                INSERT INTO comments (post_id, author_id, content)
                VALUES (?, ?, ?)
            ''', (post_id, author_id, "Great explanation! Design patterns like Factory and Observer build naturally on these OOP principles."))
        elif post[3] == "Hardware & IoT":
            cursor.execute('''
                INSERT INTO comments (post_id, author_id, content)
                VALUES (?, ?, ?)
            ''', (post_id, author_id, "Merging hardware with MQTT is super clean. The ESP32 is definitely the go-to board for IoT."))
        elif post[3] == "Internship":
            cursor.execute('''
                INSERT INTO comments (post_id, author_id, content)
                VALUES (?, ?, ?)
            ''', (post_id, author_id, "Very practical advice. Having a portfolio with working live demos made a huge difference in my interviews."))

    conn.commit()

# =========================================================================
# User & Authentication Operations
# =========================================================================

def register_user(username: str, email: str, password: str, bio: str = ""):
    username = username.strip()
    email = email.strip().lower()
    
    if len(username) < 3:
        return None, "Username must be at least 3 characters long."
    if len(password) < 6:
        return None, "Password must be at least 6 characters long."
    if "@" not in email or "." not in email:
        return None, "Invalid email address format."

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check for duplicate
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        return None, "Username or Email is already registered."

    pwd_hash, salt = hash_password(password)
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, salt, bio)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, pwd_hash, salt, bio))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Generate initial session token
        token = secrets.token_hex(24)
        expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        cursor.execute('''
            INSERT INTO sessions (token, user_id, expires_at)
            VALUES (?, ?, ?)
        ''', (token, user_id, expires))
        conn.commit()

        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "bio": bio,
            "token": token
        }
        conn.close()
        return user, None
    except Exception as e:
        conn.close()
        return None, f"Registration failed: {str(e)}"

def login_user(username_or_email: str, password: str):
    identifier = username_or_email.strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE username = ? OR email = ?
    ''', (identifier, identifier.lower()))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return None, "Invalid username/email or password."

    if not verify_password(user['password_hash'], user['salt'], password):
        conn.close()
        return None, "Invalid username/email or password."

    # Create new session token
    token = secrets.token_hex(24)
    expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    cursor.execute('''
        INSERT INTO sessions (token, user_id, expires_at)
        VALUES (?, ?, ?)
    ''', (token, user['id'], expires))
    conn.commit()

    user_data = {
        "id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "bio": user['bio'],
        "token": token
    }
    conn.close()
    return user_data, None

def get_user_by_token(token: str):
    if not token:
        return None
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT u.id, u.username, u.email, u.bio, u.created_at
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.token = ? AND s.expires_at > ?
    ''', (token, datetime.now(timezone.utc).isoformat()))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def delete_session(token: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

# =========================================================================
# Blog Posts Operations
# =========================================================================

def create_post(author_id: int, title: str, content: str, category: str = "General", image_url: str = ""):
    title = title.strip()
    content = content.strip()
    category = category.strip() or "General"
    image_url = image_url.strip()

    if len(title) < 3:
        return None, "Title must be at least 3 characters long."
    if len(content) < 10:
        return None, "Post content must be at least 10 characters long."

    # Default fallback image if none provided
    if not image_url:
        cat_lower = category.lower()
        if "software" in cat_lower:
            image_url = "/assets/software-banner.svg"
        elif "hardware" in cat_lower or "iot" in cat_lower:
            image_url = "/assets/hardware-iot-banner.svg"
        elif "intern" in cat_lower:
            image_url = "/assets/internship-banner.svg"
        elif "job" in cat_lower:
            image_url = "/assets/jobs-banner.svg"
        else:
            image_url = "/assets/general-banner.svg"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (author_id, title, content, category, image_url, likes)
        VALUES (?, ?, ?, ?, ?, 0)
    ''', (author_id, title, content, category, image_url))
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return get_post_by_id(post_id), None

def get_posts(search_query: str = None, category: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = '''
        SELECT p.id, p.title, p.content, p.category, p.image_url, p.likes, p.created_at,
               u.id as author_id, u.username as author_name,
               (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) as comment_count
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE 1=1
    '''
    params = []

    if search_query:
        query_pattern = f"%{search_query.strip()}%"
        sql += " AND (p.title LIKE ? OR p.content LIKE ? OR p.category LIKE ?)"
        params.extend([query_pattern, query_pattern, query_pattern])

    if category and category.lower() != "all":
        # Handle flexible match for merged hardware & iot
        if "hardware" in category.lower() or "iot" in category.lower():
            sql += " AND (LOWER(p.category) LIKE '%hardware%' OR LOWER(p.category) LIKE '%iot%')"
        else:
            sql += " AND LOWER(p.category) = LOWER(?)"
            params.append(category.strip())

    sql += " ORDER BY p.created_at DESC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    posts = [dict(row) for row in rows]
    conn.close()
    return posts

def get_post_by_id(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.id, p.title, p.content, p.category, p.image_url, p.likes, p.created_at,
               u.id as author_id, u.username as author_name, u.bio as author_bio
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    if not post:
        conn.close()
        return None

    post_dict = dict(post)
    # Fetch comments for this post
    cursor.execute('''
        SELECT c.id, c.content, c.created_at,
               u.id as author_id, u.username as author_name
        FROM comments c
        JOIN users u ON c.author_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    ''', (post_id,))
    comments = [dict(c) for c in cursor.fetchall()]
    post_dict['comments'] = comments
    conn.close()
    return post_dict

def like_post(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()

    cursor.execute("SELECT likes FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()
    return row['likes'] if row else 0

def delete_post(post_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Post not found."
    if row['author_id'] != user_id:
        conn.close()
        return False, "You do not have permission to delete this post."

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return True, None

# =========================================================================
# Comments Operations
# =========================================================================

def create_comment(post_id: int, author_id: int, content: str):
    content = content.strip()
    if not content:
        return None, "Comment cannot be empty."

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check post exists
    cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cursor.fetchone():
        conn.close()
        return None, "Post does not exist."

    cursor.execute('''
        INSERT INTO comments (post_id, author_id, content)
        VALUES (?, ?, ?)
    ''', (post_id, author_id, content))
    conn.commit()
    comment_id = cursor.lastrowid

    cursor.execute('''
        SELECT c.id, c.content, c.created_at, u.username as author_name
        FROM comments c
        JOIN users u ON c.author_id = u.id
        WHERE c.id = ?
    ''', (comment_id,))
    new_comment = dict(cursor.fetchone())
    conn.close()
    return new_comment, None

# =========================================================================
# Profile Operations
# =========================================================================

def get_user_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, email, bio, created_at
        FROM users WHERE id = ?
    ''', (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return None

    profile = dict(user)
    # Get user's posts
    cursor.execute('''
        SELECT p.id, p.title, p.category, p.image_url, p.likes, p.created_at,
               (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) as comment_count
        FROM posts p
        WHERE p.author_id = ?
        ORDER BY p.created_at DESC
    ''', (user_id,))
    profile['posts'] = [dict(r) for r in cursor.fetchall()]
    profile['total_posts'] = len(profile['posts'])
    conn.close()
    return profile
