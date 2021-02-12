import sqlite3
from os.path import exists
import os


class SQLiter:

    def __init__(self, database):

        first_path = database.split('/')
        path = first_path[:-1]
        path = '/'.join(path)

        if not exists(path):
            os.mkdir(first_path[1])
        if not exists(database):
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            text = """CREATE TABLE "Persons" (
            "id"	INTEGER NOT NULL UNIQUE,
            "name"	TEXT,
            "chat_id"	INTEGER NOT NULL UNIQUE,
            "Status"	BOOL NOT NULL,
            "first_connection"	BOOL NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
            self.cursor.execute(text)
            self.connection.commit()

        else:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()

    def add_member(self, name: str, chat_id: int, status=False, con=True):
        string = ("INSERT INTO Persons ('name', 'chat_id', 'Status', 'first_connection') VALUES(?,?,?,?)",
                  (name, chat_id, status, con))

        with self.connection:
            self.cursor.execute(string[0], string[1])
            self.connection.commit()

    def edit_status_subscribe_member(self, chat_id, status):
        string = "UPDATE Persons SET Status=? WHERE chat_id=?", (status, chat_id)
        with self.connection:
            self.cursor.execute(string[0], string[1])
            self.connection.commit()

    def getAllMembersStatusTrue(self, status=True):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Persons` WHERE `Status`=?", (status,)).fetchall()
            for i in result:
                yield i[2]

    def subscriber_exist(self, chat_id):
        string = "SELECT * FROM Persons WHERE chat_id=?", (chat_id,)
        result = self.cursor.execute(string[0], string[1]).fetchall()
        return bool(len(result))

    def close(self):
        self.connection.close()

    def delete(self, name):
        with self.connection:
            self.cursor.execute("DELETE FROM Persons WHERE name=?", (name,))

    def switch_status_connection(self, chat_id, status_connection=False):
        string = "UPDATE Persons SET first_connection=? WHERE chat_id=?", (status_connection, chat_id)
        with self.connection:
            self.cursor.execute(string[0], string[1])
            self.connection.commit()

    def cheak_status_connection(self, chat_id):
        string = "SELECT `first_connection` FROM `Persons` WHERE `chat_id`=?", (chat_id,)
        with self.connection:
            result = self.cursor.execute(string[0], string[1]).fetchall()
            if len(result) != 0:
                return bool(result[0][0])

    def getCountAllMembersTrue(self):
        pass

    def getCountAllMembersFalse(self):
        pass

    def get_Status(self, chat_id):
        text = "SELECT `Status` FROM `Persons` WHERE `chat_id`=?"
        values = (chat_id,)
        with self.connection:
            result = self.cursor.execute(text, values).fetchone()
            if result is None:
                return "Person doesn't exist"
            else:
                return bool(result[0])

    def getCountAllMembers(self):
        count = 0
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Persons`").fetchall()
        for i in result:
            count += 1
        return count


if __name__ == '__main__':
    # a = SQLiter('DATABASE/members.db')
    # print(a.subscriber_exist(575704682))
    # a.edit_status_subscribe_member(575704682, True)
    # # b = a.getAllMembersStatusTrue()
    # print(a.getCountAllMembers())
    # # print(a.cheak_status_connection(575704682))
    # print(a.switch_status_connection(575704682, True))
    # # print(a.cheak_status_connection(575704682))
    # print(a.get_Status(575704682))
    pass
