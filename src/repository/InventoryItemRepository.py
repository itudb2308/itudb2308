from repository.BaseRepository import BaseRepository


class InventoryItemRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_IDS)
    
    def getTotalStock(self, product_id: int, distribution_center_id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_GET_TOTAL_STOCK
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=product_id, distribution_center_id = distribution_center_id )
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def getTotalSold(self, product_id: int, distribution_center_id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_GET_TOTAL_SOLD
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=product_id, distribution_center_id = distribution_center_id )
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
        

