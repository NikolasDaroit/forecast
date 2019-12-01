from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

TOKEN_CLIMATEMPO = 'b22460a8b91ac5f1d48f5b7029891b53'
app = Flask(__name__)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////C:/Users/majinbuzz/workspace/ambar/zero/REST_API_Flask/db/datashop.db'
db_rel_path = './db/forecast.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/forecast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'test'

class ErrorMessages:

    class INVALID_LOCATION:
        message = 'Invalid location, double check the input value'

    class INVALID_DATE:
        message = 'Incorrect date format, should be YYYY-MM-DD'
