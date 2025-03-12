import os
import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Get the user's message from the query parameters.
    message = websocket.query_params.get("message", "")
    
    # Create your agent.
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )
    
    # Start the streaming run using your agent.
    result = Runner.run_streamed(agent, input=message)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await websocket.send_text(event.data.delta)
    await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)