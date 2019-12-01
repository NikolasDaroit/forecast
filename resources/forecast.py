from models.forecast import ForecastModel, ClimatempoModel, InvalidLocationError, InvalidDateError
from flask_restful import Resource, reqparse
from flask_restful import reqparse
import json
from config import ErrorMessages

class Forecast(Resource):

    def get(self):
        """
        Resource for /cidade
        Save data from climatempo on database
        Example request: /cidade?id=3412
        Example output: {"message": "saved data for Natividade"}
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=int, help='id is required and should be an integer', location='args')
        args = parser.parse_args()
        id = args.get('id')
        try:
            result, status = ClimatempoModel(id).get_data()
        except InvalidLocationError:
            return {'error': ErrorMessages.INVALID_LOCATION.message}
        
        result = json.loads(result)
        
        city_data = []
        city = result['name']
        state = result['state']
        country = result['country']
        for i in result['data']:
            date = i['date']
            probability = i['rain']['probability']
            precipitation = i['rain']['precipitation']
            temperature_min = i['temperature']['min']
            temperature_max = i['temperature']['max']
            city_data.append(ForecastModel(id
                                           ,city
                                           ,state
                                           ,country
                                           ,date
                                           ,probability
                                           ,precipitation
                                           ,temperature_min
                                           ,temperature_max))
        
        ForecastModel.bulk_add(city_data)
        return {'message':f'saved data for {city}'}, 200



class ForecastAnalyze(Resource):

    def get(self):
        """
        Resource for /analise
        Return max temperature from among cities
        Return avg precipitation for each city
        
        Example request: /analise?data_inicial=2019-12-01&data_final=2019-12-07
        Example output: {"max_temp": [{"city": "Natividade", "temperature_max": 37}], "avg_precipitation": [{"city": "Natividade", "precipitation_avg": 7.0}]}
        """
        parser = reqparse.RequestParser()
        parser.add_argument('data_inicial', required=True, type=str,
                            help='Required Field - Sould be YYYY-MM-DD', location='args')
        parser.add_argument('data_final', required=True, type=str,
                            help='Required Field - Sould be YYYY-MM-DD', location='args')
        args = parser.parse_args()

        start_date = args.get('data_inicial')
        end_date = args.get('data_final')
        
        try:
            data = ForecastModel.analyze(start_date,
                                         end_date)
        except InvalidDateError:
            return {'error': ErrorMessages.INVALID_DATE.message}

        
        if data:
            return data, 200
        return {'message': 'No users found!'}, 404
