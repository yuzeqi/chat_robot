import os
import sqlite3

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
DATA_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "../data"))
DEST_FILE = os.path.join(DATA_DIRECTORY, "./rules")

conn = sqlite3.connect(os.path.join(DATA_DIRECTORY, "rule.db"))


def create_database():
    conn.execute('''
    CREATE TABLE IF NOT EXISTS keyword_rule
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    word VARCHAR(255),
    relate_resp integer )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS rule_resp
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    response text )
    ''')
    conn.commit()


def insert_word(word, response):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO keyword_rule(word, relate_resp) VALUES(?, ?)""", (word, response,))
    conn.commit()


def insert_resp(response):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO rule_resp(response) VALUES(?)""", (response,))
    id = cursor.lastrowid
    conn.commit()
    return id


def read_file(dest_file):
    fp = open(dest_file)
    for line in fp:
        words, resp = line.split(' ', 1)
        word_list = words.split(',')
        yield word_list, resp




if __name__ == "__main__":
    create_database()
    for res in read_file(DEST_FILE):
        word_list, resp = res
        cursor = conn.cursor()
        cursor.execute("select id from rule_resp where response like ?", (resp,))
        res = cursor.fetchone()
        if not res:
            rowid = insert_resp(resp)
        else:
            rowid = res[0]
        for word in word_list:
            insert_word(word, rowid)
