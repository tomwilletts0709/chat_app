import uvicorn
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session

from chat_app.config import HOST, PORT
from chat_app.db import get_db, engine, Base
from chat_app.models import Chat, Message
from chat_app.websocket import manager
from chat_app.api import router

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/api", tags=["chats"])


@app.get("/")
def read_root() -> dict:
    return {"hello": "world"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message received: {data}")
    except Exception:
        manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=8000)