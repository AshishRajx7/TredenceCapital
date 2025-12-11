# Minimal Workflow Engine

A small workflow or agent engine built with FastAPI.  
It supports node-based execution, shared state transitions, conditional routing, tool registration, and live log streaming.  
The focus was to keep the system simple, clear, and easy to extend.

## Features
- Create workflow graphs through an API  
- Execute nodes step by step with shared state  
- Conditional branching  
- Background async execution  
- WebSocket log streaming  
- Decorator based tool registry  
- Example code review workflow included

## Folder Structure

<pre>
app
  main.py
  engine
    graph.py
    executor.py
    registry.py
    models.py
  storage
    memory_store.py
    sqlite_store.py
  workflows
    code_review.py
  utils
    logger.py
README.md
requirements.txt
</pre>



## How to Run
Install dependencies:
pip install -r requirements.txt


Start the server:
uvicorn app.main:app


## API Endpoints
<pre>
<h2><strong>POST /graph/create</strong></h2>
  <img width="1402" height="624" alt="image" src="https://github.com/user-attachments/assets/478aff3a-b062-4d0c-b1a1-bc4775547c51" />


<h2><strong>POST /graph/run</strong></h2>
  <img width="1377" height="609" alt="image" src="https://github.com/user-attachments/assets/f47be06a-8a48-4827-9a40-04720ba004c6" />


<h2><strong>GET /graph/state/{run_id}</strong></h2>
  <img width="1414" height="789" alt="image" src="https://github.com/user-attachments/assets/8bedad80-db90-4dcc-bbaa-9fc150102d3b" />

<h2><strong>WS /ws/logs/{run_id}</strong></h2>
<img width="1548" height="766" alt="image" src="https://github.com/user-attachments/assets/03526152-7c91-4d31-bdb9-deadcefcc44e" />


</pre>

## Example Workflow
A simple code review flow demonstrating the engine:
extract → check → detect → suggest


## Evaluation Criteria Addressed
- Clear project structure  
- Readable engine logic  
- Clean and simple APIs  
- State driven execution model  
- Good async and Python practices  
