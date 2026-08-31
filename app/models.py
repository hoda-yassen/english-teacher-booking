from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from .database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    whatsapp = Column(String(30), nullable=False)
    service = Column(String(80), nullable=False)
    details = Column(Text, nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TranslationRequest(Base):
    __tablename__ = "translation_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    whatsapp = Column(String(30), nullable=False)
    notes = Column(Text, nullable=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
