import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Erstellt eine PostgreSQL-Verbindung"""
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="yondem",
        user="yondem",
        password="dev123",
        cursor_factory=RealDictCursor
    )
