import os
from pathlib import Path
from dotenv import load_dotenv
import pymssql

# Load environment variables from .env file located in backend/
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MSSQL_SERVER = os.getenv("MSSQL_SERVER", "localhost")
MSSQL_PORT = int(os.getenv("MSSQL_PORT", "1433"))
MSSQL_USER = os.getenv("MSSQL_USER", "sa")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "YourStrong@Password")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "LostAndFoundDB")


def get_db_connection() -> pymssql.Connection:
    """
    Creates and returns a raw Microsoft SQL Server connection using pymssql.
    as_dict=True enables dictionary-like row access (column_name -> value).
    """
    conn = pymssql.connect(
        server=MSSQL_SERVER,
        port=MSSQL_PORT,
        user=MSSQL_USER,
        password=MSSQL_PASSWORD,
        database=MSSQL_DATABASE,
        as_dict=True,
        autocommit=False,
    )
    return conn


def init_db() -> None:
    """
    Initialize database tables with explicit raw T-SQL (Transact-SQL) strings.
    TODO: Add table creation statements here once the team finalizes the ERD.
    Example:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='items' AND xtype='U')
                    CREATE TABLE items (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        title NVARCHAR(255) NOT NULL,
                        ...
                    );
                ''')
            conn.commit()
        finally:
            conn.close()
    """
    pass
