from flask import request, jsonify
from models.sparq_api_db import Reading, db
from sqlalchemy.orm import aliased
from sqlalchemy import func
import json

def init_app(app):
    @app.route('/readings', methods=['GET', 'POST'])
    @app.route('/readings/<int:qnt>', methods=['GET']) #Especifica a quantidade de leituras a se puxar
    @app.route('/readings/<int:qnt>/<int:sens_id>', methods=['GET']) #Especifica a quantidade de leituras a se puxar de um sensor
    def readings(qnt = -1, sens_id = -1): #Padrão é retornar 1 leitura, a última.
        if request.method == "POST":
            data = request.get_json()

            if not data:
                return jsonify({"error": "Invalid or missing JSON body"}), 400

            try:
                newReading = Reading(
                    sens_id=int(data['sens_id']),
                    temp=int(data['temp']),
                    humi=int(data['humi']),
                    carb=int(data['carb']),
                    sens_name=data.get('sens_name'),
                    thermo_mat=data.get('thermo_mat')  # Espera-se uma lista 8x8 de floats (oq a AMG retorna)
                )

                db.session.add(newReading)
                db.session.commit()
                return jsonify({"message": "Success"}), 201

            except (KeyError, ValueError, TypeError) as e:
                return jsonify({"error": f"Missing or invalid field: {e}"}), 400
        else:
            if qnt == -1:
                # Get most recent reading per sens_id
                subquery = db.session.query(
                    func.max(Reading.id).label('max_id')
                ).group_by(Reading.sens_id).subquery()

                # Join to Reading table to get full rows
                results = Reading.query.filter(Reading.id.in_(subquery)).order_by(Reading.sens_id).all()
            else:

                query = Reading.query.order_by(Reading.dateserver.desc())

                if sens_id != -1:
                    query = query.filter_by(sens_id=sens_id)

                if qnt > 0:
                    query = query.order_by(Reading.id.desc()).limit(qnt)
                elif qnt == 0:
                    query = query.order_by(Reading.id.desc())  # retorna todas sem limitar

                results = query.all()
                results = list(reversed(results))

            readings_list = []
            for r in results:
                readings_list.append({
                    "id": r.id,
                    "sens_name": r.sens_name,
                    "sens_id": r.sens_id,
                    "temp": r.temp,
                    "humi": r.humi,
                    "carb": r.carb,
                    "dateserver": r.dateserver.isoformat() if r.dateserver else None,
                    "thermo_mat": json.loads(r.thermo_mat) if r.thermo_mat else None,
                    "temp_soil": (
                        (lambda t: max(t) if t else None)(json.loads(r.thermo_mat))
                        if r.thermo_mat else None
                    )
                })

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