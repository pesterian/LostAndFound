# Backend Setup Guide / دليل إعداد الواجهة الخلفية

## English

### Prerequisites
- Python 3.11+ recommended
- Linux shell (examples below use bash)

### 1) Create and activate a virtual environment
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Run FastAPI (Uvicorn)
```bash
uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000`.

### 4) Test the health endpoint
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{"status":"ok"}
```

### 5) Run tests
```bash
pytest
```

### SQL directory layout
- `sql/schema.sql`: canonical SQLite schema file (to be filled after ERD is finalized).
- `sql/queries/`: handwritten SQL query files, grouped by feature as the project grows.

### SQLite connection infrastructure
- Reusable connection helper: `app/db/connection.py`.
- It uses Python's built-in `sqlite3` module.
- Every opened connection enables foreign keys with `PRAGMA foreign_keys = ON`.
- Future SQL operations should use parameterized statements (for example with `?` placeholders).

> Note: This starter does **not** auto-create domain tables. Add initialization only after the team completes the ERD and writes SQL in `sql/schema.sql`.

---

## العربية

### المتطلبات المسبقة
- يُفضَّل استخدام Python 3.11 أو أحدث
- بيئة سطر أوامر على لينكس (الأمثلة التالية باستخدام bash)

### 1) إنشاء وتفعيل بيئة افتراضية
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

### 2) تثبيت الاعتمادات
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) تشغيل FastAPI عبر Uvicorn
```bash
uvicorn app.main:app --reload
```
سيعمل الخادم على `http://localhost:8000`.

### 4) اختبار نقطة الصحة
```bash
curl http://localhost:8000/health
```
الاستجابة المتوقعة:
```json
{"status":"ok"}
```

### 5) تشغيل الاختبارات
```bash
pytest
```

### بنية مجلد SQL
- `sql/schema.sql`: الملف الأساسي لمخطط SQLite (سيتم استكماله بعد اعتماد ERD).
- `sql/queries/`: ملفات استعلامات SQL المكتوبة يدويًا، ويتم تنظيمها حسب الميزة لاحقًا.

### بنية الاتصال بـ SQLite
- ملف الاتصال القابل لإعادة الاستخدام: `app/db/connection.py`.
- يعتمد على مكتبة `sqlite3` المدمجة في بايثون.
- كل اتصال جديد يفعّل العلاقات المرجعية عبر `PRAGMA foreign_keys = ON`.
- عند إضافة استعلامات مستقبلًا، استخدموا استعلامات مُعلّمة بمعاملات (`?`) لتجنّب المشاكل الأمنية.

> ملاحظة: هذا المشروع الابتدائي لا ينشئ جداول المجال تلقائيًا. أضيفوا تهيئة قاعدة البيانات فقط بعد إنهاء ERD وكتابة SQL داخل `sql/schema.sql`.
