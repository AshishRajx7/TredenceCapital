from pydantic import BaseModel
from typing import List, Optional,Dict,Any,Union

class NodeSpec(BaseModel):
    fn:str
    params:Optional[Dict[str,Any]] = None
    
class ConditionalEdge(BaseModel):
    if_Expr:str
    goto:str
    
class CreateGraphRequest(BaseModel):
    graph_id:Optional[str] = None
    start_node: str
    nodes: Dict[str, NodeSpec]
    edges: Dict[str, Optional[Union[str, List[Dict[str, str]]]]]
    
class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str,Any]
    run_id: Optional[str] = None           