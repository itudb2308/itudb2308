from dto.Transaction import Transaction
from repository.BaseRepository import BaseRepository

getAllSettings = {
    "where": "",
    "order_by": "ORDER BY u.id ASC",
    "limit": 20,
    "offset": 0
}


class UserRepository(BaseRepository):

    def __init__(self, connection):
        super().__init__(connection)

    def findById(self, transaction: Transaction, id: int):
        return self._findById(transaction, id, self._constants.SQL_FILES.USERS_FIND_BY_ID)

    def findByIds(self, transaction: Transaction, ids: [int]):
        return self._findByIds(transaction, ids, self._constants.SQL_FILES.USERS_FIND_BY_IDS)

    def findByEmail(self, transaction: Transaction, email):
        queryFileName = self._constants.SQL_FILES.USERS_FIND_BY_EMAIL
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(email=email)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()

    def getAllAndCount(self, transaction: Transaction, **kwargs):
        queryFileName = self._constants.SQL_FILES.USERS_GET_ALL
        query = self._getSqlQueryFromFile(queryFileName)

        settings = getAllSettings.copy()

        if "limit" in kwargs.keys():
            settings["limit"] = kwargs["limit"]
        if "offset" in kwargs.keys():
            settings["offset"] = kwargs["offset"]
        if "first_name" in kwargs.keys() and kwargs["first_name"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"u.first_name ILIKE '%{kwargs['first_name']}%'"
        if "last_name" in kwargs.keys() and kwargs["last_name"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"u.last_name ILIKE '%{kwargs['last_name']}%'"
        if "email" in kwargs.keys() and kwargs["email"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"u.email = '{kwargs['email']}'"
        if "ageLower" in kwargs.keys() and kwargs["ageLower"] != "":
            self.handleWhereStatement(settings)
            lower_bound = kwargs["ageLower"]
            settings["where"] = settings["where"] + f"u.age >= {lower_bound}"
        if "ageUpper" in kwargs.keys() and kwargs["ageUpper"] != "":
            self.handleWhereStatement(settings)
            upper_bound = kwargs["ageUpper"]
            settings["where"] = settings["where"] + f"u.age <= {upper_bound}"
        if "gender" in kwargs.keys() and kwargs["gender"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"u.gender = '{kwargs['gender']}'"
        if "country" in kwargs.keys() and kwargs["country"] != "":
            self.handleWhereStatement(settings)
            settings["where"] = settings["where"] + f"u.country = '{kwargs['country']}'"
        query = query.format(**settings)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    def addUser(self, transaction: Transaction, user: dict):
        queryFileName = self._constants.SQL_FILES.USERS_ADD_USER
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(user)
        query = query.format(**user)
        transaction.cursor.execute(query, user)
        user_id = transaction.cursor.fetchone()[0]
        return user_id

    def updateUser(self, transaction: Transaction, user: dict):
        queryFileName = self._constants.SQL_FILES.USERS_UPDATE_USER_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        self.replaceDoubleApostrophes(user)
        query = query.format(**user)
        transaction.cursor.execute(query, user)
        user_id = transaction.cursor.fetchone()[0]
        return user_id

    def deleteUserById(self, transaction: Transaction, id: int):
        queryFileName = self._constants.SQL_FILES.USERS_DELETE_USER_BY_ID
        return self._deleteById(transaction, id, queryFileName)

    def getDistinctCountry(self, transaction: Transaction):
        queryFileName = self._constants.SQL_FILES.GET_DISTINCT_COUNTRY
        query = self._getSqlQueryFromFile(queryFileName)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()
