from flask import request, jsonify
from models.sparq_api_db import Reading, db

def init_app(app):
    @app.route('/readings', methods=['GET', 'POST'])
    @app.route('/readings/<int:qnt>', methods=['GET'])
    @app.route('/readings/<int:qnt>/<int:sens_id>', methods=['GET']) #Especifica a quantidade de leituras a se puxar
    def readings(qnt = 1, sens_id = -1): #Padrão é retornar 1 leitura, a última.
        if(request.method == "POST"):
            newReading = Reading(
                int(request.form['sens_id']),
                int(request.form['temp']),
                int(request.form['humi']),
                int(request.form['carb']),
                #request.form['datehard'] # Data de hardware - do ESP.
            )
            db.session.add(newReading)
            db.session.commit()
            return "Success", 201
        else:
            query = Reading.query.order_by(Reading.dateserver.desc())

            if sens_id != -1:
                query = query.filter_by(sens_id=sens_id)

            results = query.limit(qnt).all()
            results = list(reversed(results))

            readings_list = [{
                "id": r.id,
                "sens_id": r.sens_id,
                "temp": r.temp,
                "humi": r.humi,
                "carb": r.carb,
                "dateserver": r.dateserver.isoformat() if r.dateserver else None
            } for r in results]

            return jsonify(readings_list), 200

            # DEBUG DEBUG DEBUG DEBUG DEV TEST START
            # newReading = Reading(
            #     1,
            #     2504,
            #     76,
            #     3001,
            #     #request.form['datehard'] # Data de hardware - do ESP.
            # )
            # print(newReading.dateserver)
            # db.session.add(newReading)
            # db.session.commit()
            # return "Success", 201
            # DEBUG DEBUG DEBUG DEBUG DEV TEST START END