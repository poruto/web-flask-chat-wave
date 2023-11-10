import asyncio
import websockets
import threading
import json

class WebsocketClient:
    def __init__(self, websocketServer, websocket):
        self.websocketServer = websocketServer
        self.websocket = websocket
        self.status = None
        self.targetClient = None
        self.countryCode = None
        self.age = None
        self.sex = None
        self.valid = True
    
    async def send_message(self, msg, ignoreRecursion=False):
        try:
            await self.websocket.send(msg)
        except:
            print("Websocket disconnected")
            self.valid = False
            self.status = StatusTypes.DISCONNECTED

            if ignoreRecursion == False:
                if self.targetClient != None and self.targetClient != StatusTypes.DISCONNECTED:
                    data = {"event" : "STRANGER_DISCONNECT"}
                    await self.targetClient.send_message(json.dumps(data), ignoreRecursion=True)
                    self.targetClient.status = StatusTypes.DISCONNECTED

            if self in self.websocketServer.websocket_clients:
                self.websocketServer.websocket_clients.remove(self)
            

class WebsocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_thread = None
        self.websocket_clients = []
    
    def debug(self, msg):
        print("[WebsocketAPIServer]: %s" % msg)
    
    def get_client_by_websocket(self, websocket):
        for w in self.websocket_clients:
            if w.websocket == websocket:
                return w
        return None

    async def handle_client(self, websocket, path):
        try:
            async for message in websocket:
                self.debug(f"Received: {message}")

                #  Check if websocket is already in the system
                client = self.get_client_by_websocket(websocket)

                if client == None:
                    #  If first message, add client to list
                    client = WebsocketClient(self, websocket)
                    self.websocket_clients.append(client)
                
                #  Handle client's message
                jsonData = json.loads(message)
                self.debug(f"Handling event '{jsonData['event']}'")
                await EventHandler.handle_event(client, jsonData["event"], jsonData)
                
        except websockets.ConnectionClosed:
            #  On websocket close, remove the client from list
            client = self.get_client_by_websocket(websocket)
            self.debug("Websocket closed.")

            if client:
                self.websocket_clients.remove(client)
    
    #  Connect clients who are SEARCHING for a conversation
    async def connect_conversations(self):
        while True:
            clients = self.websocket_clients.copy()

            for c in clients:
                #  Send heart beat check packet from server
                data = {"event" : "HEARTBEAT"}
                await c.send_message(json.dumps(data))

                if c.valid and c.status == StatusTypes.SEARCHING:
                    target = self.get_random_searching_client(c)
                    
                    #  If target found
                    if target:
                        c.status = StatusTypes.INCONVO
                        target.status = StatusTypes.INCONVO

                        c.targetClient = target
                        target.targetClient = c

                        cData = {"event" : "INCONVO", "countryCode" : target.countryCode, "age" : target.age, "sex" : target.sex}
                        targetData = {"event" : "INCONVO", "countryCode" : c.countryCode, "age" : c.age, "sex" : c.sex}   

                        await c.send_message(json.dumps(cData))
                        await target.send_message(json.dumps(targetData))            

                        self.debug("Conversation found!")

            await asyncio.sleep(1)
    
    def get_random_searching_client(self, ignore_client):
        for c in self.websocket_clients:
            if c != ignore_client and c.valid and c.status == StatusTypes.SEARCHING:
                return c

    def start_server(self):
        self.debug("Running on -> host: %s, port: %s" % (self.host, self.port))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = websockets.serve(self.handle_client, self.host, self.port)
        loop.create_task(self.connect_conversations())
        loop.run_until_complete(server)
        loop.run_forever()

    def run_in_thread(self):
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.start()

    def stop_server(self):
        if self.server_thread:
            self.server_thread.join()

class EventHandler:
    EVENTS = {}

    @classmethod
    def register_event(cls, event_name):
        def decorator(handler_func):
            cls.EVENTS[event_name] = handler_func
            return handler_func
        return decorator

    @classmethod
    async def handle_event(cls, client, event_name, json_object):
        handler = cls.EVENTS.get(event_name)
        if handler and callable(handler):
            await handler(client, json_object)
        else:
            print(f"Handler for event '{event_name}' not found.")

@EventHandler.register_event("searching")
async def client_searching(client, json_object):
    client.status = StatusTypes.SEARCHING
    client.age = json_object["age"]
    client.sex = json_object["sex"]
    client.countryCode = json_object["countryCode"]

@EventHandler.register_event("disconnect")
async def client_disconnect(client, json_object):
    client.status = StatusTypes.DISCONNECTED

    if client.targetClient != None:
        data = {"event" : "STRANGER_DISCONNECT"}
        client.targetClient.status = StatusTypes.DISCONNECTED
        await client.targetClient.send_message(json.dumps(data))

@EventHandler.register_event("message")
async def client_message(client, json_object):
    message = json_object["data"]

    if client.status == StatusTypes.INCONVO:
        if client.targetClient:
            data = {"event" : "RECEIVED_MESSAGE", "data" : message}
            await client.targetClient.send_message(json.dumps(data))
    
class StatusTypes:
    SEARCHING = "SEARCHING"
    INCONVO = "INCONVO"
    DISCONNECTED = "DISCONNECTED"
