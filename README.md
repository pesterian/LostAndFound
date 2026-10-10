# Lost and Found Starter Repository

## English

### Purpose and current scope
This repository is a beginner-friendly monorepo starter for a university database course project (Lost and Found).

Current scope:
- Development setup for backend and frontend
- SQL-first project structure
- One simple end-to-end health-check integration

Out of scope for now:
- ERD design
- Domain database schema and queries
- Lost-and-found business features

### Technology stack
- **Backend:** Python, FastAPI, Pydantic, sqlite3, pytest
- **Frontend:** Svelte, TypeScript, Vite, Tailwind CSS, DaisyUI, npm
- **Database:** SQLite with handwritten SQL files under `backend/sql/`

### Repository structure
```text
lost-and-found/
├── backend/
│   ├── app/
│   ├── sql/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── .gitignore
└── README.md
```

### Setup guides
- Backend guide: [backend/README.md](backend/README.md)
- Frontend guide: [frontend/README.md](frontend/README.md)

> The team will design the ERD, final SQL schema, and application features in later project phases.

---

## العربية

### الهدف والنطاق الحالي
هذا المستودع هو نقطة بداية مبسطة (Monorepo) لمشروع مادة قواعد البيانات الجامعي (Lost and Found).

النطاق الحالي يشمل:
- تجهيز بيئة التطوير للواجهة الخلفية والأمامية
- تنظيم المشروع بحيث تكون SQL واضحة ومركزية
- مثال اتصال بسيط من الواجهة الأمامية إلى الخلفية عبر نقطة الصحة

وخارج النطاق حاليًا:
- تصميم ERD
- بناء مخطط قاعدة البيانات النهائي واستعلامات المجال
- تنفيذ خصائص نظام المفقودات والموجودات

### التقنيات المستخدمة
- **الخلفية:** Python و FastAPI و Pydantic و sqlite3 و pytest
- **الأمامية:** Svelte و TypeScript و Vite و Tailwind CSS و DaisyUI و npm
- **قاعدة البيانات:** SQLite مع ملفات SQL مكتوبة يدويًا داخل `backend/sql/`

### هيكل المستودع
```text
lost-and-found/
├── backend/
│   ├── app/
│   ├── sql/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── .gitignore
└── README.md
```

### أدلة الإعداد
- دليل الواجهة الخلفية: [backend/README.md](backend/README.md)
- دليل الواجهة الأمامية: [frontend/README.md](frontend/README.md)

> سيتم لاحقًا تصميم ERD وبناء مخطط قاعدة البيانات النهائي وتفاصيل خصائص التطبيق بواسطة الفريق.
