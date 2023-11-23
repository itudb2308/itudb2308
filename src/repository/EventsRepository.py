import sqlite3
from repository.BaseRepository import BaseRepository

class EventsRepository(BaseRepository):

    def __init__(self, connection: sqlite3.Connection):
        super().__init__(connection)

    def findById(self, id: int):
        queryFileName = self._constants.SQL_FILES.EVENTS_FIND_BY_ID
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(id=id)

        return self.cursor.execute(query).fetchall()[0]

    
    def findByIds(self, ids: [int]):
        queryFileName = self._constants.SQL_FILES.EVENTS_FIND_BY_IDS
        query = self._getSqlQueryFromFile(queryFileName)
        query = query.format(ids=','.join(map(str,ids)))

        return self.cursor.execute(query).fetchall()
