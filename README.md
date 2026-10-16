# Lost & Found - University Database Project Starter Template

A decoupled starter template designed specifically for a University Database Course project using **Microsoft SQL Server**.

---

## Architecture Stack & Configuration

- **Backend:** Python 3 + [FastAPI](https://fastapi.tiangolo.com/) + Raw [pymssql](https://pymssql.readthedocs.io/) driver for Microsoft SQL Server.
- **Frontend:** Decoupled [Svelte 5](https://svelte.dev/) Single Page Application initialized via [Vite](https://vitejs.dev/), styled with [Pico.css v2](https://picocss.com/) for classless/semantic HTML styling.
- **Authentication:** None. All endpoints are open and public for coursework simplicity.
- **CORS:** Pre-configured with permissive CORS (`allow_origins=["*"]`) so the Svelte frontend can communicate directly with the FastAPI backend without browser cross-origin errors.

---

## Database Philosophy (Critical Course Requirement)

1. **Explicit Raw T-SQL Only:** No ORMs (such as SQLAlchemy, SQLModel, or Peewee) are used. All database definitions (`CREATE TABLE`, constraints, indexes) and queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) are written as raw, explicit Transact-SQL (T-SQL) strings.
2. **Role of Pydantic:** Pydantic is used strictly as a **Request Body Data Transfer Object (DTO)** layer to validate incoming JSON payloads from the frontend. Pydantic fields are unpacked directly into parameterized raw SQL queries (`cursor.execute(sql, (param1, param2))`) to prevent SQL injection.
3. **Database Engine:** Microsoft SQL Server accessed via `pymssql` with dictionary cursor mapping (`as_dict=True`) for direct JSON response serialization.

---

## Project Directory Tree

```
LostAndFound/
├── .gitignore
├── README.md
├── backend/
│   ├── .env                       # Local DB environment variables (git-ignored)
│   ├── .env.example               # Template for DB connection settings
│   ├── requirements.txt
│   ├── venv/                      # Python virtual environment
│   └── app/
│       ├── __init__.py
│       ├── main.py                # FastAPI entrypoint with CORS & routers
│       ├── database.py            # Raw pymssql connection & table init skeleton
│       ├── schemas.py             # Pydantic DTO models stub
│       └── routes/
│           ├── __init__.py
│           ├── items.py           # Application domain routes stub
│           └── reference_logs.py  # [REFERENCE EXAMPLE] Raw T-SQL CRUD
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── app.css                # Imports @picocss/pico
        ├── main.js                # Svelte mount entrypoint
        ├── App.svelte             # Root layout
        └── lib/
            └── reference/
                └── ReferenceLog.svelte # [REFERENCE EXAMPLE] Svelte 5 + Pico.css + async fetch
```

---

## Prerequisites: Microsoft SQL Server Setup

You must have an accessible instance of Microsoft SQL Server (and a database named `LostAndFoundDB`).

### Option A: Using Docker (Recommended for Linux, macOS & Windows WSL)
Run MS SQL Server 2022 Express in Docker:
```bash
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YourStrong@Password" \
   -p 1433:1433 --name mssql-db -d \
   mcr.microsoft.com/mssql/server:2022-latest
```

Create the database using `sqlcmd`:
```bash
docker exec -it mssql-db /opt/mssql-tools18/bin/sqlcmd \
   -S localhost -U sa -P "YourStrong@Password" -C \
   -Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name='LostAndFoundDB') CREATE DATABASE LostAndFoundDB;"
```

### Option B: Native SQL Server (Windows)
1. Download and install **SQL Server 2022 Express** and **SQL Server Management Studio (SSMS)**.
2. Ensure **SQL Server and Windows Authentication mode** (Mixed Mode) is enabled.
3. In SSMS or `sqlcmd`, run:
   ```sql
   CREATE DATABASE LostAndFoundDB;
   ```

---

## Step-by-Step Setup Guides (Windows & Linux)

### 1. Backend Setup (Python 3 + FastAPI)

#### Linux (Ubuntu/Debian)
```bash
# 1. Navigate to backend directory
cd backend

# 2. Ensure Python 3 and venv are installed
sudo apt update && sudo apt install -y python3 python3-venv python3-pip

# 3. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install backend dependencies (FastAPI, Uvicorn, Pydantic, pymssql)
pip install -r requirements.txt

# 5. Configure environment variables (.env)
cp .env.example .env
# Edit .env with your SQL Server host, port, user, password, and database

# 6. Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```

#### Windows (PowerShell)
```powershell
# 1. Navigate to backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# (If execution of scripts is disabled, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Configure environment variables (.env)
Copy-Item .env.example .env
# Edit .env to match your SQL Server instance (e.g. localhost, port 1433, sa password)

# 5. Start the FastAPI development server
uvicorn app.main:app --reload --port 8000
```

- API Base URL: `http://localhost:8000`
- Interactive Swagger Documentation: `http://localhost:8000/docs`

---

### 2. Frontend Setup (JavaScript / Node.js + Svelte 5 + Pico.css)

#### Linux (Ubuntu/Debian)
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install Node.js & npm (if not already installed, Node.js 18+ or 20+ recommended)
# sudo apt install nodejs npm

# 3. Install dependencies (Vite, Svelte 5, Pico.css)
npm install

# 4. Start the local development server
npm run dev
```

#### Windows (PowerShell or Command Prompt)
```powershell
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the local development server
npm run dev
```

- Frontend App URL: `http://localhost:5173`

---

## Configuration Settings ([backend/.env](file:///home/pesterian/Documents/code/uni/LostAndFound/backend/.env))

```ini
MSSQL_SERVER=localhost
MSSQL_PORT=1433
MSSQL_USER=sa
MSSQL_PASSWORD=YourStrong@Password
MSSQL_DATABASE=LostAndFoundDB
```

---

## Isolated Reference Example (`SystemLog`)

An isolated, end-to-end example demonstrates the full MS SQL Server workflow without interfering with your team's upcoming ERD design.

### 1. Raw T-SQL Schema (`backend/app/routes/reference_logs.py`)
```python
def init_reference_table():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # T-SQL table with auto-incrementing identity primary key
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='system_logs' AND xtype='U')
                CREATE TABLE system_logs (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    message NVARCHAR(MAX) NOT NULL,
                    timestamp NVARCHAR(50) NOT NULL
                );
            """)
        conn.commit()
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
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT id, message, timestamp FROM system_logs ORDER BY id DESC;")
            rows = cursor.fetchall()
            return rows
    finally:
        conn.close()

@router.post("/", status_code=201)
def create_system_log(payload: SystemLogCreate):
    conn = get_db_connection()
    current_timestamp = datetime.now(timezone.utc).isoformat()
    try:
        with conn.cursor(as_dict=True) as cursor:
            # Parameterized query with OUTPUT inserted.id for MS SQL Server
            sql = """
                INSERT INTO system_logs (message, timestamp)
                OUTPUT inserted.id
                VALUES (%s, %s);
            """
            cursor.execute(sql, (payload.message, current_timestamp))
            row = cursor.fetchone()
            created_id = row["id"] if row else None
        conn.commit()
        return {"id": created_id, "message": payload.message, "timestamp": current_timestamp}
    finally:
        conn.close()
```

### 3. Svelte Component (`frontend/src/lib/reference/ReferenceLog.svelte`)
- Uses reactive two-way binding (`bind:value={newMessage}`).
- Native Svelte loops (`{#each logs as log (log.id)}`).
- Pure semantic HTML tags (`<article>`, `<form>`, `<input>`, `<table>`) styled automatically by **Pico.css**.
- Direct async `fetch()` calls to `http://localhost:8000/reference/logs/`.
