from typing import Any, List, Dict
import sqlite3
import logging, unittest

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

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
        connection: Any = self.getDBConnection()
        cursor: Any = connection.cursor
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
        connection.conn.close()
        return resources
    
    def getResourcesByUserId(self, userId: int) -> List[Dict]:
        connection: Any = self.getDBConnection()
        cursor: Any = connection.cursor
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
        connection.conn.close()
        return resources

    def getResourceDescription(self, resourceId: int):
        connection: Any = self.getDBConnection()
        cursor: Any = connection.cursor
        query: str = "SELECT Resource.description FROM Resource WHERE Resource.id = " + str(resourceId)
        cursor.execute(query)
        desc = cursor.fetchone()[0]
        return desc

    def bookResource(self, userId: int, resourceId: int, date: str, time: str):
        connection: Any = self.getDBConnection()
        cursor: Any = connection.cursor
        query: str = """INSERT INTO 'Reservation'('date', 'resourceId', 'reservedBy', 'time') VALUES (?, ?, ?, ?);"""
        data_tuple = (date, resourceId, userId, time)
        cursor.execute(query, data_tuple)
        logger.info(userId)
        connection.conn.commit()
        connection.conn.close()
        logger.info("booked")

