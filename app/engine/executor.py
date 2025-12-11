import asyncio
import uuid
import time
from typing import Optional, Dict, Any, List

from app.engine.registry import call_tool
from app.utils.logger import log
from app.engine.graph import GraphManager

def evaluate_condition(expr: str, state: dict) -> bool:
    allowed_globals = {"__builtins__": {}}
    local_vars = {"state": state}
    try:
        return bool(eval(expr, allowed_globals, local_vars))
    except Exception:
        return False

class Executor:
    def __init__(self, store, graph_manager: GraphManager, persist_store=None):
        self.store = store
        self.graph_manager = graph_manager
        self.persist_store = persist_store 

    def start_run(self, req, background_tasks) -> str:
        run_id = req.run_id or f"run_{uuid.uuid4().hex[:8]}"
        initial_state = dict(req.initial_state)
        self.store.create_run(run_id, initial_state)
        background_tasks.add_task(self._run_background, run_id, req.graph_id)
        return run_id

    async def _run_background(self, run_id: str, graph_id: str):
        run_meta = {
            "run_id": run_id,
            "status": "running",
            "current_node": None,
            "state": self.store.get_state(run_id),
            "log": [],
            "started_at": time.time(),
        }
        self.store.update_run(run_id, run_meta)
        graph = self.graph_manager.get_graph(graph_id)
        if not graph:
            run_meta["status"] = "error"
            run_meta["error"] = "graph not found"
            self.store.update_run(run_id, run_meta)
            return

        node_name = graph["start_node"]
        try:
            while node_name:
                run_meta["current_node"] = node_name
                self.store.update_run(run_id, run_meta)

                node_spec = graph["nodes"].get(node_name)
                if node_spec is None:
                    run_meta["log"].append({"node": node_name, "event": "node not found"})
                    break

                fn_name = node_spec["fn"]
                params = node_spec.get("params") or {}

                state = self.store.get_state(run_id) or {}
                log_entry = {
                    "node": node_name,
                    "fn": fn_name,
                    "before_state_snapshot": dict(state),
                    "timestamp": time.time(),
                }
                await self.store.get_log_queue(run_id).put({"node": node_name, "event": "start", "fn": fn_name})
                result = await call_tool(fn_name, state, **params)
                if isinstance(result, dict):
                    state = result
                self.store.update_state(run_id, state)
                run_meta["state"] = state
                run_meta["log"].append({"node": node_name, "event": "completed", "fn": fn_name, "after_state_snapshot": dict(state), "timestamp": time.time()})
                await self.store.get_log_queue(run_id).put({"node": node_name, "event": "completed", "fn": fn_name, "state": state})

                edges = graph.get("edges", {})
                outgoing = edges.get(node_name)
                next_node = None
                if outgoing is None:
                    next_node = None
                elif isinstance(outgoing, str):
                    next_node = outgoing
                elif isinstance(outgoing, list):
                    for cond in outgoing:
                        expr = cond.get("if")
                        goto = cond.get("goto")
                        if expr is None or goto is None:
                            continue
                        if evaluate_condition(expr, state):
                            next_node = goto
                            break
                else:
                    next_node = None

                node_name = next_node

                if self.persist_store:
                    try:
                        self.persist_store.save_state(run_id, run_meta["state"])
                    except Exception:
                        log("warning: sqlite persist failed")

            run_meta["status"] = "finished"
            run_meta["finished_at"] = time.time()
            run_meta["current_node"] = None
            final_entry = {"final": True, "run_id": run_id, "status": "finished", "state": run_meta["state"]}
            await self.store.get_log_queue(run_id).put(final_entry)
            self.store.update_run(run_id, run_meta)
           
            if self.persist_store:
                self.persist_store.save_state(run_id, run_meta["state"])
        except Exception as e:
            run_meta["status"] = "error"
            run_meta["error"] = str(e)
            self.store.update_run(run_id, run_meta)
            await self.store.get_log_queue(run_id).put({"final": True, "run_id": run_id, "status": "error", "error": str(e)})
