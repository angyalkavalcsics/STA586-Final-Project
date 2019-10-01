CREATE TABLE IF NOT EXISTS words (
    word TEXT NOT NULL,
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    CONSTRAINT original_words UNIQUE (word)
);

CREATE TABLE IF NOT EXISTS counts (
    word_id INTEGER PRIMARY KEY,
    word_count INT NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words (word_id)

);

CREATE TABLE IF NOT EXISTS no_gap (
    first_id INTEGER NOT NULL,
    second_id INTEGER NOT NULL,
    pair_count INT NOT NULL,
    PRIMARY KEY (first_id, second_id),
    FOREIGN KEY (first_id) REFERENCES words (word_id),
    FOREIGN KEY (second_id) REFERENCES words (word_id)
);

CREATE TABLE IF NOT EXISTS one_gap (
    first_id INTEGER NOT NULL,
    second_id INTEGER NOT NULL,
    pair_count INT NOT NULL,
    PRIMARY KEY (first_id, second_id),
    FOREIGN KEY (first_id) REFERENCES words (word_id),
    FOREIGN KEY (second_id) REFERENCES words (word_id)
);