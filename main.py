import asyncio
import os
import shutil

import webview
import threading
from services.HttpServer import HttpServerService
from services.WebSocket import WebSocketService
from utils.get_taskbar_height import get_taskbar_height
from libs.Recognition import Recognition

previous_window_size = None
previous_window_position = None


# ==================|)
# [*] CrowdQuant
# [*] > | App Class
# [*] > | v1.0
# ==================|)
class App:
    def __init__(self):
        self.app_name = "CrowdQuant"
        self.http_server_thread = None
        self.websocket_thread = None
        self.client_ui_thread = None
        self.websocket = None
        self.client_ui = None
        self.webview = webview

        self.loaded_handler = None

    async def start(self):
        self.cleanData()
        self.createDataFolders()
        self.http_server_thread = threading.Thread(target=HttpServerService("127.0.0.1", 8001).start)
        self.http_server_thread.daemon = True  # Set the thread as daemon
        self.http_server_thread.start()

        self.websocket = WebSocketService("127.0.0.1", 8008, 512000000)
        self.websocket_thread = threading.Thread(target=lambda: asyncio.run(self.websocket.start()))
        self.websocket_thread.daemon = True  # Set the thread as daemon
        self.websocket_thread.start()

        self.client_ui = webview.create_window("CrowdQuant", url="http://127.0.0.1:8001", width=1024, height=770,
                                               resizable=False, frameless=True)
        self.loaded_handler = self.on_loaded_handler
        self.client_ui.events.loaded += self.loaded_handler
        self.websocket.on_message(self.toolbar_action, "app_toolbar_action")
        self.websocket.on_message(self.image_recognition, "image_recognition_media_filename")
        self.websocket.on_message(self.rtsp_recognition, "rtsp_recognition")
        self.websocket.on_message(self.camera_recognition, "camera_recognition")

        webview.start()

    def stop(self):
        self.http_server_thread.stop()
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.stop(), asyncio.get_event_loop())

        self.webview.stop()

    def on_loaded_handler(self):
        self.websocket.on_message(variable_name="window_ready", handle_message_fn=self.on_loaded)

    def on_loaded(self, window_ready):
        global previous_window_size, previous_window_position
        self.client_ui.events.loaded -= self.loaded_handler
        self.loaded_handler = None
        if window_ready:
            screen_width, screen_height = webview.screens[0].width, webview.screens[0].height
            new_width = 1280
            new_height = 800
            x = (screen_width - new_width) // 2
            y = (screen_height - new_height) // 2
            webview.windows[0].move(x, y)
            webview.windows[0].resize(new_width, new_height)
            previous_window_size = (new_width, new_height)
            previous_window_position = (x, y)

    @staticmethod
    def toolbar_action(action):
        global previous_window_size, previous_window_position

        if action == "minimize":
            webview.windows[0].minimize()
        elif action == "maximize":
            screen_width, screen_height = webview.screens[0].width, webview.screens[0].height
            taskbar_height = get_taskbar_height()
            webview.windows[0].move(0, 0)
            webview.windows[0].resize(screen_width, screen_height - taskbar_height)
        elif action == "restore":
            if previous_window_size:
                width, height = previous_window_size
                x, y = previous_window_position
                webview.windows[0].move(x, y)
                webview.windows[0].resize(width, height)
        elif action == "close":
            webview.windows[0].destroy()

    @staticmethod
    def cleanData():
        try:
            shutil.rmtree("data")
            print("Data succesfully cleaned.")
        except OSError as e:
            print(f"An error occurred while deleting the folder: {e}")

    @staticmethod
    def createDataFolders():
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        temp_dir = os.path.join(data_dir, "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        processed_dir = os.path.join(data_dir, "processed")
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)

    @staticmethod
    def image_recognition(media_filename):
        if os.path.isfile("data/processed/image.png"):
            os.unlink("data/processed/image.png")
        Recognition(media_filename).Image()

    @staticmethod
    def rtsp_recognition(media_url):
        Recognition(media_url).Live()

    @staticmethod
    def camera_recognition(val):
        Recognition().Camera()


if __name__ == "__main__":
    asyncio.run(App().start())
