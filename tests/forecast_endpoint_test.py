import requests
import unittest
import json
import os
from database import create_database


class ForecastTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists('forecast_test.db'):
            os.system('rm forecast_test.db')
        create_database('forecast_test.db')
        cls.uri = 'http://127.0.0.1:5000'

    def test_cidade_status_code(cls):
        """
        Tests status code for cidade endpoint
        """
        cls.uri += '/cidade?id=3412'
        uri_request = requests.get(cls.uri)
        cls.assertEqual(200, uri_request.status_code)

    def test_cidade_response_check(cls):
        """
        Tests response for cidade endpoint
        """
        cls.uri += '/cidade?id=3477'
        uri_request = requests.get(cls.uri).content
        content_decode = json.loads(uri_request.decode('utf-8'))
        cls.assertEqual("saved data for São Paulo",
                        content_decode.get('message'))

    def test_cidade_invalid_id(cls):
        """
        Tests response for cidade endpoint with invalid id
        """
        cls.uri += '/cidade?id=0'
        uri_request = requests.get(cls.uri).content
        content_decode = json.loads(uri_request.decode('utf-8'))
        cls.assertEqual("Invalid location, double check the input value",
                        content_decode.get('error'))

    def test_cidade_empty_id(cls):
        """
        Tests response for cidade endpoint without id parameter
        """
        cls.uri += '/cidade'
        uri_request = requests.get(cls.uri).content
        content_decode = json.loads(uri_request.decode('utf-8'))
        cls.assertEqual("id is required and should be an integer",
                        content_decode.get('message').get('id'))


    def test_analyze_response_count_check(cls):
        """
        Tests analyze response for analise endpoint
        """
        cls.uri += '/analise?data_inicial=2019-12-01&data_final=2019-12-07'
        uri_request = requests.get(cls.uri).content
        content_decode = json.loads(uri_request.decode('utf-8'))
        cls.assertGreaterEqual(len(content_decode.get('max_temp')),1)
        cls.assertGreaterEqual(
            len(content_decode.get('avg_precipitation')), 1)


    @classmethod
    def tearDownClass(cls):
        os.system('rm forecast_test.db')

if __name__ == '__main__':
    unittest.main(verbosity=2)
