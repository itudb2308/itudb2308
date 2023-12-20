from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository
import time


class InventoryItemRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, transaction: Transaction, id: int):
        return self._findById(transaction, id, self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_ID)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(transaction, ids, self._constants.SQL_FILES.INVENTORY_ITEMS_FIND_BY_IDS)

    # Function to add inventory item for product specified by dictionary .
    # Returns the id of the added inventory item.
    def addInventoryItem(self, transaction: Transaction, data: dict) -> int:
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

        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()[0]

    def getTotalStockAndSold(self, transaction: Transaction, product_id: int, distribution_center_id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_GET_TOTAL_STOCK_AND_SOLD
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=product_id, distribution_center_id=distribution_center_id)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    def getInventoryItemsByProductId(self, transaction: Transaction, product_id: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_GET_INVENTORY_ITEMS_BY_PRODUCT_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=product_id)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()

    # Function to update the sold_at field of an inventory item.
    # Here there is an issue with quantity
    # We rely on the frontend to make sure that the quantity is not more than the stock
    # TODO : Double check quanttity is less than or equal to stock.
    def sellInventoryItem(self, transaction: Transaction, productId: int, quantity: int):
        queryFileName = self._constants.SQL_FILES.INVENTORY_ITEMS_SELL_INVENTORY_ITEMS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(product_id=productId, quantity=quantity)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()
