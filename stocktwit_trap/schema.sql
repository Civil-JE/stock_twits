DROP TABLE IF EXISTS symbols;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS messages_symbols;

CREATE TABLE symbols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stocktwit_id INTEGER UNIQUE NOT NULL,
    symbol TEXT UNIQUE NOT NULL,
    active NUMERIC NOT NULL
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stocktwit_id INTEGER UNIQUE NOT NULL,
    body TEXT NOT NULL,
    sentiment TEXT NULL
);

CREATE TABLE messages_symbols_xref (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    symbol_id INTEGER NOT NULL,
    FOREIGN KEY (message_id) REFERENCES messages (stocktwit_id),
    FOREIGN KEY (symbol_id) REFERENCES symbols (stocktwit_id)
);
