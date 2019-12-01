class Queries:

    class TEMPERATURE_MAX:
        sql = ("SELECT DISTINCT city, temperature_max FROM forecast "
               "WHERE temperature_max = (SELECT MAX(temperature_max) FROM forecast ) "
               "AND date BETWEEN ? AND ?;"
                )
    class PRECIPITATION_AVG:
        sql = ("SELECT city, AVG(precipitation) as precipitation_avg FROM forecast "
               "WHERE date BETWEEN ? AND ? GROUP BY city;"   
                )
    class INSERT_FORECAST:
        sql = 'INSERT OR IGNORE INTO forecast VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?);'
