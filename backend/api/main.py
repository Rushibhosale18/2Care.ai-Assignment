import os
import time
import json
import uuid
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

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

            transcript, stt_ms = stt_engine.transcribe("temp.wav")
            
            stored = session_memory.get_session(session_id) or {}
            history = stored.get("history", [])
            response = clinical_reasoning.process(transcript, history)
            
            session_memory.append_message(session_id, {"role": "user", "content": transcript})
            session_memory.append_message(session_id, {"role": "assistant", "content": response["text"]})
            
            audio_resp, tts_ms = tts_engine.synthesize(response["text"])
            
            # UI LOGIC REFINDED
            msg = response["text"].lower()
            appointments = []
            
            if "cancel" in msg:
                appointments = []
            elif "confirmed" in msg or "recorded" in msg:
                appointments = [{"doctor": "Dr. Amit Sharma", "time": "10:30 AM", "status": "Confirmed ✅"}]
            elif "slots" in msg:
                appointments = [{"doctor": "Dr. Amit Sharma", "time": "10:30 AM | 2:00 PM | 4:30 PM", "status": "Select a Slot"}]
            else:
                appointments = [] # No card until they ask for a doctor

            await websocket.send_json({"type": "appointments", "list": appointments})
            await websocket.send_bytes(audio_resp)
            await websocket.send_json({
                "type": "feedback", 
                "text": response["text"],
                "latency": {"stt_ms": stt_ms, "agent_ms": response["latency"], "tts_ms": tts_ms}
            })

    except Exception as e:
        print(f"Error: {e}"); await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
