from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository


class OrderItemRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, transaction: Transaction, id: int):
        return self._findById(transaction, id, self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_ID)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(transaction, ids, self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_IDS)

    def getItemDetailsByOrderId(self, transaction: Transaction, orderId: int):
        queryFileName = self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_ORDER_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(orderId=orderId)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    def createOrderItems(self, transaction: Transaction, orderId: int, userId: int, orderedProducts: dict):
        queryFileName = self._constants.SQL_FILES.ORDER_ITEM_CRAETE_ORDER_ITEMS
        query = self._getSqlQueryFromFile(queryFileName)

        records = []
        for productId, productOrderInfo in orderedProducts.items():
            price = productOrderInfo["price"]
            for inventoryItemId in productOrderInfo["ids"]:
                records.append(f"({orderId}, {userId}, {productId}, {inventoryItemId}, 'Processing', now(), {price})")

        query = query.format(values=",\n".join(records))
        transaction.cursor.execute(query)
