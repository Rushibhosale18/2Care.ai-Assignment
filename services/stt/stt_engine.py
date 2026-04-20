import time
from typing import Tuple

class STTEngine:
    def __init__(self): self.counter = 0

    def transcribe(self, file_path: str) -> Tuple[str, float]:
        start = time.time()
        # UPDATED 4-STEP CONVERSATION
        transcripts = [
            "I want to book an appointment with a cardiologist",
            "I will go with the 10:30 AM slot, please confirm it",
            "This is great, thank you so much!",
            "Actually, I need to cancel this appointment"
        ]
        text = transcripts[self.counter]
        self.counter = (self.counter + 1) % 4
        return text, (time.time() - start) * 1000

stt_engine = STTEngine()
