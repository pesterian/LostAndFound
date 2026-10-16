"""
REFERENCE EXAMPLE: Isolated End-to-End SystemLog Implementation for Microsoft SQL Server
This module demonstrates:
1. Raw T-SQL table definition (CREATE TABLE with IDENTITY primary key).
2. Pydantic DTO model for parsing JSON request bodies.
3. Raw SQL write (INSERT ... OUTPUT inserted.id / %s parameters).
4. Raw SQL read (SELECT) returning pure JSON lists.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import pymssql
import logging

from app.database import get_db_connection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reference/logs", tags=["reference-example"])


# --- 1. Raw T-SQL Schema Initialization for Reference Example ---
def init_reference_table():
    """Initializes the mock SystemLog table with explicit raw T-SQL in MSSQL."""
    try:
        conn = get_db_connection()
    except Exception as e:
        logger.warning(
            f"Could not connect to MS SQL Server to run init_reference_table: {e}. "
            "Ensure SQL Server is running and credentials in .env are correct."
        )
        return

    try:
        with conn.cursor() as cursor:
            # Explicit T-SQL table creation: IDENTITY(1,1) for auto-incrementing ID in MS SQL Server
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='system_logs' AND xtype='U')
                CREATE TABLE system_logs (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    message NVARCHAR(MAX) NOT NULL,
                    timestamp NVARCHAR(50) NOT NULL
                );
            """)
        conn.commit()
    except Exception as e:
        logger.error(f"Error initializing system_logs table: {e}")
        conn.rollback()
    finally:
        conn.close()


# --- 2. Pydantic DTO (Request Body Parser Only) ---
class SystemLogCreate(BaseModel):
    message: str = Field(..., min_length=1, description="Log message text")


# --- 3. Route Handlers Using Explicit Raw SQL ---
@router.get("/")
def get_system_logs():
    """Fetches all system logs using a raw T-SQL SELECT query from MS SQL Server."""
    try:
        conn = get_db_connection()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}. Please verify your MS SQL Server instance is reachable."
        )

    try:
        with conn.cursor(as_dict=True) as cursor:
            # Raw T-SQL query
            cursor.execute("SELECT id, message, timestamp FROM system_logs ORDER BY id DESC;")
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    finally:
        conn.close()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_system_log(payload: SystemLogCreate):
    """
    Inserts a new system log using raw SQL parameterized INSERT in MS SQL Server.
    Uses 'OUTPUT inserted.id' to retrieve the newly generated identity ID.
    Unpacks Pydantic DTO into raw SQL parameters to prevent SQL injection.
    """
    try:
        conn = get_db_connection()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}. Please verify your MS SQL Server instance is reachable."
        )

    current_timestamp = datetime.now(timezone.utc).isoformat()
    try:
        with conn.cursor(as_dict=True) as cursor:
            # Parameterized query (%s is the standard pymssql parameter placeholder)
            # OUTPUT inserted.id returns the generated IDENTITY column value directly
            sql = """
                INSERT INTO system_logs (message, timestamp)
                OUTPUT inserted.id
                VALUES (%s, %s);
            """
            cursor.execute(sql, (payload.message, current_timestamp))
            row = cursor.fetchone()
            created_id = row["id"] if row else None
        conn.commit()

        return {
            "id": created_id,
            "message": payload.message,
            "timestamp": current_timestamp
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
