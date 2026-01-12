import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "1686074670"),
        database=os.environ.get("MYSQL_DATABASE", "controle"),
        port=int(os.environ.get("MYSQL_PORT", 3306))
    )








