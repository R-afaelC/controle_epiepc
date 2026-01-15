import mysql.connector
import os
def get_connection():
     return mysql.connector.connect( 
            host=os.environ["MYSQL_HOST"],
            user=os.environ["USUARIO_MYSQL"],
            password=os.environ["MSQL_PASSWORD"],
            database=os.environ["BANCO_DE_DADOS_MYSQL"],
            port=int(os.environ["MYSQL_PORT"]),
             connection_timeout=5
              )








