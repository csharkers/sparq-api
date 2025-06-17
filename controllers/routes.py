from flask import request
from models.sparq_api_db import Reading, db

def init_app(app):
    @app.route('/readings', methods=['GET', 'POST'])
    @app.route('/readings/<int:qnt>') #Especifica a quantidade de leituras a se puxar
    def readings(id=1): #Padrão é retornar 1 leitura, a última.
        if(request.method == "POST"):
            newReading = Reading(
                request.form['sens_id'],
                request.form['temp'],
                request.form['humi'],
                request.form['carb'],
                #request.form['datehard'] # Data de hardware - do ESP.
            )
            db.session.add(newReading)
            db.session.commit()
            return "Success", 201
        else:
            # DEBUG DEBUG DEBUG DEBUG DEV TEST START
            newReading = Reading(
                1,
                2504,
                76,
                3001,
                #request.form['datehard'] # Data de hardware - do ESP.
            )
            db.session.add(newReading)
            db.session.commit()
            return "Success", 201
            # DEBUG DEBUG DEBUG DEBUG DEV TEST START END