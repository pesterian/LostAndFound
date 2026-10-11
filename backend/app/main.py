from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.routes import items
from app.routes.reference_logs import router as reference_router, init_reference_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize core database (stubbed) and the reference example table on startup
    init_db()
    init_reference_table()
    yield


app = FastAPI(
    title="Lost and Found API",
    description="University Database Project API (Raw SQL + SQLite)",
    lifespan=lifespan,
)

# -------------------------------------------------------------
# Comprehensive CORS Configuration
# Ensures the decoupled Svelte SPA can communicate without CORS issues
# -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Application Routers
app.include_router(items.router)

# Reference Example Router (mock isolated concept for team onboarding)
app.include_router(reference_router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Lost and Found backend is running"}

