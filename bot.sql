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


INSERT INTO Resource(name, description) VALUES("Washing machine 1", "One of the washing machine");
INSERT INTO Resource(name, description) VALUES("Washing machine 2", "One of the washing machine");
INSERT INTO Resource(name, description) VALUES("Dryer", "After using washing machine, you can use Dryer");
INSERT INTO Resource(name, description) VALUES("Ping-Pong Table", "Play Ping-Pong with you friend");

INSERT INTO Resource(name, description) VALUES("Sauna", "Go to Sauna to relax");
INSERT INTO Resource(name, description) VALUES("Basketball court", "Play basketball with your friends");
INSERT INTO Resource(name, description) VALUES("Treadmill", "Go to run");
INSERT INTO Resource(name, description) VALUES("BBQ area", "Make BBQ with your friends");


/* Select statemens used in SQLiteHandler */
SELECT * FROM Resource;
SELECT * FROM Reservation;

SELECT Resource.id AS resourceId, Resource.name, Reservation.id AS reservationId, date FROM Resource
INNER JOIN Reservation ON Resource.id = Reservation.resourceId
WHERE Reservation.ReservedBy = 5;