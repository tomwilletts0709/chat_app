from fastapi import WebSocket
from typing import Dict, List, Optional


class ConnectionManager:
    """Manages active WebSocket connections. Supports per-user targeting and broadcast."""

    def __init__(self) -> None:
        # user_id -> list of WebSockets (user_id can be None for anonymous)
        self.active_connections: Dict[Optional[int], List[WebSocket]] = {}
        # Track websocket -> user_id for disconnect
        self._ws_to_user: Dict[WebSocket, Optional[int]] = {}

    async def connect(self, websocket: WebSocket, user_id: Optional[int] = None) -> None:
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        self._ws_to_user[websocket] = user_id

    def disconnect(self, websocket: WebSocket) -> None:
        user_id = self._ws_to_user.pop(websocket, None)
        if user_id is not None and user_id in self.active_connections:
            conns = self.active_connections[user_id]
            if websocket in conns:
                conns.remove(websocket)
            if not conns:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: int, message: str) -> None:
        if user_id not in self.active_connections:
            return
        disconnected = []
        for ws in self.active_connections[user_id]:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(ws)
        for ws in disconnected:
            self.disconnect(ws)

    async def broadcast(self, message: str) -> None:
        disconnected = []
        for user_id, conns in list(self.active_connections.items()):
            for ws in conns:
                try:
                    await ws.send_text(message)
                except Exception:
                    disconnected.append(ws)
        for ws in disconnected:
            self.disconnect(ws)


manager = ConnectionManager()
