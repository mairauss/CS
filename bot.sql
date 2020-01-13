DROP TABLE Resource;
DROP TABLE Reservation;

CREATE TABLE Resource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
);


CREATE TABLE Reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    reservedBy INTEGER,
    date DATE,
    resourceId INTEGER,
    time TEXT,
    CONSTRAINT fk_Resource
        FOREIGN KEY (resourceId)
        REFERENCES Resource(resourceId)
        ON DELETE CASCADE
);

/* Fake data set */

INSERT INTO Resource(name, description) VALUES("Ping-pong Table 1", "test");
INSERT INTO Resource(name, description) VALUES("Ping-pong Table 2", "test");
INSERT INTO Resource(name, description) VALUES("Ping-pong Table 3", "test");
INSERT INTO Resource(name, description) VALUES("Ping-pong Table 4", "test");

INSERT INTO Resource(name, description) VALUES("BBQ area 1", "test");
INSERT INTO Resource(name, description) VALUES("BBQ area 2", "test");
INSERT INTO Resource(name, description) VALUES("BBQ area 3", "test");
INSERT INTO Resource(name, description) VALUES("BBQ area 4", "test");


INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 1, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 1, "09:30");

INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 2, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 2, "09:00");

INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 3, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 3, "09:00");


INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 4, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 4, "09:00");

INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 5, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 5, "09:00");

INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 6, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 6, "09:00");

INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 7, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 7, "09:00");

INSERT INTO Reservation(date, resourceId, time) VALUES ("15.11.2019", 8, "09:00");
INSERT INTO Reservation(date, resourceId, time) VALUES ("16.11.2019", 8, "09:00");

/* Data to test function getReservedBy */ 
INSERT INTO Reservation(date, resourceId, reservedBy) VALUES ("17.11.2019", 8, 5);
INSERT INTO Reservation(date, resourceId, reservedBy) VALUES ("18.11.2019", 8, 5);

/* Data to test function getReservedBy for sergey */ 
INSERT INTO Reservation(date, resourceId, reservedBy) VALUES ("19.11.2019", 7, 1012086922);
INSERT INTO Reservation(date, resourceId, reservedBy) VALUES ("20.11.2019", 6, 1012086922);

/* Select statemens used in SQLiteHandler */
SELECT * FROM Resource;
SELECT * FROM Reservation;

SELECT Resource.id AS resourceId, Resource.name, Reservation.id AS reservationId, date FROM Resource
INNER JOIN Reservation ON Resource.id = Reservation.resourceId
WHERE Reservation.ReservedBy = 5;