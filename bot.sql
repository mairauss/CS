CREATE TABLE Resource (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);


CREATE TABLE Reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    reservedBy INTEGER,
    date DATE,
    resourceId INTEGER,
    CONSTRAINT fk_Resource
        FOREIGN KEY (resourceId)
        REFERENCES Resource(resourceId)
        ON DELETE CASCADE
);

/* Fake data set */

INSERT INTO Resource(name) VALUES("Ping-pong Table 1");
INSERT INTO Resource(name) VALUES("Ping-pong Table 2");
INSERT INTO Resource(name) VALUES("Ping-pong Table 3");
INSERT INTO Resource(name) VALUES("Ping-pong Table 4");

INSERT INTO Resource(name) VALUES("BBQ area 1");
INSERT INTO Resource(name) VALUES("BBQ area 2");
INSERT INTO Resource(name) VALUES("BBQ area 3");
INSERT INTO Resource(name) VALUES("BBQ area 4");


INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 1);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 1);

INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 2);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 2);

INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 3);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 3);


INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 4);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 4);

INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 5);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 5);

INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 6);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 6);

INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 7);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 7);

INSERT INTO Reservation(date, resourceId) VALUES ("15.11.2019", 8);
INSERT INTO Reservation(date, resourceId) VALUES ("16.11.2019", 8);

/* Data to test function getReservedBy */ 
INSERT INTO Reservation(date, resourceId, reservedBy) VALUES ("17.11.2019", 8, 5);
INSERT INTO Reservation(date, resourceId, reservedBy) VALUES ("18.11.2019", 8, 5);

/* Select statemens used in SQLiteHandler */
SELECT * FROM Resource;

SELECT Resource.id AS resourceId, Resource.name, Reservation.id AS reservationId, date FROM Resource
INNER JOIN Reservation ON Resource.id = Reservation.resourceId
WHERE Reservation.ReservedBy = 5;