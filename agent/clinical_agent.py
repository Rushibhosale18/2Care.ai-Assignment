import time
from typing import Dict, Any, List

class ClinicalAgent:
    def process_request(self, text: str, history: List[Dict[str, str]], forced_lang: str = "English") -> Dict[str, Any]:
        start_time = time.time()
        msg = text.lower()
        
        # VERY SIMPLE LOGIC FOR DEMO
        if "cancel" in msg:
            final_text = "I have successfully canceled your appointment. Goodbye!"
        elif "confirm" in msg or "am" in msg:
             final_text = "Excellent. I have recorded and confirmed your appointment with Dr. Sharma for 10 AM. You are all set!"
        elif "cardiologist" in msg:
            final_text = "I found Dr. Amit Sharma. He is available at 10 AM. Should I book it for you?"
        else:
            final_text = "Welcome to 2Care.ai. I can help you book an appointment. Would you like a Cardiologist?"
        
        return {
            "text": final_text,
            "language": forced_lang,
            "latency": (time.time() - start_time) * 1000
        }
