import http.server
import socketserver
import urllib.parse
import os
import sys
import mimetypes

# Set up module directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TECHBLOG_DIR = os.path.join(ROOT_DIR, "techblog")
CALCULATOR_DIR = os.path.join(ROOT_DIR, "calculator")

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from techblog.server import TechBlogRequestHandler
import techblog.database as database

class UnifiedHubRequestHandler(TechBlogRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Calculator Routes
        if path == "/calculator" or path == "/calculator/":
            self.serve_calculator_file("index.html")
            return
        elif path.startswith("/calculator/"):
            rel_path = path[len("/calculator/"):].lstrip("/")
            self.serve_calculator_file(rel_path)
            return

        # 2. REST API Routes
        if path.startswith("/api/"):
            self.handle_api_get(path, query)
            return

        # 3. TechBlog Static File Serving
        self.serve_static_file(path)

    def serve_calculator_file(self, rel_path):
        if not rel_path or rel_path == "":
            rel_path = "index.html"
        file_path = os.path.abspath(os.path.join(CALCULATOR_DIR, rel_path))
        if not file_path.startswith(CALCULATOR_DIR) or not os.path.isfile(file_path):
            file_path = os.path.join(CALCULATOR_DIR, "index.html")

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            if file_path.endswith(".js"):
                mime_type = "application/javascript"
            elif file_path.endswith(".css"):
                mime_type = "text/css"
            else:
                mime_type = "text/html"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8" if "text" in mime_type or "javascript" in mime_type else mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))

def run_hub_server(port=8080, host="0.0.0.0"):
    database.init_db()
    server_address = (host, port)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, UnifiedHubRequestHandler) as httpd:
        print(f"============================================================")
        print(f"🚀 Sarv-Infotech Unified Server Active!")
        print(f"📡 TechBlog:   http://localhost:{port}/")
        print(f"🧮 Calculator: http://localhost:{port}/calculator")
        print(f"📁 TechBlog Dir:   {TECHBLOG_DIR}")
        print(f"📁 Calculator Dir: {CALCULATOR_DIR}")
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

    run_hub_server(port=port)
