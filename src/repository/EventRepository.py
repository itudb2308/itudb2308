from repository.BaseRepository import BaseRepository

getAllSettings = {
    "where": "",
    "order_by": "ORDER BY events.id ASC",
    "limit": 20,
    "offset": 0
}

class EventRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.EVENTS_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.EVENTS_FIND_BY_IDS)

    def getAll(self, **kwargs):
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
        if "order_by" in kwargs.keys() and kwargs["order_by"] != "":
            field = kwargs["order_by"]["field"]
            ascOrDesc = "ASC" if kwargs["order_by"]["ascending"] else "DESC"
            settings["order_by"] = f"ORDER BY o.{field} {ascOrDesc}"
        query = query.format(**settings)

        self.cursor.execute(query)
        return self.cursor.fetchall()
