import sqlite3
from repository.BaseRepository import BaseRepository

getAllSettings = {
    "where": "",
    "order_by": "ORDER BY o.created_at DESC",
    "limit": 20,
    "offset": 0
}

class OrderRepository(BaseRepository):

    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def findById(self, id: int):
        queryFileName = self._constants.SQL_FILES.ORDER_FIND_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)

        return self.cursor.execute(query).fetchall()[0]

    def findByIds(self, ids: [int]):
        queryFileName = self._constants.SQL_FILES.ORDER_FIND_BY_IDS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids=",".join(map(str, ids)))

        return self.cursor.execute(query).fetchall()

    def getAll(self, **kwargs):
        queryFileName = self._constants.SQL_FILES.ORDER_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)

        # construct the query
        settings = getAllSettings.copy()
        if "limit" in kwargs.keys() and kwargs["limit"] != "":
            settings["limit"] = kwargs["limit"]
        if "offset" in kwargs.keys() and kwargs["offset"] != "":
            settings["offset"] = kwargs["offset"]
        if "status" in kwargs.keys() and kwargs["status"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"o.status = '{kwargs['status']}'"
        if "gender" in kwargs.keys() and kwargs["gender"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"o.gender = '{kwargs['gender']}'"
        if "user_id" in kwargs.keys() and kwargs["user_id"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"o.user_id = {kwargs['user_id']}"
        if "order_id" in kwargs.keys() and kwargs["order_id"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"o.id = {kwargs['order_id']}"
        if "order_by" in kwargs.keys() and kwargs["order_by"] != "":
            field = kwargs["order_by"]["field"]
            ascOrDesc = "ASC" if kwargs["order_by"]["ascending"] else "DESC"
            settings["order_by"] = f"ORDER BY o.{field} {ascOrDesc}"
        query = query.format(**settings)

        return self.cursor.execute(query).fetchall()
