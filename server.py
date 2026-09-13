import http.server
import socketserver
import json
import urllib.parse
import os
import sys
import mimetypes
import database

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

class BlogRequestHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Clean request logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[0]}\n")

    def send_json_response(self, data, status_code=200):
        response_bytes = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()
        self.wfile.write(response_bytes)

    def send_error_response(self, message, status_code=400):
        self.send_json_response({"error": message, "success": False}, status_code)

    def get_auth_user(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            return database.get_user_by_token(token)
        return None

    def read_json_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len == 0:
            return {}
        try:
            body = self.rfile.read(content_len).decode('utf-8')
            return json.loads(body)
        except Exception:
            return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.end_headers()

    # =========================================================================
    # GET Handlers
    # =========================================================================
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. REST API Routes
        if path.startswith("/api/"):
            self.handle_api_get(path, query)
            return

        # 2. Static File Serving
        self.serve_static_file(path)

    def handle_api_get(self, path, query):
        if path == "/api/auth/me":
            user = self.get_auth_user()
            if not user:
                self.send_error_response("Unauthorized", 401)
                return
            self.send_json_response({"user": user, "success": True})

        elif path == "/api/posts":
            search_q = query.get("q", [None])[0]
            cat = query.get("category", [None])[0]
            posts = database.get_posts(search_query=search_q, category=cat)
            self.send_json_response({"posts": posts, "total": len(posts), "success": True})

        elif path.startswith("/api/posts/"):
            parts = path.strip("/").split("/")
            if len(parts) == 3 and parts[2].isdigit():
                post_id = int(parts[2])
                post = database.get_post_by_id(post_id)
                if not post:
                    self.send_error_response("Post not found", 404)
                    return
                self.send_json_response({"post": post, "success": True})
            else:
                self.send_error_response("Invalid post endpoint", 404)

        elif path.startswith("/api/users/") and path.endswith("/profile"):
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[2].isdigit():
                user_id = int(parts[2])
                profile = database.get_user_profile(user_id)
                if not profile:
                    self.send_error_response("User not found", 404)
                    return
                self.send_json_response({"profile": profile, "success": True})
            else:
                self.send_error_response("Invalid user endpoint", 404)
        else:
            self.send_error_response("Endpoint not found", 404)

    # =========================================================================
    # POST Handlers
    # =========================================================================
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.read_json_body()

        if path == "/api/auth/register":
            username = body.get("username", "")
            email = body.get("email", "")
            password = body.get("password", "")
            bio = body.get("bio", "")
            user, err = database.register_user(username, email, password, bio)
            if err:
                self.send_error_response(err, 400)
            else:
                self.send_json_response({"user": user, "success": True}, 201)

        elif path == "/api/auth/login":
            username = body.get("username", "")
            password = body.get("password", "")
            user, err = database.login_user(username, password)
            if err:
                self.send_error_response(err, 401)
            else:
                self.send_json_response({"user": user, "success": True})

        elif path == "/api/auth/logout":
            auth_header = self.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
                database.delete_session(token)
            self.send_json_response({"message": "Logged out successfully", "success": True})

        elif path == "/api/posts":
            user = self.get_auth_user()
            if not user:
                self.send_error_response("You must be logged in to create a post.", 401)
                return
            title = body.get("title", "")
            content = body.get("content", "")
            category = body.get("category", "General")
            image_url = body.get("image_url", "")
            post, err = database.create_post(user["id"], title, content, category, image_url=image_url)
            if err:
                self.send_error_response(err, 400)
            else:
                self.send_json_response({"post": post, "success": True}, 201)

        elif path.startswith("/api/posts/") and path.endswith("/like"):
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[2].isdigit():
                post_id = int(parts[2])
                new_likes = database.like_post(post_id)
                self.send_json_response({"likes": new_likes, "success": True})
            else:
                self.send_error_response("Invalid like endpoint", 400)

        elif path.startswith("/api/posts/") and path.endswith("/comments"):
            user = self.get_auth_user()
            if not user:
                self.send_error_response("You must be logged in to leave a comment.", 401)
                return
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[2].isdigit():
                post_id = int(parts[2])
                content = body.get("content", "")
                comment, err = database.create_comment(post_id, user["id"], content)
                if err:
                    self.send_error_response(err, 400)
                else:
                    self.send_json_response({"comment": comment, "success": True}, 201)
            else:
                self.send_error_response("Invalid comment path", 400)

        else:
            self.send_error_response("Endpoint not found", 404)

    # =========================================================================
    # DELETE Handlers
    # =========================================================================
    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/posts/"):
            user = self.get_auth_user()
            if not user:
                self.send_error_response("Unauthorized", 401)
                return
            parts = path.strip("/").split("/")
            if len(parts) == 3 and parts[2].isdigit():
                post_id = int(parts[2])
                success, err = database.delete_post(post_id, user["id"])
                if err:
                    self.send_error_response(err, 403)
                else:
                    self.send_json_response({"message": "Post deleted successfully", "success": True})
            else:
                self.send_error_response("Invalid delete path", 400)
        else:
            self.send_error_response("Endpoint not found", 404)

    # =========================================================================
    # Static Files Serving
    # =========================================================================
    def serve_static_file(self, path):
        clean_path = path.strip("/")
        if clean_path == "" or clean_path == "index":
            rel_file = "index.html"
        elif clean_path == "auth":
            rel_file = "auth.html"
        elif clean_path == "create-post":
            rel_file = "create-post.html"
        elif clean_path == "profile":
            rel_file = "profile.html"
        elif clean_path == "calculator":
            rel_file = "calculator/index.html"
        else:
            rel_file = clean_path

        file_path = os.path.abspath(os.path.join(STATIC_DIR, rel_file))

        # Security check: prevent directory traversal
        if not file_path.startswith(STATIC_DIR) or not os.path.isfile(file_path):
            file_path = os.path.join(STATIC_DIR, "index.html")

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            if file_path.endswith(".svg"):
                mime_type = "image/svg+xml"
            else:
                mime_type = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "svg" in mime_type else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))

def run_server(port=8080, host="0.0.0.0"):
    database.init_db()
    server_address = (host, port)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, BlogRequestHandler) as httpd:
        print(f"============================================================")
        print(f"🚀 Modern Full-Stack Blog Platform Server Active!")
        print(f"📡 Local URL:    http://localhost:{port}")
        print(f"📁 Static Directory: {STATIC_DIR}")
        print(f"🛑 Press Ctrl+C to stop the server")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            httpd.shutdown()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    elif "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv) and sys.argv[idx + 1].isdigit():
            port = int(sys.argv[idx + 1])

    run_server(port=port)
