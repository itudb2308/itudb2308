from psycopg2._psycopg import connection

class TransactionManager:
    def __init__(self, dbConnection: connection):
        self.connection = dbConnection
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
