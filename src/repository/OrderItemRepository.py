import sqlite3

from BaseRepository import BaseRepository


class OrderItemRepository(BaseRepository):

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def findById(self, id: int):
        queryFileName = self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)

        result = self.cursor.execute(query).fetchall()
        if len(result) < 1:
            raise Exception("Order Item not found")

        return result[0]

    def findByIds(self, ids: [int]):
        queryFileName = self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_IDS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids=",".join(map(str, ids)))

        result = self.cursor.execute(query).fetchall()
        if len(result) < 1:
            raise Exception("Order Item not found")

        return result