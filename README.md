# English Teacher & Translator — Booking Platform

## التشغيل محليًا بدون Docker (SQLite)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

الـ API هيشتغل على `http://localhost:8000` وقاعدة بيانات SQLite هتتعمل تلقائي (`app.db`).

## التشغيل عبر Docker (PostgreSQL)

```bash
docker-compose up --build
```

- الـ API: `http://localhost:8000`
- قاعدة البيانات: `localhost:5432`
- ملفات الترجمة المرفوعة بتتحفظ في مجلد `uploads/` على جهازك.

## الواجهة الأمامية

افتح `frontend/index.html` مباشرة في المتصفح (أو عبر Live Server)، وتأكد إن الـ API شغال على نفس العنوان المكتوب في `frontend/booking.js` (`API_BASE_URL`).

## Endpoints

| Method | Path                        | الوظيفة                          |
|--------|-----------------------------|-----------------------------------|
| GET    | /api/health                 | فحص إن السيرفر شغال               |
| POST   | /api/bookings                | حجز درس/خدمة                     |
| POST   | /api/translation-requests    | إرسال طلب ترجمة + رفع ملف         |

توثيق تفاعلي تلقائي: `http://localhost:8000/docs`

## الخطوة القادمة

لوحة تحكم (Admin Dashboard) بكلمة سر لعرض الحجوزات وطلبات الترجمة — هتتبني في مرحلة لاحقة.
