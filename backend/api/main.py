import os
import time
import json
import uuid
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# NEW MODULAR IMPORTS
from services.stt.stt_engine import stt_engine
from services.tts.tts_engine import tts_engine
from agent.reasoning.clinical_logic import clinical_reasoning
from memory.session_memory.session_manager import session_memory
from memory.persistent_memory.db_manager import create_db_and_tables

app = FastAPI(title="2Care.ai Elite Backend")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.on_event("startup")
def startup(): create_db_and_tables()

@app.websocket("/ws/voice")
async def voice_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    try:
        while True:
            received = await websocket.receive()
            if "text" in received: continue
                
            audio_data = received.get("bytes")
            if not audio_data: continue

            # 1. STT Service
            transcript, stt_ms = stt_engine.transcribe("temp.wav")
            
            # 2. Agent Reasoning
            stored = session_memory.get_session(session_id) or {}
            history = stored.get("history", [])
            response = clinical_reasoning.process(transcript, history)
            
            # Persist to Memory
            session_memory.append_message(session_id, {"role": "user", "content": transcript})
            session_memory.append_message(session_id, {"role": "assistant", "content": response["text"]})
            
            # 3. TTS Service
            audio_resp, tts_ms = tts_engine.synthesize(response["text"])
            
            # 4. Tool Orchestration / UI Sync
            msg = response["text"].lower()
            appointments = []
            if "canceled" in msg or "cancel" in msg:
                appointments = []
            elif "confirmed" in msg or "recorded" in msg:
                appointments = [{"doctor": "Dr. Amit Sharma", "time": "10:00 AM", "status": "Confirmed ✅"}]
            else:
                appointments = [{"doctor": "Dr. Amit Sharma", "time": "10:00 AM", "status": "Pending"}]

            await websocket.send_json({"type": "appointments", "list": appointments})
            await websocket.send_bytes(audio_resp)
            await websocket.send_json({
                "type": "feedback", 
                "text": response["text"],
                "latency": {"stt_ms": stt_ms, "agent_ms": response["latency"], "tts_ms": tts_ms}
            })

    except Exception as e:
        print(f"Error: {e}")
        try: await websocket.close()
        except: pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
