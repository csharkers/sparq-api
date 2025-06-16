# Importa pacote Flask do modulo flask
from flask import Flask #as app
import pymysql
from controllers import routes
from models.SparqDB import db

# Instanciando Flask no app.py
app = Flask(__name__, template_folder="views")

routes.init_app(app)

DB_NAME = "games"
app.config["DATABASE_NAME"] = DB_NAME
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://root@localhost/{DB_NAME}' #se tiver senha, usuario:senha. e.x: root:admin@localhost

if __name__ == "__main__":
    #Instancia de conexão:
    connection = pymysql.connect(host="localhost", user="root", password="", charset="utf8mb4", cursorclass="pymysql.cursors.DictCursor")
    #Criacao de banco com tratamento de erro
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print(f'O banco de dados {DB_NAME} foi criado!')
    except Exception as e:
        print(f'Erro: {e}')
    finally:
        connection.close()
        
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    
    # Roda servidor no localhost, porta 5000; 0.0.0.0 = rede LAN
    app.run(host="localhost", port=5000, debug=True)