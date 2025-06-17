from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

# Classe da entidade Leitura/Reading
class Reading(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sens_id = db.Column(db.Integer)
    temp = db.Column(db.Integer) # Celsius
    humi = db.Column(db.Integer) # Apesar de ser decimal, é mais conveniente armazenar como Int e transpor a virgula
    carb = db.Column(db.Integer) # Mesma coisa
    dateserver = db.Column(db.DateTime(), server_default=func.now())
    #datehard = db.Column(db.Datetime()) # Tempo logado pelo ESP

    def __init__(self, sens_id, temp, humi, carb):
        self.sens_id = sens_id
        self.temp = temp
        self.humi = humi
        self.carb = carb
        #self.datehard = datehard 