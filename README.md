## Description:
Forecast api to get climatempo data and get personalized reports based on date

So far active endpoints are:

GET /cidade

GET /analise



### Steps to run app and tests:

1.Install Python (tested on Python 3.8.0, Windows 10)

3.Download project from GitHub

2.Create virtualenv

```
$ python -m venv ambar-forecast
```

```
$ cd ambar-forecast\Scripts
```

```
$ activate
```

4.Go to root folder of the project, install required modules:
    
```
$ pip install -r requirements.txt
```

5.To run app:

```
$ python app.py
```

Then in Postman (have to be installed on your system), you can import collection of URL's from __postman__ folder placed in root folder of the downloaded app.

6.To run automated API tests, open terminal/console and run app, then open another terminal/console window, go to __tests__ folder and enter command:

```
$ python tests\forecast_endpoint_test.py
```
```
$ python tests\model_test.py
```
