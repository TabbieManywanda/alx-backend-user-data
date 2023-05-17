#!/usr/bin/env python3

'''Returning obfuscated log message'''

import re
from typing import List
import logging
from os import environ
from mysql.connector import connection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''Initialize class'''

        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter values in incoming log records using `filter_datum`'''

        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''Returns log message obfuscated'''

    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


def get_logger() -> logging.Logger:
    '''takes no arguments and returns a `logging.Logger object`'''

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    ''' returns a connector to the database'''

    username = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = environ.get('PERSONAL_DATA_DB_NAME')
    connector = connection.MySQLConnection(user=username,
                                           password=password,
                                           host=db_host,
                                           database=db_name)
    return connector


def main() -> None:
    '''takes no arguments and returns nothing'''

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    headers = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        info_answer = ''
        for x, y in zip(row, headers):
            info_answer += f'{y}={(x)}; '
        logger.info(info_answer)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
