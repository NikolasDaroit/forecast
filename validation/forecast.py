import datetime

class InvalidLocationError(Exception):
    """ Raised in case of
    {"error":true,"detail":"Access forbidden, you have no acces for this locale: 1992"}
    """
    pass


class InvalidDateError(Exception):
    """ Raised in case of
    data isn't in the format YYYY-MM-DD
    """
    pass


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise InvalidDateError
