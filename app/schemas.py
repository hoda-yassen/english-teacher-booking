from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ServiceType(str, Enum):
    private_lesson = "private_lesson"        # حصة خصوصي لغة إنجليزية
    exam_prep = "exam_prep"                   # تحضير لاختبارات (IELTS/TOEFL)
    business_english = "business_english"     # إنجليزي أعمال
    interpretation = "interpretation"         # ترجمة فورية
    document_translation = "document_translation"  # ترجمة تحريرية


class BookingCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    service: ServiceType
    appointment_time: datetime


class BookingOut(BookingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class TranslationRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    notes: Optional[str] = None
    original_filename: str
    created_at: datetime
