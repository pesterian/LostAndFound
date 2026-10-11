# Lost & Found - University Database Project Starter Template

A decoupled starter template designed specifically for a University Database Course project.

---

## Architecture Stack & Configuration

- **Backend:** Python 3 + [FastAPI](https://fastapi.tiangolo.com/) + Native Python `sqlite3` driver.
- **Frontend:** Decoupled [Svelte 5](https://svelte.dev/) Single Page Application initialized via [Vite](https://vitejs.dev/), styled with [Pico.css v2](https://picocss.com/) for classless/semantic HTML styling.
- **Authentication:** None. All endpoints are open and public for coursework simplicity.
- **CORS:** Pre-configured with permissive CORS (`allow_origins=["*"]`) so the Svelte frontend can communicate directly with the FastAPI backend without browser cross-origin errors.

---

## Database Philosophy (Critical Course Requirement)

1. **Explicit Raw SQL Only:** No ORMs (such as SQLAlchemy, SQLModel, or Peewee) are used. All database definitions (`CREATE TABLE`, indexes) and queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) are written as raw, explicit SQL strings.
2. **Role of Pydantic:** Pydantic is used strictly as a **Request Body Data Transfer Object (DTO)** layer to validate incoming JSON payloads from the frontend. Pydantic fields are unpacked directly into parameterized raw SQL queries (`cursor.execute(sql, (param1, param2))`) to prevent SQL injection.
3. **Database Engine:** Pure Python `sqlite3` standard library with `sqlite3.Row` row factory for clean dict/JSON serialization and `PRAGMA foreign_keys = ON;`.

---

## Project Directory Tree

```
LostAndFound/
├── .gitignore
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── venv/                      (Created via setup guide)
│   ├── lost_and_found.db          (Generated SQLite database file)
│   └── app/
│       ├── __init__.py
│       ├── main.py                (FastAPI entrypoint with CORS & routers)
│       ├── database.py            (Raw sqlite3 connection & table init skeleton)
│       ├── schemas.py             (Pydantic DTO models stub)
│       └── routes/
│           ├── __init__.py
│           ├── items.py           (Application domain routes stub)
│           └── reference_logs.py  (Isolated Reference Example: raw SQL CRUD)
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── app.css                (Imports @picocss/pico)
        ├── main.js                (Svelte mount entrypoint)
        ├── App.svelte             (Root layout)
        └── lib/
            └── reference/
                └── ReferenceLog.svelte (Isolated Reference Example component)
```

---

## Step-by-Step Setup Guides

### 1. Backend Setup (Terminal)

From the project root:

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create a Python 3 virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate
# (On Windows PowerShell: .\venv\Scripts\Activate.ps1)

# 4. Install backend dependencies (FastAPI, Uvicorn, Pydantic)
pip install -r requirements.txt

# 5. Start the development server with auto-reload
uvicorn app.main:app --reload --port 8000
```

- API Base URL: `http://localhost:8000`
- Interactive Swagger Documentation: `http://localhost:8000/docs`

---

### 2. Frontend Setup (Terminal)

Open a separate terminal window and navigate from the project root:

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies (including Vite, Svelte, and Pico.css)
npm install

# 3. Start the local development server
npm run dev
```

- Frontend App URL: `http://localhost:5173`

---

## Isolated Reference Example (`SystemLog`)

An isolated, end-to-end example is provided to demonstrate the full workflow without polluting your upcoming ERD logic.

### 1. Raw SQL Schema (`backend/app/routes/reference_logs.py`)
```python
def init_reference_table():
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                );
            """)
    finally:
        conn.close()
```

### 2. Route Handler with DTO & Parameterized Raw SQL (`backend/app/routes/reference_logs.py`)
```python
class SystemLogCreate(BaseModel):
    message: str = Field(..., min_length=1)

@router.get("/")
def get_system_logs():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, message, timestamp FROM system_logs ORDER BY id DESC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@router.post("/", status_code=201)
def create_system_log(payload: SystemLogCreate):
    conn = get_db_connection()
    current_timestamp = datetime.utcnow().isoformat() + "Z"
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO system_logs (message, timestamp) VALUES (?, ?);",
                (payload.message, current_timestamp)
            )
            created_id = cursor.lastrowid
        return {"id": created_id, "message": payload.message, "timestamp": current_timestamp}
    finally:
        conn.close()
```

### 3. Svelte Component (`frontend/src/lib/reference/ReferenceLog.svelte`)
- Uses reactive two-way binding (`bind:value={newMessage}`).
- Native Svelte loops (`{#each logs as log (log.id)}`).
- Pure semantic HTML tags (`<article>`, `<form>`, `<input>`, `<table>`) styled automatically by **Pico.css**.
- Direct async `fetch()` calls to `http://localhost:8000/reference/logs/`.
