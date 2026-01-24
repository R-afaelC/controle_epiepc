import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1686074670",
        database="controle"  # nome do banco
    )


