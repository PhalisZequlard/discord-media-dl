from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.queue_utils import download_queue
import uvicorn
from typing import List
import json
import asyncio
from datetime import datetime, timedelta
from config import Config

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_state(self, data: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(data))

manager = ConnectionManager()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "allowed_users": Config.ALLOWED_USERS,
            "concurrent_downloads": Config.CONCURRENT_DOWNLOADS
        }
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send current state every second
            await websocket.receive_text()
            current_state = {
                "stats": {
                    "active": len(download_queue.active_downloads),
                    "queued": download_queue.queue.qsize(),
                    "completed_today": len([
                        task for task in download_queue.history 
                        if task.completed_at and 
                        datetime.fromtimestamp(task.completed_at) > datetime.now() - timedelta(days=1)
                    ])
                },
                "active_downloads": [
                    {
                        "id": task.id,
                        "type": task.type.value,
                        "url": task.url,
                        "status": task.status.value,
                        "progress": task.progress,
                        "started_at": datetime.fromtimestamp(task.started_at).strftime("%Y-%m-%d %H:%M:%S") if task.started_at else None
                    } 
                    for task in download_queue.active_downloads.values()
                ],
                "history": [
                    {
                        "id": task.id,
                        "type": task.type.value,
                        "url": task.url,
                        "status": task.status.value,
                        "options": task.options,
                        "started_at": datetime.fromtimestamp(task.started_at).strftime("%Y-%m-%d %H:%M:%S") if task.started_at else None,
                        "completed_at": datetime.fromtimestamp(task.completed_at).strftime("%Y-%m-%d %H:%M:%S") if task.completed_at else None
                    }
                    for task in download_queue.history[-100:]  # Show last 100 downloads
                ]
            }
            await websocket.send_text(json.dumps(current_state))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def start_web_server():
    config = uvicorn.Config(
        app,
        host=Config.WEB_HOST,
        port=Config.WEB_PORT,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()