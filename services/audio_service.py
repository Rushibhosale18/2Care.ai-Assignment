import os
import time
from typing import Tuple

class AudioService:
    def __init__(self):
        self.counter = 0

    def speech_to_text(self, audio_file_path: str) -> Tuple[str, float]:
        start_time = time.time()
        
        # ADVANCED DEMO CYCLE
        if self.counter == 0:
            transcript = "I want to book an appointment with a cardiologist"
        elif self.counter == 1:
            transcript = "okay confirm this slot"
        elif self.counter == 2:
            transcript = "Everything looks perfect, thank you!"
        else:
            transcript = "Actually, please cancel the appointment"
            
        self.counter = (self.counter + 1) % 4 # Now a 4-step cycle
        latency = (time.time() - start_time) * 1000
        return transcript, latency

    def text_to_speech(self, text: str, language: str = "en") -> Tuple[bytes, float]:
        start_time = time.time()
        audio_content = b'\x00' * 1000 
        latency = (time.time() - start_time) * 1000
        return audio_content, latency

audio_service = AudioService()
