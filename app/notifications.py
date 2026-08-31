import os
from html import escape

import httpx

RESEND_API_URL = "https://api.resend.com/emails"
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM = os.getenv("RESEND_FROM", "onboarding@resend.dev")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "ahmedawadallah108@gmail.com")


def _send(subject: str, body_html: str) -> None:
    # لو الـ API key مش متظبط (مثلاً وقت التطوير المحلي)، تجاهل الإرسال بهدوء
    if not RESEND_API_KEY:
        return
    try:
        httpx.post(
            RESEND_API_URL,
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": RESEND_FROM,
                "to": [NOTIFY_EMAIL],
                "subject": subject,
                "html": body_html,
            },
            timeout=10,
        )
    except httpx.HTTPError:
        pass


def notify_new_booking(booking) -> None:
    _send(
        "حجز جديد على الموقع",
        f"<h2>حجز جديد</h2>"
        f"<p><b>الاسم:</b> {escape(booking.name)}</p>"
        f"<p><b>البريد الإلكتروني:</b> {escape(booking.email)}</p>"
        f"<p><b>واتساب:</b> {escape(booking.whatsapp)}</p>"
        f"<p><b>الخدمة:</b> {escape(booking.service)}</p>"
        f"<p><b>تفاصيل الطلب:</b> {escape(booking.details)}</p>"
        f"<p><b>الميعاد المطلوب:</b> {booking.appointment_time}</p>",
    )


def notify_new_translation_request(request) -> None:
    _send(
        "طلب ترجمة جديد على الموقع",
        f"<h2>طلب ترجمة جديد</h2>"
        f"<p><b>الاسم:</b> {escape(request.name)}</p>"
        f"<p><b>البريد الإلكتروني:</b> {escape(request.email)}</p>"
        f"<p><b>واتساب:</b> {escape(request.whatsapp)}</p>"
        f"<p><b>ملاحظات:</b> {escape(request.notes or '-')}</p>"
        f"<p><b>اسم الملف:</b> {escape(request.original_filename)}</p>",
    )
