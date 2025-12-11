import asyncio
from typing import Dict, Any, Optional

class MemoryStore:
    def __init__(self):
        self.graphs: Dict[str, Any] = {}
        self.run_states: Dict[str, Dict[str, Any]] = {}
        self.log_queues: Dict[str, asyncio.Queue] = {}
        self.run_meta: Dict[str, Dict[str, Any]] = {}

    def save_graph(self, graph_id: str, graph: Dict[str, Any]):
        self.graphs[graph_id] = graph

    def load_graph(self, graph_id: str) -> Optional[Dict[str, Any]]:
        return self.graphs.get(graph_id)

    def create_run(self, run_id: str, initial_state: Dict[str, Any]):
        self.run_states[run_id] = dict(initial_state)
        self.log_queues[run_id] = asyncio.Queue()
        self.run_meta[run_id] = {
            "run_id": run_id,
            "status": "created",
            "state": dict(initial_state),
            "log": [],
            "current_node": None,
        }

    def update_state(self, run_id: str, state: Dict[str, Any]):
        self.run_states[run_id] = state
        meta = self.run_meta.get(run_id)
        if meta is not None:
            meta["state"] = state

    def get_state(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self.run_states.get(run_id)

    def get_log_queue(self, run_id: str) -> Optional[asyncio.Queue]:
        return self.log_queues.get(run_id)

    def update_run(self, run_id: str, meta: Dict[str, Any]):
        self.run_meta[run_id] = meta

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        return self.run_meta.get(run_id)
