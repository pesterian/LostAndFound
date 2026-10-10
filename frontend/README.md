# Frontend Setup Guide / دليل إعداد الواجهة الأمامية

## English

### Prerequisites
- Node.js 20+
- npm 10+

### 1) Install dependencies
```bash
cd frontend
npm install
```

### 2) Configure backend URL
Copy the example file and adjust if needed:
```bash
cp .env.example .env
```
Default value:
```env
VITE_BACKEND_URL=http://localhost:8000
```

### 3) Start the development server
```bash
npm run dev
```
Vite will print a local URL (usually `http://localhost:5173`).

### 4) Verify frontend-backend communication
- Ensure backend is running on `http://localhost:8000`.
- Open the frontend in the browser.
- The health card should show loading first, then success or an error state.

### 5) Build for production
```bash
npm run build
```

### Stack notes
- Svelte + TypeScript app generated with Vite.
- Styling is configured with Tailwind CSS and DaisyUI.
- The app currently includes only a starter page and a backend health-check example.

---

## العربية

### المتطلبات المسبقة
- Node.js 20 أو أحدث
- npm 10 أو أحدث

### 1) تثبيت الاعتمادات
```bash
cd frontend
npm install
```

### 2) ضبط رابط الواجهة الخلفية
انسخ ملف المثال ثم عدّل القيمة عند الحاجة:
```bash
cp .env.example .env
```
القيمة الافتراضية:
```env
VITE_BACKEND_URL=http://localhost:8000
```

### 3) تشغيل خادم التطوير
```bash
npm run dev
```
سيعرض Vite رابط التشغيل المحلي (غالبًا `http://localhost:5173`).

### 4) التحقق من اتصال الواجهة الأمامية بالخلفية
- تأكد أن الواجهة الخلفية تعمل على `http://localhost:8000`.
- افتح الواجهة الأمامية في المتصفح.
- ستظهر حالة تحميل أولًا، ثم نجاح أو رسالة خطأ في بطاقة الصحة.

### 5) بناء نسخة الإنتاج
```bash
npm run build
```

### ملاحظات حول التقنيات
- التطبيق مبني بـ Svelte + TypeScript عبر Vite.
- التنسيق جاهز باستخدام Tailwind CSS و DaisyUI.
- المشروع يحتوي حاليًا على صفحة بداية ومثال اتصال بسيط مع نقطة الصحة فقط.
