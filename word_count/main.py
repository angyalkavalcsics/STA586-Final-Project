import numpy as np
import argparse
import sqlite3
import math
import pathlib

# https://docs.python.org/3/library/argparse.html
def get_arguments():
    # Todo better description
    parser = argparse.ArgumentParser(description="Word counter")

    parser.add_argument(
        "action",
        help="action to be preformed on the database. Can be one of [init, matrix]",
    )

    parser.add_argument(
        "database",
        help="filename to the database. If DB not present, one will be created",
    )

    parser.add_argument(
        "-f", metavar="filename", dest="filename", help="filename to the input file"
    )

    return parser.parse_args()


def initalize_database(connection):
    db = connection.cursor()
    current_dir = pathlib.Path(__file__).parent
    with open(str(current_dir) + "/init.sql", "r", encoding="utf-8") as file:
        # https://stackoverflow.com/questions/8369219/how-to-read-a-text-file-into-a-string-variable-and-strip-newlines
        data = file.read().replace("\n", "")
        db.executescript(data)
    connection.commit()


def count_single(word):
    # Add word to word_id listing
    db.execute(
        "INSERT INTO words VALUES (?, NULL) ON CONFLICT (word) DO NOTHING", (word,)
    )

    # Add the word to our count
    db.execute(
        """
    INSERT INTO counts (word_id, word_count)
        SELECT word_id, 1 AS word_count
        FROM words
        WHERE word = ?
    ON CONFLICT (word_id) DO UPDATE SET
        word_count = 1 + counts.word_count
    """,
        (word,),
    )


def insert_words(first, second, table):
    # Assumes words are already in the `words` table
    db.execute(
        """
    INSERT INTO {} (first_id, second_id, pair_count)
        SELECT
            w1.word_id AS first_id,
            w2.word_id AS second_id,
            1 AS pair_count
        FROM words w1
        CROSS JOIN words w2
        WHERE
            w1.word = ?
            AND w2.word = ?
    ON CONFLICT (first_id, second_id) DO UPDATE SET
        pair_count = 1 + {}.pair_count
    """.format(
            table, table
        ),
        (first, second),
    )


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

        if i - 1 >= 0:
            last_word = words[i - 1]
            insert_words(last_word, this_word, "no_gap")

        if i - 2 >= 0:
            two_ago = words[i - 2]
            insert_words(two_ago, this_word, "one_gap")


def load_file_filename(filename, db, db_connection):

    with open(arguments.filename, "r", encoding="utf-8") as file:
        total_lines = lines_in_file(arguments.filename)
        counter = line_counter(total_lines, 1000)

        # Todo, clean each line
        for line in file:
            add_line_to_database(line)
            next(counter)

        db_connection.commit()


arguments = get_arguments()
db_connection = sqlite3.connect(arguments.database)
db = db_connection.cursor()

initalize_database(db_connection)

if arguments.action == "init" and arguments.filename:
    load_file_filename(arguments.filename, db, db_connection)
elif arguments.action == "init" and not arguments.filename:
    print("You must supply a filename with -f")
elif arguments.action == "matrix":
    print()
