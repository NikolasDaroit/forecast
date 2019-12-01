import sqlite3
from flask_sqlalchemy import SQLAlchemy
from config import db, db_rel_path, TOKEN_CLIMATEMPO, ErrorMessages
import requests
from db.queries import Queries
import datetime
import pandas as pd
from validation.forecast import InvalidLocationError, InvalidDateError, validate_date


class ForecastModel:

    def __init__(self, id
                 ,city
                 ,state
                 ,country
                 ,date
                 ,probability
                 ,precipitation
                 ,temperature_min
                 ,temperature_max):

        self.id=id
        self.city=city
        self.state=state
        self.country=country
        self.date=date
        self.probability=probability
        self.precipitation=precipitation
        self.temperature_min=temperature_min
        self.temperature_max=temperature_max

        
    @staticmethod
    def bulk_add(list_forecast, db_rel_path=db_rel_path):
        connection = sqlite3.connect(db_rel_path)
        cursor = connection.cursor()

        query = Queries.INSERT_FORECAST.sql
        for item in list_forecast:
            cursor.execute(query, (item.city,
                                   item.state,
                                   item.country,
                                   item.date,
                                   item.probability,
                                   item.precipitation,
                                   item.temperature_min,
                                   item.temperature_max
                                   ))

        connection.commit()
        connection.close()
        
    
    @classmethod
    def analyze(cls, start_date, end_date, db_path=db_rel_path):
        try:
            validate_date(start_date)
            validate_date(end_date)
        except InvalidDateError:
            raise
        
        
        connection = sqlite3.connect(db_path)
        
        max_temp_df = pd.read_sql(
            sql=Queries.TEMPERATURE_MAX.sql, con=connection, params=[start_date, end_date])
        
        
        avg_precipitation_df = pd.read_sql(
            sql=Queries.PRECIPITATION_AVG.sql, con=connection, params=[start_date, end_date])
        

        connection.close()

        data = {'max_temp': max_temp_df.to_dict (orient='records'),
                'avg_precipitation': avg_precipitation_df.to_dict(orient='records')
                }

        return data

    
    def list_item(self):
        return [
            
            self.city,
            self.state,
            self.country,
            self.date,
            self.probability,
            self.precipitation,
            self.temperature_max,
            self.temperature_min
        ]


    def json(self):
        return {
            'id':self.id,
            'city':self.city,
            'state':self.state,
            'country':self.country,
            'date':self.date,
            'probability':self.probability,
            'precipitation':self.precipitation,
            'temperature_max':self.temperature_max,
            'temperature_min':self.temperature_min
        }


class ClimatempoModel:

    def __init__(self, id):
        self.id = id
        self.token = TOKEN_CLIMATEMPO
    
    
    def get_data(self):
        url = f'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{self.id}/days/15?token={self.token}'
        r = requests.get(url)
        if r.status_code == 200:
            return r.text, r.status_code
        raise InvalidLocationError
    

