import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "containers-us-west-xxx.railway.app"),
        user=os.environ.get("USUARIO_MYSQL", "root"),
        password=os.environ.get("SENHA_DO_MYSQL", "1686074670"),
        database=os.environ.get("BANCO_DE_DADOS_MYSQL", "controle"),
        port=int(os.environ.get("MYSQL_PORT", 3306)),
        connection_timeout=5

    )









