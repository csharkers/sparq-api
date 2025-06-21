from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json

db = SQLAlchemy()

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sens_id = db.Column(db.Integer)
    sens_name = db.Column(db.String(100))  # Nome do sensor
    temp = db.Column(db.Integer)  # Celsius *100
    humi = db.Column(db.Integer)  # Umidade *100
    carb = db.Column(db.Integer)  # CO2 em ppm 
    dateserver = db.Column(db.DateTime(), default=datetime.now)
    thermo_mat = db.Column(db.Text)  # Matriz 8x8 serializada como JSON

    def __init__(self, sens_id, temp, humi, carb, sens_name, thermo_mat=None):
        self.sens_id = sens_id
        self.temp = temp
        self.humi = humi
        self.carb = carb
        self.sens_name = sens_name

        if thermo_mat is not None:
            self.thermo_mat = json.dumps(thermo_mat)

    def get_thermo_mat(self):
        if self.thermo_mat:
            return json.loads(self.thermo_mat)
        return None
