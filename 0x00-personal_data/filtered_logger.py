#!/usr/bin/env python3
""" PII and personal data
"""

from typing import List
from logging import Formatter, Logger, LogRecord
import logging
import re
import mysql.connector
from os import environ

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function called filter_datum that the log message
    """
    for u in fields:
        message = re.sub(f'{u}=.*?{separator}',
                         f'{u}={redaction}{separator}', message)
    return message


class RedactingFormatter(Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialized method
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: LogRecord) -> str:
        """ Filter values in incomming log records
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Implement get_logger function that takes no agruments
    """
    logg = logging.getLogger("user_data")
    logg.setLevel(logging.INFO)
    logg.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logg.addHandler(handler)

    return logg


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Function that returns a connector to the database
    """
    dbc = mysql.connector.connection.MySQLConnection(
        user=environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        host=environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=environ.get('PERSONAL_DATA_DB_NAME'))

    return dbc


def main():
    """ Funcion that takes no arguments and returns nothing
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field = [i[0] for i in cursor.description]

    logg = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field))
        logg.info(str_row.strip)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
