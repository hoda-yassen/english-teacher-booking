import os
import uuid

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine
from .notifications import notify_new_booking, notify_new_translation_request

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 ميجابايت
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}

app = FastAPI(title="English Teacher & Translator Booking API", version="1.0.0")

# CORS: يسمح للواجهة الأمامية (frontend) بمناداة الـ API من دومين مختلف
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/bookings", response_model=schemas.BookingOut, status_code=201)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = models.Booking(
        name=booking.name,
        email=booking.email,
        whatsapp=booking.whatsapp,
        service=booking.service.value,
        details=booking.details,
        appointment_time=booking.appointment_time,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    notify_new_booking(db_booking)
    return db_booking


@app.post(
    "/api/translation-requests",
    response_model=schemas.TranslationRequestOut,
    status_code=201,
)
async def create_translation_request(
    name: str = Form(..., min_length=2, max_length=120),
    email: str = Form(...),
    whatsapp: str = Form(..., min_length=6, max_length=30),
    notes: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        email = TypeAdapter(EmailStr).validate_python(email)
    except ValidationError:
        raise HTTPException(status_code=422, detail="البريد الإلكتروني غير صالح")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="نوع الملف غير مدعوم. الأنواع المسموحة: PDF, DOC, DOCX, TXT",
        )

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail="حجم الملف أكبر من الحد المسموح (10 ميجابايت)",
        )

    stored_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, stored_filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    db_request = models.TranslationRequest(
        name=name,
        email=email,
        whatsapp=whatsapp,
        notes=notes,
        original_filename=file.filename,
        stored_filename=stored_filename,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    notify_new_translation_request(db_request)
    return db_request


# لازم يتحط بعد كل الـ API routes: الملفات الثابتة (الواجهة الأمامية) بتتقدَّم من نفس السيرفر
# عشان النشر يبقى خدمة واحدة على Railway، من غير الحاجة لإعداد CORS بين دومينين مختلفين
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
