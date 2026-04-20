from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str = Field(index=True, unique=True)
    preferred_language: str = "English"

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int
    doctor_name: str
    specialty: str
    appointment_time: datetime
    status: str = "booked"  

class DoctorSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int
    doctor_name: str
    specialty: str
    available_time: datetime
    is_booked: bool = False

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def check_availability(specialty: str, date_str: str):
    with Session(engine) as session:
        statement = select(DoctorSchedule).where(
            DoctorSchedule.specialty == specialty,
            DoctorSchedule.is_booked == False
        )
        results = session.exec(statement).all()
        return results

def book_appointment(patient_id: int, doctor_id: int, time: datetime):
    with Session(engine) as session:
        slot = session.exec(select(DoctorSchedule).where(
            DoctorSchedule.doctor_id == doctor_id,
            DoctorSchedule.available_time == time,
            DoctorSchedule.is_booked == False
        )).first()
        
        if not slot:
            return None
        
        slot.is_booked = True
        session.add(slot)
        
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            doctor_name=slot.doctor_name,
            specialty=slot.specialty,
            appointment_time=time
        )
        session.add(appointment)
        session.commit()
        session.refresh(appointment)
        return appointment
