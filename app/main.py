import asyncio
import redis
import socketio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from threading import Thread
from fastapi.middleware.cors import CORSMiddleware
import pickle


app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", transports=["websocket"])
app.mount("/socket.io", socketio.ASGIApp(sio, socketio_path="socket.io"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

redis_client = redis.Redis(host='redis-sigasiga', port=6379, db=0, decode_responses=False)

@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")
    await sio.emit("message", {"data": "Bienvenido maquinola"}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

def redis_listener():
    """
    This function is a Redis listener that listens to the socket_io_data channel and emits the data to the socket.io server.
    The data is emitted to the socket.io server using the sio.emit function.
    The data is emitted to the socket.io server using the sio.emit function.
    input data example:
    {
        "event_id": "123",
        "event_type": "config_room-rtmp_status",
        "data": {"rtmp_status": True}
    }
    the message published to redis is serialized using pickle.dumps and published to the socket_io_data channel.
    the message received from redis is deserialized using pickle.loads.
    the data is emitted to the socket.io server using the sio.emit function.
    the socket.io server emits the data to the client using the socket.io client.
    the socket.io client receives the data and emits the data to the client using the socket.io client.
    the socket.io client receives the data and emits the data to the client using the socket.io client.
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe("socket_io_data")
    print("ScoketIO Redis listener started...")
    for message in pubsub.listen():
        if message["type"] == "message":
            pickle_data = message["data"]
            data = pickle.loads(pickle_data)
            event_id = data.get("event_id")
            event_type = data.get("event_type")
            data = data.get("data")
            socket_event = f"{event_id}-{event_type}"
            # print(f"Evento recibido desde Redis: {socket_event} con datos: {data}")
            room = "mi_sala"
            asyncio.run(sio.emit(socket_event, {"data": data}))

def start_redis_listener():
    thread = Thread(target=redis_listener)
    thread.daemon = True
    thread.start()

start_redis_listener()
@app.get("/")
async def get():
    # HTML response with a simple message
    return HTMLResponse("<h1>Socket.IO FastAPI Server</h1><p>Conectado a Redis</p>")