from psycopg2._psycopg import connection


class Transaction:
    def __init__(self, dbConnection: connection):
        self._connection = dbConnection
        self.cursor = self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()
