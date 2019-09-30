import numpy as np
import argparse
import sqlite3
import math

# https://docs.python.org/3/library/argparse.html
def get_arguments():
    # Todo better description
    parser = argparse.ArgumentParser(description="Word counter")
    parser.add_argument(
        "-f",
        metavar="filepath",
        dest="filepath",
        required=True,
        help="filepath to the input file",
    )

    parser.add_argument(
        "-d",
        metavar="database",
        dest="database",
        required=True,
        help="filepath to the database. If not present, one will be created",
    )

    return parser.parse_args()


def initalize_database(connection):
    db = connection.cursor()
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS word_count (
        word TEXT NOT NULL,
        count INT NOT NULL,
        PRIMARY KEY (word)
    )
    """
    )

    db.execute(
        """
    CREATE TABLE IF NOT EXISTS no_gap (
        first TEXT NOT NULL,
        second TEXT NOT NULL,
        count INT NOT NULL,
        PRIMARY KEY (first, second)
    )
    """
    )
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS one_gap (
        first TEXT NOT NULL,
        second TEXT NOT NULL,
        count INT NOT NULL,
        PRIMARY KEY (first, second)
    )
    """
    )
    connection.commit()


def count_single(word):
    db.execute("SELECT count FROM word_count WHERE word = ?", (word,))
    count = (db.fetchone() or (0,))[0]
    count += 1

    db.execute("INSERT OR REPLACE INTO word_count VALUES (?, ?)", (word, count))


def insert_words(first, second, table):
    query = "SELECT count FROM {} WHERE first = ? AND second = ?".format(table)
    db.execute(query, (first, second))
    count = (db.fetchone() or (0,))[0]
    count += 1

    query = "INSERT OR REPLACE INTO {} VALUES (?, ?, ?)".format(table)
    db.execute(query, (first, second, count))


# https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def lines_in_file(filename):
    def _make_gen(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)

    def rawgencount(filename):
        f = open(filename, "rb")
        f_gen = _make_gen(f.raw.read)
        return sum(buf.count(b"\n") for buf in f_gen)

    return rawgencount(filename)


def line_counter(total, hits):
    print_indexes = []
    for i in range(1, hits + 1):
        print_indexes += [(total // (hits + 1)) * i]
    print_indexes += [total + 1]

    i = 0
    while True:
        if print_indexes[0] == i:
            print_indexes = print_indexes[1:]
            print(
                "Processed line:",
                i,
                "out of",
                total,
                " ",
                round(i * 100 / total, 2),
                "% done",
            )
        yield
        i += 1

    return


def add_line_to_database(line):
    line = line.rstrip()  # Remove trailing newline
    words = line.lower().split(" ")
    num_words = len(words)
    for i in range(num_words - 1):
        this_word = words[i]

        # Always true
        if i + 0 <= num_words - 1:
            count_single(this_word)

        if i + 1 <= num_words - 1:
            next_word = words[i + 1]
            insert_words(this_word, next_word, "no_gap")

        if i + 2 <= num_words - 1:
            skip_word = words[i + 2]
            insert_words(this_word, skip_word, "one_gap")


arguments = get_arguments()
db_connection = sqlite3.connect(arguments.database)
db = db_connection.cursor()

initalize_database(db_connection)

with open(arguments.filepath, "r", encoding="utf-8") as file:
    total_lines = lines_in_file(arguments.filepath)
    counter = line_counter(total_lines, 1000)

    # Todo, clean each line
    for line in file:
        add_line_to_database(line)
        next(counter)

    db_connection.commit()
