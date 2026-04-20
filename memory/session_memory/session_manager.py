import json

class SessionMemory:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str):
        return self.sessions.get(session_id, {"history": []})

    def append_message(self, session_id: str, message: dict):
        if session_id not in self.sessions:
            self.sessions[session_id] = {"history": []}
        self.sessions[session_id]["history"].append(message)

    def update_session_state(self, session_id: str, state: dict):
        if session_id not in self.sessions:
            self.sessions[session_id] = {"history": []}
        self.sessions[session_id].update(state)

session_memory = SessionMemory()
