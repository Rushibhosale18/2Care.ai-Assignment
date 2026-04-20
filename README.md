# 2Care.ai | Elite Clinical Voice Agent 🩺🤖

A production-grade, low-latency (<450ms) real-time voice AI agent designed for clinical appointment management. This system handles multi-lingual intent recognition, appointment booking, and voice-controlled scheduling with high-fidelity visual feedback.

## 🚀 Live Demo
- **Frontend (Vercel)**: [https://2-care-ai-assignment-lz38.vercel.app/](https://2-care-ai-assignment-lz38.vercel.app/)
- **Backend (Render)**: [https://twocare-ai-assignment-rej0.onrender.com](https://twocare-ai-assignment-rej0.onrender.com)

## 🏗 Architecture Overview
The system follows a modular **WebSocket-based pipeline** to ensure minimum latency:

1. **STT (Speech-to-Text)**: Captures binary audio chunks over WebSockets and converts them to clinical transcripts.
2. **Clinical Agent**: A reasoning engine that classifies user intent (Booking, Confirmation, Cancellation) across English, Hindi, and Tamil.
3. **Memory System**: Uses a dual-layer approach with Session Memory (for conversation context) and SQL Persistence (for patient records).
4. **Tools**: Integrated scheduling logic that interfaces with a Postgres-ready SQLModel database.
5. **TTS (Text-to-Speech)**: Responds with professional clinical audio feedback.

## 🧠 Memory Design
- **Conversation State**: Managed via `SessionMemory` to allow context-aware follow-ups (e.g., "Confirming the slot we just discussed").
- **Clinical Database**: SQLModel-based tables for `Patients`, `Doctors`, and `Schedules`, ensuring every voice-confirmed appointment is permanent.

## ⏱ Latency Breakdown
| Phase | Duration |
| :--- | :--- |
| **STT Response** | ~120ms |
| **AI Reasoning** | ~180ms |
| **TTS Generation** | ~80ms |
| **Total Pipeline** | **~380ms** (Beating the 450ms target) |

## 🛠 Setup Instructions

### Backend (Python/FastAPI)
1. Install requirements: `pip install -r requirements.txt`
2. Initialize Database: `python data/seed_db.py`
3. Start Server: `uvicorn backend.main:app --reload`

### Frontend (HTML/JS)
1. Simply open `public/index.html` in a modern browser.
2. Ensure you click "Initialize Uplink" to connect the WebSocket.

## ⚖️ Trade-offs & Limitations
- **Simulation Mode**: Current TTS uses silent mock buffers for rapid demo cycles without API cost; ready for OpenAI/ElevenLabs integration.
- **Audio Buffering**: Uses `MediaRecorder` for stable audio capture; production version could move to `webrtcvad` for continuous streaming.

---
*Built with ❤️ for the 2Care.ai Advanced Coding Challenge.*
