CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    street_name TEXT NOT NULL,
    street_number TEXT NOT NULL,
    zip INTEGER NOT NULL,
    city TEXT NOT NULL,
    gender TEXT NOT NULL,
    user_since DATETIME NOT NULL,
    is_admin BOOLEAN NOT NULL,
    is_confirmed BOOLEAN NOT NULL,
    hash TEXT NOT NULL
);


CREATE TABLE bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    court INTEGER NOT NULL,
    date,
    start TEXT,
    end TEXT
);