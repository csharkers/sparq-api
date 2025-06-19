import os
from flask import Flask
from controllers import routes
from models.sparq_api_db import db
import pymysql

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "sparq-api-database"
DB_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@sparq-api-server.mysql.database.azure.com'
FULL_URI = f'{DB_URI}/{DB_NAME}'


def create_app():
    app = Flask(__name__, template_folder="views")
    app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    routes.init_app(app)
    db.init_app(app)

    with app.app_context():
        connection = pymysql.connect(
            host="sparq-api-server.mysql.database.azure.com",
            user=DB_USER,
            password=DB_PASSWORD,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

        exists = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
                result = cursor.fetchone()
                if result is not None:
                    exists = True
        finally:
            connection.close()

        if exists:
            db.create_all()

    return app

app = create_app()
