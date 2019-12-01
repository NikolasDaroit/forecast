import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models import forecast
from models.forecast import ForecastModel
from database import create_database

class DataBaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_file = 'forecast_test.db'
        if os.path.exists(cls.test_db_file):
            os.system(f'rm {cls.test_db_file}')
        create_database(cls.test_db_file)
        cls.uri = 'http://127.0.0.1:5000'

    def test_forecast_model_bulk_add_analyze(cls):
        """
        Tests bulk_add writting to database
        Tests analyze reading correct data
        """
        forecast_list = [
            ForecastModel(3412, 'Natividade', 'RJ', 'BR',
                          '1990-01-01', 34, 0, 11, 13),
            ForecastModel(3412, 'Natividade', 'RJ', 'BR',
                          '1990-01-02', 23, 1, 12, 14),
            ForecastModel(3412, 'Natividade', 'RJ', 'BR',
                          '1990-01-03', 12, 2, 21, 15),
            ForecastModel(3412, 'Natividade', 'RJ', 'BR',
                          '1990-01-04', 3, 12, 22, 29),
            ForecastModel(3412, 'Natividade', 'RJ', 'BR', '1990-01-05', 45, 18, 0, 30)]

        ForecastModel.bulk_add(forecast_list, cls.test_db_file)
        data = ForecastModel.analyze('1990-01-01',
                                     '1990-01-05', cls.test_db_file)
        
        max_temp = next(iter(data.get('max_temp') or []), None)
        cls.assertEqual(30, max_temp.get('temperature_max'))
        cls.assertEqual('Natividade', max_temp.get('city'))

        avg_prec = next(iter(data.get('avg_precipitation') or []), None)
        cls.assertEqual(6.6, avg_prec.get('precipitation_avg'))
        cls.assertEqual('Natividade', avg_prec.get('city'))
        cls.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
