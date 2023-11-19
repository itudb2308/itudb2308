import sqlite3
from os.path import join as path_join
from repository.RepositoryConstants import RepositoryConstants


class BaseRepository:
    _constants = RepositoryConstants

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    # Get SQL Query From File
    def _getSqlQueryFromFile(self, filePath: str):
        with open(path_join(self._constants.SQL_FOLDER_PATH, filePath)) as f:
            query = f.read()
        return query
