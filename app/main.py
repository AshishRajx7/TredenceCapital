from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import app.workflows.code_review

from app.storage.memory_store import MemoryStore
from app.storage.sqlite_store import SQLiteStore
from app.engine.graph import GraphManager
from app.engine.executor import Executor
from app.engine.models import CreateGraphRequest, RunRequest

app = FastAPI(title="Minimal Workflow Engine")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_store = MemoryStore()
sqlite_store = SQLiteStore("runs.db")

graph_manager = GraphManager(memory_store)
executor = Executor(memory_store,graph_manager,persist_store=sqlite_store)

@app.get("/")
async def health():
    return {"status": "ok", "message": "Workflow Engine is running"}

@app.post("/graph/create")
async def create_graph(request: CreateGraphRequest):
    graph_id = graph_manager.create_graph(request)
    return {"graph_id": graph_id}

@app.post("/graph/run")
async def run_graph(req: RunRequest, background_tasks: BackgroundTasks):
    run_id = executor.start_run(req,background_tasks)
    return {"run_id": run_id}

@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    run = memory_store.get_run(run_id)
    if not run:
        return {"error": "run not found"}

    return {
        "run_id": run_id,
        "status": run.get("status"),
        "current_node": run.get("current_node"),
        "state": run.get("state"),
        "log": run.get("log", []),
        "error": run.get("error")
    }


@app.websocket("/ws/logs/{run_id}")
async def websocket_logs(websocket: WebSocket, run_id:str):
    await websocket.accept()
    queue = memory_store.get_log_queue(run_id)
    if queue is None:
        await websocket.close(code=1008)
        return
    try:
        while True:
            entry = await queue.get()
            await websocket.send_json(entry)
            if entry.get("final", False):
                await websocket.close()
                break
    except WebSocketDisconnect:
        return      