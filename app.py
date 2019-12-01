from flask import Flask, jsonify
from flask_restful import Api
from resources.forecast import Forecast, ForecastAnalyze
from db.database import create_database
from flask_sqlalchemy import SQLAlchemy
from config import app, api, db, db_rel_path


api.add_resource(Forecast, '/cidade')
api.add_resource(ForecastAnalyze, '/analise')

if __name__ == '__main__':
    #db.create_all()
    create_database(db_rel_path)
    app.run()
