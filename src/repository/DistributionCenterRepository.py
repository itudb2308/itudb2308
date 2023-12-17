from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository


class DistributionCenterRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)
        self.defaultArguments = {
            "where": "",
            "order_by": "ORDER BY D.id ASC",
            # Removing the limit and offset because they are not used for now!!
            # "limit": 100,
            # "offset": 0
        }

    def findById(self, transaction: Transaction, id: int):
        return self._findById(transaction, id, self._constants.SQL_FILES.DISTRIBUTION_CENTERS_FIND_BY_ID)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(transaction, ids, self._constants.SQL_FILES.DISTRIBUTION_CENTERS_FIND_BY_IDS)

    def getAll(self, transaction: Transaction, **kwargs):
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
            queryArguments["order_by"] = f" ORDER BY D.{columnName} {ascOrDesc}"

        # I'm not sure if this will be used, but I'm leaving it here just in case
        if "latitude" in kwargs.keys() and kwargs["latitude"] != "":
            self.handleWhereStatement(queryArguments)
            queryArguments["where"] = queryArguments["where"] + f" D.latitude = '{kwargs['latitude']}' "
        if "longitude" in kwargs.keys() and kwargs["longitude"] != "":
            self.handleWhereStatement(queryArguments)
            queryArguments["where"] = queryArguments["where"] + f" D.longitude = '{kwargs['longitude']}' "

        query = query.format(**queryArguments)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    # returns the id of the newly added distribution center
    def addDistributionCenter(self, transaction: Transaction, distributionCenter: dict) -> int:
        queryFileName = self._constants.SQL_FILES.DISTRIBUTION_CENTERS_ADD_DISTRIBUTION_CENTER
        query = self._getSqlQueryFromFile(queryFileName)
        queryArguments = {
            "name": distributionCenter["name"],
            "latitude": distributionCenter["latitude"],
            "longitude": distributionCenter["longitude"]
        }
        query = query.format(**queryArguments)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()[0]

    # returns the id of the newly added distribution center
    def updateDistributionCenter(self, transaction: Transaction, distributionCenter: dict):
        queryFileName = self._constants.SQL_FILES.DISTRIBUTION_CENTERS_UPDATE_DISTRIBUTION_CENTER
        query = self._getSqlQueryFromFile(queryFileName)
        queryArguments = {
            "id": distributionCenter["id"],
            "name": distributionCenter["name"],
            "latitude": distributionCenter["latitude"],
            "longitude": distributionCenter["longitude"]
        }
        query = query.format(**queryArguments)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()[0]

    def deleteDistributionCenter(self, transaction: Transaction, id: int):
        queryFileName = self._constants.SQL_FILES.DISTRIBUTION_CENTERS_DELETE_DISTRIBUTION_CENTER
        query = self._getSqlQueryFromFile(queryFileName)
        queryArguments = {
            "id": id
        }
        query = query.format(**queryArguments)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()[0]
