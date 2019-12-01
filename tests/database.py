import sqlite3


def create_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_forecast_table = (
        'CREATE TABLE IF NOT EXISTS forecast('
        '    id              INTEGER      PRIMARY KEY,'
        '    city            VARCHAR(30),'
        '    state           VARCHAR(3),'
        '    country         VARCHAR(3),'
        '    date            DATE,'
        '    probability     INTEGER,'
        '    precipitation   INTEGER,'
        '    temperature_min INTEGER      NOT NULL,'
        '    temperature_max INTEGER      NOT NULL'
        ')'
    )
    create_forecast_index = (
        'CREATE UNIQUE INDEX IF NOT EXISTS city_state_country_date ON forecast('
        'city,state,country,date)'
    )

    cursor.execute(create_forecast_table)
    cursor.execute(create_forecast_index)
    cursor.execute(
        "INSERT OR REPLACE INTO forecast(city,state,country,date,probability,precipitation,temperature_min,temperature_max)VALUES('esteio', 'RS', 'BR', '2019-12-03', 25, 10, 0, 30)")

    connection.commit()
    connection.close()

    print('Database successfully created and populated with data!')
