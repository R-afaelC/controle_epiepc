import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida.")

def get_connection():
    return psycopg.connect(DATABASE_URL)
