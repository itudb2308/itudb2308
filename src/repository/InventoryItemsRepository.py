import sqlite3

from BaseRepository import BaseRepository

class InventoryItemsRepository(BaseRepository):

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def findById(self, id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)

        result = self.cursor.execute(query).fetchall()

        if len(result) < 1 :
            raise Exception("Inventory item not found!")

        return result[0]
    
    def findByIds(self, ids: [int]):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_IDS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids=','.join(map(str,ids)))

        result = self.cursor.execute(query).fetchall()

        if len(result) < 1 :
            raise Exception("Inventory item not found!")

        return result