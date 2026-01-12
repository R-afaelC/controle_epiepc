import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("localhost"),
        user=os.environ.get("root"),
        password=os.environ.get("1686074670"),
        database=os.environ.get("controle"),
        port=int(os.environ.get("DB_PORT", 3306))
    )




