from os.path import join as path_join

from dto.Transaction import Transaction
from repository.RepositoryConstants import RepositoryConstants


class BaseRepository:
    _constants = RepositoryConstants

    def __init__(self, connection):
        self._connection = connection

    def handleWhereStatement(self, queryArguments):
        if len(queryArguments["where"]) == 0:
            queryArguments["where"] = "WHERE "
        else:
            queryArguments["where"] = queryArguments["where"] + " AND "

    # Get SQL Query From File
    def _getSqlQueryFromFile(self, filePath: str):
        with open(path_join(self._constants.SQL_FOLDER_PATH, filePath)) as f:
            query = f.read()
        return query

    # Generic Find By Id Method
    def _findById(self, transaction: Transaction, id: int, queryFileName):
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)

        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()

    # Generic Find By Ids Method
    def _findByIds(self, transaction: Transaction, ids: [int], queryFileName):
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids=",".join(map(str, ids)))
        transaction.cursor.execute(query)
        return transaction.cursor.fetchall()

    # Generic Delete Method
    def _deleteById(self, transaction: Transaction, id: int, queryFileName):
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)
        transaction.cursor.execute(query)
        return transaction.cursor.fetchone()[0]

    def replaceDoubleApostrophes(self, arguments: dict):
        for key, value in arguments.items():
            if isinstance(value, str):
                arguments[key] = value.replace("'", "''")

    def createNewTransaction(self) -> Transaction:
        return Transaction(self._connection)
