from flask import Flask #as app
from controllers import routes
from models.sparq_api_db import db
import pymysql
import ssl

# Instanciando Flask no app.py
app = Flask(__name__, template_folder="views")

routes.init_app(app)

DB_USER = ""
DB_PASSWORD = ""

DB_NAME = "sparq-api-database"
DB_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@sparq-api-server.mysql.database.azure.com' #se tiver senha, usuario:senha. e.x: root:admin@localhost
FULL_URI = f'{DB_URI}/{DB_NAME}'


if __name__ == "__main__":
    connection = pymysql.connect(host="sparq-api-server.mysql.database.azure.com", user="ikashaieod", password="FnDzq1dFsoi$5ROt", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor, ssl={arrumar})
    # Conexão com SSL ativado mas sem certificação. Vulnerável a ataques MITM ^

    exists = False

    try:
        with connection.cursor() as cursor:
            #cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
            result = cursor.fetchone()
            if result is not None:
                exists = True
    except Exception as e:
        print(f'Connection error whilst accessing DB: {e}')
    finally:
        connection.close()

    if exists:
        app.config["DATABASE_NAME"] = DB_NAME
        app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URI

        db.init_app(app=app)
        with app.test_request_context():
            db.create_all()
        app.run(host="localhost", port=5000, debug=True)