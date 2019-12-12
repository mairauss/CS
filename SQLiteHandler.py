from typing import Any, List, Dict
import sqlite3

class SqliteConnection:
    def __init__(self, pathToDBFile: str):
        self.conn: Any = sqlite3.connect(pathToDBFile)
        self.cursor: Any = self.conn.cursor()


class SQLiteHandler:
    def __init__(self):
        self.pathToDBFile = "./data/data.db"

    def getDBConnection(self) -> Any:
        return SqliteConnection(self.pathToDBFile)

    def getAllResources(self) -> List[Dict]:
        cursor: Any = self.getDBConnection().cursor
        resources: List[Dict] = []
        query: str = "SELECT * FROM Resource"
        cursor.execute(query)
        rows: List[List] = [x for x in cursor]
        columns: List[str] = [x[0] for x in cursor.description]
        for row in rows:
            dictObject: Dict = {}
            for index, column in enumerate(columns):
                dictObject[column] = row[index]
            resources.append(dictObject)
        return resources
    
    def getResourcesByUserId(self, userId: int) -> List[Dict]:
        cursor: Any = self.getDBConnection().cursor
        resources: List[Dict] = []
        query: str = """SELECT Resource.id AS resourceId, Resource.name, Reservation.id AS reservationId, date FROM Resource
                     INNER JOIN Reservation ON Resource.id = Reservation.resourceId
                     WHERE Reservation.ReservedBy = {}"""
        
        query = query.format(userId)
        cursor.execute(query)
        rows: List[List] = [x for x in cursor]
        columns: List[str] = [x[0] for x in cursor.description]
        for row in rows:
            dictObject: Dict = {}
            for index, column in enumerate(columns):
                dictObject[column] = row[index]
            resources.append(dictObject)
        return resources