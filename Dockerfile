FROM python:3.11-slim

WORKDIR /app

# تثبيت المكتبات أولاً عشان الاستفادة من Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# المنفذ اللي هيشتغل عليه تطبيق FastAPI جوه الكونتينر
EXPOSE 8000

# للتشغيل المحلي فقط: docker build -t teacher-booking-api .  ثم  docker run -p 8000:8000 teacher-booking-api
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
