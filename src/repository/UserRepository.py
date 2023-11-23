import sqlite3
from repository.BaseRepository import BaseRepository

getAllSettings = {
    "where": "",
    "order_by": "ORDER BY u.id ASC",
    "limit": 20,
    "offset": 0
}

class UserRepository(BaseRepository):

    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def findById(self, id: int):
        queryFileName = self._constants.SQL_FILES.USERS_FIND_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)

        return self.cursor.execute(query).fetchall()[0]

    
    def findByIds(self, ids: [int]):
        queryFileName = self._constants.SQL_FILES.USERS_FIND_BY_IDS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids=','.join(map(str,ids)))

        return self.cursor.execute(query).fetchall()
    
    def handleWhere(self,queryArguments):

        if len(queryArguments["where"]) == 0:
            queryArguments["where"] = "WHERE "
        else:
            queryArguments["where"] = queryArguments["where"] + " AND "
    
    def getAll(self, **kwargs):
        queryFileName = self._constants.SQL_FILES.USERS_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)

        settings = getAllSettings.copy()

        if "limit" in kwargs.keys():
            settings["limit"] = kwargs["limit"]
        if "offset" in kwargs.keys():
            settings["offset"] = kwargs["offset"]
        if "first_name" in kwargs.keys():
            self.handleWhere(settings)
            settings["where"] = settings["where"] + f"u.first_name LIKE '%{kwargs['first_name']}%'"
        if "last_name" in kwargs.keys():
            self.handleWhere(settings)
            settings["where"] = settings["where"] + f"u.last_name LIKE '%{kwargs['last_name']}%'"
        if "email" in kwargs.keys():
            self.handleWhere(settings)
            settings["where"] = settings["where"] + f"u.email = '{kwargs['email']}'"
        if "age" in kwargs.keys():
            if "lower_bound" in kwargs["age"]:
                self.handleWhere(settings)
                lower_bound = kwargs["age"]["lower_bound"]
                settings["where"] = settings["where"] + f"u.age >= {lower_bound}"
            if "upper_bound" in kwargs["age"]:
                self.handleWhere(settings)
                upper_bound = kwargs["age"]["upper_bound"]
                settings["where"] = settings["where"] + f"u.age <= {upper_bound}"
        if "gender" in kwargs.keys():
            self.handleWhere(settings)
            settings["where"] = settings["where"] + f"u.gender = '{kwargs['gender']}'"
        if "country" in kwargs.keys():
            self.handleWhere(settings)
            settings["where"] = settings["where"] +f"u.country = '{kwargs['country']}'"
        query = query.format(**settings)
        
        return self.cursor.execute(query).fetchall()
