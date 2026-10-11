"""
REFERENCE EXAMPLE: Isolated End-to-End SystemLog Implementation
This module demonstrates:
1. Raw SQL table definition (CREATE TABLE).
2. Pydantic DTO model for parsing JSON request bodies.
3. Raw SQL write (INSERT) with parameterized queries.
4. Raw SQL read (SELECT) returning pure JSON lists.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import sqlite3
from typing import List
from datetime import datetime

from app.database import get_db_connection

router = APIRouter(prefix="/reference/logs", tags=["reference-example"])


# --- 1. Raw SQL Schema Initialization for Reference Example ---
def init_reference_table():
    """Initializes the mock SystemLog table with explicit raw SQL."""
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


# --- 2. Pydantic DTO (Request Body Parser Only) ---
class SystemLogCreate(BaseModel):
    message: str = Field(..., min_length=1, description="Log message text")


# --- 3. Route Handlers Using Explicit Raw SQL ---
@router.get("/")
def get_system_logs():
    """Fetches all system logs using a raw SQL SELECT query."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Raw SQL query
        cursor.execute("SELECT id, message, timestamp FROM system_logs ORDER BY id DESC;")
        rows = cursor.fetchall()
        # Convert sqlite3.Row objects to standard Python dicts for pure JSON serialization
        return [dict(row) for row in rows]
    finally:
        conn.close()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_system_log(payload: SystemLogCreate):
    """
    Inserts a new system log using raw SQL parameterized INSERT.
    Unpacks Pydantic DTO into raw SQL parameters to prevent SQL injection.
    """
    conn = get_db_connection()
    current_timestamp = datetime.utcnow().isoformat() + "Z"
    try:
        with conn:
            cursor = conn.cursor()
            # Raw SQL parameterized query - DO NOT concatenate user input into SQL strings!
            cursor.execute(
                "INSERT INTO system_logs (message, timestamp) VALUES (?, ?);",
                (payload.message, current_timestamp)
            )
            created_id = cursor.lastrowid
        
        return {
            "id": created_id,
            "message": payload.message,
            "timestamp": current_timestamp
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

