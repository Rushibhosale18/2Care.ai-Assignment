import time
from typing import Tuple

class TTSEngine:
    def synthesize(self, text: str, lang: str = "en") -> Tuple[bytes, float]:
        start = time.time()
        audio = b'\x00' * 1000 
        return audio, (time.time() - start) * 1000

tts_engine = TTSEngine()
