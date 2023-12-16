from repository.BaseRepository import BaseRepository

getAllSettings = {
    "where": "",
    "order_by": "ORDER BY o.created_at DESC",
    "limit": 20,
    "offset": 0
}


class OrderRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.ORDER_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.ORDER_FIND_BY_IDS)

    def getAllAndCount(self, **kwargs):
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
        if "customer_name" in kwargs.keys() and kwargs["customer_name"] != "":
            for term in kwargs["customer_name"].split():
                self.handleWhereStatement(settings)
                settings["where"] = settings["where"] + \
                    f"((u.first_name ILIKE '%{term}%') OR (u.last_name ILIKE '%{term}%'))"
        if "order_by" in kwargs.keys() and kwargs["order_by"] != "":
            field = kwargs["order_by"]["field"]
            ascOrDesc = "ASC" if kwargs["order_by"]["ascending"] else "DESC"
            settings["order_by"] = f"ORDER BY o.{field} {ascOrDesc}"
        query = query.format(**settings)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getDistinctStatus(self):
        queryFileName = self._constants.SQL_FILES.ORDER_GET_DISTINCT_STATUS
        query = self._getSqlQueryFromFile(queryFileName)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getDistinctGender(self):
        queryFileName = self._constants.SQL_FILES.ORDER_GET_DISTINCT_GENDER
        query = self._getSqlQueryFromFile(queryFileName)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def setOrderStatus(self, settings: dict):
        queryFileName = self._constants.SQL_FILES.ORDER_SET_STATUS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(**settings)
        self.cursor.execute(query)
        self.connection.commit()
