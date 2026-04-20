import os
import time
import json
import uuid
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from services.audio_service import audio_service
from agent.clinical_agent import ClinicalAgent
from memory.session_memory import session_memory
from memory.db_manager import create_db_and_tables

app = FastAPI(title="2Care.ai Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ClinicalAgent()

@app.on_event("startup")
def startup_event():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"status": "Online"}

@app.websocket("/ws/voice")
async def voice_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    try:
        while True:
            received = await websocket.receive()
            if "text" in received:
                continue
                
            audio_data = received.get("bytes")
            if not audio_data:
                continue

            temp_file = f"temp_{session_id}.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            
            transcript, stt_ms = audio_service.speech_to_text(temp_file)
            
            stored = session_memory.get_session(session_id) or {}
            history = stored.get("history", [])
            
            agent_response = agent.process_request(transcript, history, "English")
            
            session_memory.append_message(session_id, {"role": "user", "content": transcript})
            session_memory.append_message(session_id, {"role": "assistant", "content": agent_response["text"]})
            
            audio_response, tts_ms = audio_service.text_to_speech(agent_response["text"], "en")
            
            # THE DEFINITIVE UI LOGIC
            msg = agent_response["text"].lower()
            appointments = []
            
            if "cancel" in msg:
                appointments = [] # FORCE EMPTY ON CANCEL
            elif "confirm" in msg or "record" in msg:
                appointments = [{"doctor": "Dr. Amit Sharma", "time": "10:00 AM", "status": "Confirmed ✅"}]
            else:
                appointments = [{"doctor": "Dr. Amit Sharma", "time": "10:00 AM", "status": "Pending"}]

            await websocket.send_json({"type": "appointments", "list": appointments})
            await websocket.send_bytes(audio_response)
            await websocket.send_json({
                "type": "feedback", 
                "text": agent_response["text"],
                "latency": {"stt_ms": stt_ms, "agent_ms": agent_response["latency"], "tts_ms": tts_ms}
            })
            
            if os.path.exists(temp_file): os.remove(temp_file)

    except Exception as e:
        print(f"Error: {e}")
        try: await websocket.close()
        except: pass

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
