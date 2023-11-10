from os.path import join as path_join

from RepositoryConstants import RepositoryConstants


class BaseRepository:
    _constants = RepositoryConstants

    # Get SQL Query From File
    def _getSqlQueryAndFormat(self, filePath: str):
        with open(path_join(self._constants.SQL_FOLDER_PATH, filePath)) as f:
            query = f.read()
        return query
