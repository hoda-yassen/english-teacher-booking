// فاضي = نفس الدومين اللي شغال منه الموقع (الواجهة والسيرفر بيشتغلوا كخدمة واحدة بعد النشر)
// لو شغلتي الواجهة لوحدها (Live Server) وقت التطوير، غيّريها لـ "http://localhost:8000"
const API_BASE_URL = "";

// ------- نموذج الحجز -------
const bookingForm = document.getElementById("booking-form");
const bookingMessage = document.getElementById("booking-message");

bookingForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  bookingMessage.textContent = "";
  bookingMessage.className = "form-message";

  const appointmentValue = document.getElementById("booking-time").value;

  const payload = {
    name: document.getElementById("booking-name").value.trim(),
    email: document.getElementById("booking-email").value.trim(),
    whatsapp: document.getElementById("booking-whatsapp").value.trim(),
    service: document.getElementById("booking-service").value,
    details: document.getElementById("booking-details").value.trim(),
    appointment_time: new Date(appointmentValue).toISOString(),
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/bookings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "حدث خطأ أثناء إرسال الحجز");
    }

    bookingForm.reset();
    bookingMessage.textContent = "✅ تم استلام حجزك بنجاح! هيتم التواصل معاك قريبًا.";
    bookingMessage.classList.add("success");
  } catch (err) {
    bookingMessage.textContent = `⚠️ ${err.message}`;
    bookingMessage.classList.add("error");
  }
});

// ------- نموذج طلب الترجمة -------
const translationForm = document.getElementById("translation-form");
const translationMessage = document.getElementById("translation-message");

translationForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  translationMessage.textContent = "";
  translationMessage.className = "form-message";

  const formData = new FormData();
  formData.append("name", document.getElementById("translation-name").value.trim());
  formData.append("email", document.getElementById("translation-email").value.trim());
  formData.append("whatsapp", document.getElementById("translation-whatsapp").value.trim());
  formData.append("notes", document.getElementById("translation-notes").value.trim());
  formData.append("file", document.getElementById("translation-file").files[0]);

  try {
    const response = await fetch(`${API_BASE_URL}/api/translation-requests`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "حدث خطأ أثناء رفع الملف");
    }

    translationForm.reset();
    translationMessage.textContent = "✅ تم استلام طلب الترجمة بنجاح!";
    translationMessage.classList.add("success");
  } catch (err) {
    translationMessage.textContent = `⚠️ ${err.message}`;
    translationMessage.classList.add("error");
  }
});
