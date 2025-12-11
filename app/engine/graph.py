from typing import Dict, Any
from uuid import uuid4
from app.engine.models import CreateGraphRequest

class GraphManager:
    def __init__(self, store):
        self.store = store

    def create_graph(self, req: CreateGraphRequest) -> str:
        graph_id = req.graph_id or f"graph_{uuid4().hex[:8]}"
        graph = {
            "graph_id": graph_id,
            "start_node": req.start_node,
            "nodes": {name: spec.dict() for name, spec in req.nodes.items()},
            "edges": req.edges,
        }
        self.store.save_graph(graph_id, graph)
        return graph_id

    def get_graph(self, graph_id: str) -> Dict[str, Any]:
        return self.store.load_graph(graph_id)
