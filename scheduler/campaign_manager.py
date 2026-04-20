import asyncio
from services.audio_service import audio_service
from memory.db_manager import Session, select, Patient, Appointment
import datetime

class OutboundCampaignManager:
    async def run_reminder_campaign(self):
        print("Starting outbound campaign: Appointment Reminders...")
        
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        
        patients_to_remind = [
            {"name": "Rushi", "phone": "+919309246989", "doctor": "Dr. Sharma", "time": "10:30 AM"}
        ]
        
        for p in patients_to_remind:
            message = f"Hello {p['name']}, this is a reminder call from 2Care AI. You have an appointment with {p['doctor']} tomorrow at {p['time']}. Would you like to confirm or reschedule?"
            
            print(f"Calling {p['phone']}...")
            print(f"Agent says: {message}")
            
            audio_greeting, _ = audio_service.text_to_speech(message)
            
            print(f"Reminder audio generated ({len(audio_greeting)} bytes)")

if __name__ == "__main__":
    campaign = OutboundCampaignManager()
    asyncio.run(campaign.run_reminder_campaign())
