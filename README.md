# Minimal Workflow Engine

A simple workflow or agent engine built using FastAPI.  
Supports node based execution, conditional edges, background execution, tool registry, and WebSocket log streaming.

## Features
- Create workflow graphs through API
- Execute workflows with shared state
- Register custom tools using decorators
- Conditional branching based on state
- Live log streaming through WebSockets
- Optional SQLite run persistence

## Folder Structure


## Running the Server

Install dependencies:
pip install -r requirements.txt

Start server:
uvicorn app.main:app --reload

## Example Workflow

Five step code review pipeline:
extract → check → detect → suggest

## API Endpoints

POST /graph/create  
POST /graph/run  
GET /graph/state/{run_id}  
WS  /ws/logs/{run_id}

## Improvements if given more time
- Looping support
- Parallel nodes
- Pluggable storage layers
- Retry logic
- Graph validation

