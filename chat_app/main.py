import uvicorn
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session

from chat_app.config import HOST, PORT
from chat_app.db import get_db, engine, Base
from chat_app.models import Chat, Message
from chat_app.websocket import manager

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"hello": "world"}


@app.get("/chats", response_model=list)
def list_chats(db: Session = Depends(get_db)) -> list:
    return db.query(Chat).all()


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
    uvicorn.run(app, host=HOST, port=PORT)
