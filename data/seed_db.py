from sqlmodel import Session
from memory.db_manager import engine, Patient, DoctorSchedule, create_db_and_tables
from datetime import datetime, timedelta

def populate_test_data():
    create_db_and_tables()
    
    with Session(engine) as session:
        if session.query(Patient).first():
            print("Database already populated.")
            return

        doctors = [
            ("Dr. Amit Sharma", "Cardiologist"),
            ("Dr. Priya Iyer", "Dermatologist"),
            ("Dr. Venkat Raman", "General Physician")
        ]
        
        now = datetime.now()
        for i in range(1, 4):
            for name, spec in doctors:
                slot_time = (now + timedelta(days=i)).replace(hour=10, minute=0, second=0, microsecond=0)
                session.add(DoctorSchedule(doctor_id=100+i, doctor_name=name, specialty=spec, available_time=slot_time))
                session.add(DoctorSchedule(doctor_id=100+i, doctor_name=name, specialty=spec, available_time=slot_time + timedelta(hours=4)))

        session.add(Patient(name="Test User", phone="+919000000000", preferred_language="English"))
        
        session.commit()
        print("Test data populated successfully.")

if __name__ == "__main__":
    populate_test_data()
