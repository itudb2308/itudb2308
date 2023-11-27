from repository.BaseRepository import BaseRepository


class OrderItemRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.ORDER_ITEM_FIND_BY_IDS)
