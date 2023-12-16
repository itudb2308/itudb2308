from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository


class OrderItemRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, transaction: Transaction, id: int):
        return self._findById(id, self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_ID, transaction)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_IDS, transaction)

    def getItemDetailsByOrderId(self, transaction: Transaction, orderId: int):
        queryFileName = self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_ORDER_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(orderId=orderId)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()
