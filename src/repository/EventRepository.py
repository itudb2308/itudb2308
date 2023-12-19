from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository

getAllSettings = {
    "where": "",
    "order_by": "ORDER BY e.id ASC",
    "limit": 20,
    "offset": 0
}


class EventRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, transaction: Transaction, id: int):
        return self._findById(transaction, id, self._constants.SQL_FILES.EVENTS_FIND_BY_ID)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(transaction, ids, self._constants.SQL_FILES.EVENTS_FIND_BY_IDS)

    def getAll(self, transaction: Transaction, **kwargs):
        queryFileName = self._constants.SQL_FILES.EVENTS_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)

        settings = getAllSettings.copy()

        if "limit" in kwargs.keys() and kwargs["limit"] != "":
            settings["limit"] = kwargs["limit"]
        if "offset" in kwargs.keys() and kwargs["offset"] != "":
            settings["offset"] = kwargs["offset"]
        if "user_id" in kwargs.keys() and kwargs["user_id"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"e.user_id = {kwargs['user_id']}"
        if "session_id" in kwargs.keys() and kwargs["session_id"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"e.session_id = {kwargs['session_id']}"
        if "created_at" in kwargs.keys() and kwargs["created_at"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"e.created_at = {kwargs['created_at']}"
        if "event_type" in kwargs.keys() and kwargs["event_type"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"e.event_type = {kwargs['event_type']}"
        if "order_by" in kwargs.keys() and kwargs["order_by"] != "":
            field = kwargs["order_by"]["field"]
            ascOrDesc = "ASC" if kwargs["order_by"]["ascending"] else "DESC"
            settings["order_by"] = f"ORDER BY o.{field} {ascOrDesc}"
        query = query.format(**settings)

        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    def addEvent(self, transaction: Transaction, event: dict):
        queryFileName = self._constants.SQL_FILES.EVENTS_ADD_EVENT
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(event)
        query = query.format(**event)
        transaction.cursor.execute(query, event)

    def deleteEventById(self, transaction: Transaction, id: int) -> int:
        queryFileName = self._constants.SQL_FILES.EVENTS_DELETE_EVENT_BY_ID
        return self._deleteById(transaction, id, queryFileName)