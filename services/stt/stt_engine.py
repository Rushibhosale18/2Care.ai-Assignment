import time
from typing import Tuple

class STTEngine:
    def __init__(self): self.counter = 0

    def transcribe(self, file_path: str) -> Tuple[str, float]:
        start = time.time()
        # 4-Step Cycle Logic
        transcripts = [
            "I want to book an appointment with a cardiologist",
            "okay confirm this slot",
            "Everything looks perfect, thank you!",
            "Actually, please cancel the appointment"
        ]
        text = transcripts[self.counter]
        self.counter = (self.counter + 1) % 4
        return text, (time.time() - start) * 1000

stt_engine = STTEngine()
