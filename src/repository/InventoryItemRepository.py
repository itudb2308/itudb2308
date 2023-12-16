from repository.BaseRepository import BaseRepository
import time


class InventoryItemRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_IDS)

    # Function to add inventory item for product specified by dictionary .
    # Returns the id of the added inventory item.
    def addInventoryItem(self, data: dict) -> int:
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_ADD_INVENTORY_ITEM
        query = self._getSqlQueryFromFile(queryFileName)

        argument = {
            "product_id": data[0],
            "created_at":  time.strftime('%Y-%m-%d %H:%M:%S'),
            "sold_at": None,
            "cost": data[1],
            "product_category": data[2],
            "product_name": data[3],
            "product_brand": data[4],
            "product_retail_price": data[5],
            "product_department": data[6],
            "product_sku": data[7],
            "product_distribution_center_id": data[8]
        }
        # Replace ' with '' to escape the apostrophe in the query
        self.replaceDoubleApostrophes(argument)
        query = query.format(**argument)

        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def getTotalStockAndSold(self, product_id: int, distribution_center_id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_GET_TOTAL_STOCK_AND_SOLD
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=product_id, distribution_center_id=distribution_center_id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getInventoryItemsByProductId(self, product_id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_GET_INVENTORY_ITEMS_BY_PRODUCT_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=product_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    # Function to update the sold_at field of an inventory item.
    # Here there is an issue with quantity
    # We rely on the frontend to make sure that the quantity is not more than the stock
    # TODO : Double check quanttity is less than or equal to stock.
    def sellInventoryItem(self, id: int , quantity: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_SELL_INVENTORY_ITEMS
        query = self._getSqlQueryFromFile(queryFileName)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        query = query.format(product_id=id, current_time = timestamp, quantity=quantity)
        self.cursor.execute(query)
        self.connection.commit()