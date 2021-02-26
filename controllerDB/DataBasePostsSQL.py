import sqlite3
import logging
from os.path import exists
from datetime import datetime


class SQLPost:

    def __init__(self, database):
        if not exists(database):
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            text = """CREATE TABLE "Posts" (
            "index"	INTEGER NOT NULL UNIQUE,
            "content"	TEXT,
            "comment"	TEXT,
            "date"	TEXT NOT NULL,
            PRIMARY KEY("index")
            );
            """
            self.cursor.execute(text)
            self.connection.commit()

        else:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()

    def add_post(self, index, content, comment, date=datetime.today()):
        text = "INSERT INTO Posts ('index', 'content', 'comment', 'date') VALUES(?,?,?,?)"
        values = (index, content, comment, date[:-6])
        with self.connection:
            try:
                self.cursor.execute(text, values)
                self.connection.commit()

            except:
                logging.error('duplication')

    def read_all_posts(self):
        text = "SELECT * FROM Posts"
        with self.connection:
            result = self.cursor.execute(text).fetchall()
        return result


class SQLBlackList:

    def __init__(self, database):
        if not exists(database):
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            text = """
            CREATE TABLE "Black_List" (
            "content"	TEXT NOT NULL UNIQUE
            );
            """
            self.cursor.execute(text)

        else:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()

    def add_black_list(self, url):
        text = "INSERT INTO Black_list (`content`) VALUES(?)"
        values = (url,)
        with self.connection:
            try:
                self.cursor.execute(text, values)
                self.connection.commit()
            except:
                pass

    def get_all(self):
        text = "SELECT * FROM Black_list"
        black_list = []
        with self.connection:
            result = self.connection.execute(text).fetchall()
            for i in result:
                black_list.append(i[0])

        return black_list


if __name__ == '__main__':
    pass