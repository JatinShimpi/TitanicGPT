from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import os

from backend.agent import setup_agent, process_query

app = FastAPI(title="TitanicGPT Backend")

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_instance = None

class ChatRequest(BaseModel):
    query: str
    api_key: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    global agent_instance
    
    if not request.api_key:
        raise HTTPException(status_code=400, detail="API Key is required")
        
    try:
        temp_agent = setup_agent(request.api_key)
        result = process_query(temp_agent, request.query)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
