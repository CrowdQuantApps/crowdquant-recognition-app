import os

from services.Flask import FlaskService
from router.routes import routes_bp
from utils.app_root_dir import app_root_dir


class HttpServerService:
    def __init__(self, address="127.0.0.1", port=8001):
        self.address = (address, port)
        self.app = FlaskService(__name__, static_folder="app/static") #, static_folder="../app"
        self.register_routes()

    def start(self):
        root_path = self.app.root_path
        print("Root path of the Flask application:", root_path)
        print(f"Server HTTP started at http://{self.address[0]}:{self.address[1]}")
        self.app.run(host=self.address[0], port=self.address[1])

    def register_routes(self):
        self.app.register_blueprint(routes_bp)


"""
import os
import socketserver
import http.server


class HttpServerService:
    def __init__(self, address="127.0.0.1", port=8001):
        self.address = (address, port)

    def start(self):
        os.chdir("app")
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(self.address, handler) as httpd:
            print(f"Server HTTP started at http://{self.address[0]}:{self.address[1]}")
            httpd.serve_forever()
"""
