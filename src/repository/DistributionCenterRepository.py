from repository.BaseRepository import BaseRepository

class DistributionCenterRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)
        self.defaultArguments = {
            "where": "",
            "order_by": "ORDER BY D.id ASC",
            "limit": 20,
            "offset": 0
        }

    def findById(self, id: int):
        return self._findById(id, self._constants.SQL_FILES.DISTRIBUTION_CENTERS_FIND_BY_ID)

    def findByIds(self, ids: [int]):
        return self._findByIds(ids, self._constants.SQL_FILES.DISTRIBUTION_CENTERS_FIND_BY_IDS)

    def getAll(self,**kwargs):
        queryFileName = self._constants.SQL_FILES.DISTRIBUTION_CENTERS_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)
        queryArguments = self.defaultArguments.copy()

        if "limit" in kwargs.keys() and kwargs["limit"] != "":
            queryArguments["limit"] = kwargs["limit"]
        if "offset" in kwargs.keys() and kwargs["offset"] != "":
            queryArguments["offset"] = kwargs["offset"]
        if "id" in kwargs and kwargs["id"] != "":
            self.handleWhereStatement(queryArguments)
            queryArguments["where"] = queryArguments["where"] + f" D.id = '{kwargs['id']}' "
        if "name" in kwargs and kwargs["name"] != "":
            self.handleWhereStatement(queryArguments)
            queryArguments["where"] = queryArguments["where"] + f" D.name = '{kwargs['name']}' "

        if "order_by_columnName" in kwargs and kwargs["order_by_columnName"] != "":
            columnName = kwargs["order_by_columnName"]
            # set default order direction is ascending
            if "order_direction" not in kwargs.keys() or kwargs["order_direction"] == "":
                kwargs["order_direction"] = "Ascending"
    
            ascOrDesc = "ASC" if kwargs["order_direction"] == "Ascending" else "DESC"
            queryArguments["order_by"] = f" ORDER BY P.{columnName} {ascOrDesc}"

        # I'm not sure if this will be used, but I'm leaving it here just in case
        if "latitude" in kwargs.keys() and kwargs["latitude"] != "":
            self.handleWhereStatement(queryArguments)
            queryArguments["where"] = queryArguments["where"] + f" D.latitude = '{kwargs['latitude']}' "
        if "longitude" in kwargs.keys() and kwargs["longitude"] != "":
            self.handleWhereStatement(queryArguments)
            queryArguments["where"] = queryArguments["where"] + f" D.longitude = '{kwargs['longitude']}' "

        query = query.format(**queryArguments)
        self.cursor.execute(query)
        return self.cursor.fetchall()