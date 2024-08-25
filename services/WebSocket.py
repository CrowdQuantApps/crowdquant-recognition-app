import json
import asyncio
import websockets


class WebSocketService:
    def __init__(self, address="127.0.0.1", port=8008, max_size=None):
        self.socket = None
        self.url = (address, port)
        self.variable_name = None
        self.handle_message_fn = None
        self.server = None
        self.clients = set()
        self.message_handlers = {}
        self.default_handler = None
        self.max_size = max_size

    async def start(self):
        await asyncio.gather(
            self.start_server(),
            self.start_client()
        )

    async def start_client(self):
        self.socket = await websockets.connect(f"ws://{self.url[0]}:{self.url[1]}")

    async def start_server(self):
        try:
            self.server = await websockets.serve(self.handle_client_connection, self.url[0], self.url[1],
                                                 max_size=self.max_size)
            print(f"WebSocket server started at ws://{self.url[0]}:{self.url[1]}")
            await self.server.wait_closed()
        except OSError:
            print(f"Address {self.url[0]}:{self.url[1]} already in use. Retrying...")
            await asyncio.sleep(5)
            await self.start_server()

    async def handle_client_connection(self, websocket):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                await self.handle_message(message)
        finally:
            self.clients.remove(websocket)

    async def stop(self):
        await self.stop_client()
        await self.stop_server()

    async def stop_client(self):
        if self.socket:
            await self.socket.close()

    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    async def send(self, variable_name, data):
        if self.clients:
            json_data = json.dumps({'variable_name': variable_name, 'value': data})
            await asyncio.wait([client.send(json_data) for client in self.clients])
        else:
            print('WebSocket no clients connected')

    def on_message(self, handle_message_fn, variable_name=None):
        if variable_name:
            self.message_handlers[variable_name] = handle_message_fn
        else:
            self.default_handler = handle_message_fn

    async def handle_message(self, message):
        try:
            data = json.loads(message)
            variable_name = data.get('variable_name')
            if variable_name in self.message_handlers:
                handle_message_fn = self.message_handlers[variable_name]
                handle_message_fn(data.get('value'))
            elif self.default_handler:
                self.default_handler(data)
                print('Received data:', data)
            else:
                print('No handler found for variable:', variable_name)
        except json.JSONDecodeError:
            print("Received message is not valid JSON:", message)

    @staticmethod
    def on_error(error):
        print('WebSocket error:', error)
