import time
from typing import Dict, Any, List

class ClinicalReasoning:
    def process(self, text: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
        start = time.time()
        msg = text.lower()
        
        # Check if we are already in the "Booking" phase
        was_offered = any("available slots" in (m.get("content", "").lower()) for m in history)
        
        if "cancel" in msg:
            ans = "I have successfully canceled your appointment. Is there anything else?"
        elif ("confirm" in msg or "10" in msg) and was_offered:
             ans = "Excellent choice. I have recorded and confirmed your appointment with Dr. Amit Sharma for 10:30 AM. You are all set!"
        elif "cardiologist" in msg or "doctor" in msg:
            ans = "I found Dr. Amit Sharma (Cardiologist). Available slots: 10:30 AM, 2:00 PM, and 4:30 PM. Shall I book 10:30 AM for you?"
        else:
            ans = "Welcome to 2Care.ai Elite. I can check doctor schedules for you. Would you like to see a Cardiologist?"
        
        return {
            "text": ans,
            "latency": (time.time() - start) * 1000
        }

clinical_reasoning = ClinicalReasoning()
