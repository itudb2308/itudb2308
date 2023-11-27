from os.path import join as path_join
from repository.RepositoryConstants import RepositoryConstants


class BaseRepository:
    _constants = RepositoryConstants

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

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
    def _findById(self, id: int, queryFileName):
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id = id)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # Generic Find By Ids Method
    def _findByIds(self, ids: [int], queryFileName):
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids = ",".join(map(str, ids)))
        self.cursor.execute(query)
        return self.cursor.fetchall()
