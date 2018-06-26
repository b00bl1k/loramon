DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS messages;

CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deveui TEXT UNIQUE NOT NULL
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES devices (id)
);