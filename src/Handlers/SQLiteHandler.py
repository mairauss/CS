from typing import Any, List, Dict
import sqlite3
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class SqliteConnection:
    def __init__(self, pathToDBFile: str):
        self.conn: Any = sqlite3.connect(os.path.dirname(__file__) + pathToDBFile)
        self.cursor: Any = self.conn.cursor()


class SQLiteHandler:
    def __init__(self):
        self.pathToDBFile = "/data/data.db"

    def get_db_connection(self) -> SqliteConnection:
        return SqliteConnection(self.pathToDBFile)

    def get_all_Resources(self) -> List[Dict]:
        connection: SqliteConnection = self.get_db_connection()
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

    def get_resources_by_user_id(self, userId: int) -> List[Dict]:
        connection: SqliteConnection = self.get_db_connection()
        cursor: Any = connection.cursor
        resources: List[Dict] = []
        query: str = """SELECT Resource.id AS resourceId, Resource.name, Reservation.id AS reservationId, date, time FROM Resource
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

    def get_resource_description(self, resourceId: int):
        connection: SqliteConnection = self.get_db_connection()
        cursor: Any = connection.cursor
        query: str = "SELECT Resource.description FROM Resource WHERE Resource.id = " + str(resourceId)
        cursor.execute(query)
        desc = cursor.fetchone()[0]
        connection.conn.close()
        return desc

    def get_resource_schedule(self, resourceId: int) -> List[Dict]:
        connection: SqliteConnection = self.get_db_connection()
        cursor: Any = connection.cursor
        resources: List[Dict] = []
        query: str = "SELECT Reservation.date, Reservation.time FROM Reservation WHERE Reservation.resourceId = " + str(
            resourceId)
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

    def is_resource_booked(self, userId: int, resourceId: int, date: str, time: str) -> bool:
        connection: SqliteConnection = self.get_db_connection()
        cursor: Any = connection.cursor
        query: str = """SELECT id FROM Reservation WHERE date = ? and resourceId = ? and reservedBy = ? and time = ?;"""
        data_tuple = (date, resourceId, userId, time)
        cursor.execute(query, data_tuple)
        rows: List[List] = [x for x in cursor]
        connection.conn.close()
        if len(rows) > 0:
            return True
        else:
            return False

    def book_resource(self, userId: int, resourceId: int, date: str, time: str) -> bool:
        if self.is_resource_booked(userId, resourceId, date, time) is not True:
            connection: SqliteConnection = self.get_db_connection()
            cursor: Any = connection.cursor
            query: str = """INSERT INTO 'Reservation'('date', 'resourceId', 'reservedBy', 'time') VALUES (?, ?, ?, ?);"""
            data_tuple = (date, resourceId, userId, time)
            cursor.execute(query, data_tuple)
            logger.info(userId)
            connection.conn.commit()
            connection.conn.close()
            logger.info("booked")
            return True
        else:
            return False

    def delete_reservation(self, userId: int, reservationId: int):
        connection: SqliteConnection = self.get_db_connection()
        cursor: Any = connection.cursor
        query: str = "DELETE FROM Reservation WHERE id = " + str(reservationId) + " AND reservedBy = " + str(userId)
        cursor.execute(query)
        connection.conn.commit()
        connection.conn.close()
        logger.info("deleted")

    def modify_reservation(self, userId: int, reservationId: int, date: str, time: str):
        logger.info("in modifyReservation")
        connection: Any = self.get_db_connection()
        cursor: Any = connection.cursor
        cursor.execute('''UPDATE Reservation SET time = ? WHERE id = ? AND reservedBy = ?''',
                       (time, reservationId, userId))
        cursor.execute('''UPDATE Reservation SET date = ? WHERE id = ? AND reservedBy = ?''',
                       (date, reservationId, userId))
        connection.conn.commit()
        connection.conn.close()
        logger.info("modified")
