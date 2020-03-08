import json
from datetime import datetime
from datetime import date

from flask import request, jsonify
from flask_restful import Resource

class Time(Resource):
    @classmethod
    def get(self):
    # def get(self, time):
        try:
            now = datetime.now()
            today = date.today()
            current_time = now.strftime("%H:%M:%S")
            current_date = today.strftime("%d/%m/%Y")
            return jsonify({'current_time': current_time,
                            'current_date': current_date})
        except ValueError:
            return {"message": "Error al obtener la hora"}
