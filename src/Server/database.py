import sqlite3
import sys
sys.path.insert(0, '../Commons')
from User import User
import pickle


class database(object):
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.create_tables()
        # self.clear_tables()
        # self.static_users_for_test()
        # self.c.close()
        # self.conn.close()

    def create_tables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS USERTABLE(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "Username TEXT, "
                       "IP TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS FILETABLE(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "FileName TEXT, "
                       "FileType TEXT, "
                       "OwnerID INT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS FRIENDSTABLE(F1ID INT, "
                       "F2ID INT)")
        self.conn.commit()

    def clear_tables(self):
        self.c.execute("DELETE FROM USERTABLE")
        self.c.execute("DELETE FROM FILETABLE")
        self.c.execute("DELETE FROM FRIENDSTABLE")
        self.c.execute("DELETE FROM sqlite_sequence")
        self.conn.commit()

    def add_user(self, name, ip):
        self.c.execute("INSERT INTO USERTABLE VALUES (NULL, ?, ?)", (name, ip))
        self.conn.commit()

    def add_file(self, path, username):
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username == '" + username + "'")
        owner_id = self.c.fetchone()[0]
        file_type = path.split(".")[-1]
        self.c.execute("INSERT INTO FILETABLE VALUES (NULL, ?, ?, ?)", (path, file_type, owner_id))
        self.conn.commit()

    def add_relationship(self, u1, u2):
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username = '" + u1 + "'")
        u1ID = self.c.fetchone()[0]
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username = '" + u2 + "'")
        u2ID = self.c.fetchone()[0]
        self.c.execute("SELECT * FROM FRIENDSTABLE WHERE (F1ID = " + str(u1ID) + " AND F2ID = " + str(u2ID) +
                       ") OR (F1ID = " + str(u2ID) + " AND F2ID = " + str(u1ID) + ")")
        try:
            rel = self.c.fetchone()[0]
        except TypeError:
            self.c.execute("INSERT INTO FRIENDSTABLE VALUES (?, ?)", (u1ID, u2ID))
            self.conn.commit()

    def close_db(self):
        self.c.close()
        self.conn.close()

    def get_user(self, username, ip):
        self.c.execute("SELECT * FROM USERTABLE WHERE Username == '" + username + "'")
        user_info = self.c.fetchall()
        if not user_info:
            self.add_user(username, ip)
        else:
            self.c.execute("UPDATE USERTABLE SET IP = '" + ip + "' WHERE Username = '" + username + "'")
        return username

    def get_friends(self, username, *args):
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username = '" + username + "'")
        user_id = self.c.fetchone()
        if user_id:
            to_return = []
            if args:
                self.c.execute("SELECT * FROM USERTABLE WHERE ID <> " + str(user_id[0]))
                users = self.c.fetchall()
                for user in users:
                    to_return.append(User(user[1], user[2]))
            else:
                user_id = user_id[0]
                self.c.execute("SELECT * FROM FRIENDSTABLE WHERE (F1ID = " + str(user_id) + " OR F2ID = " + str(user_id) + ")")
                friends = [x[1] if x[0] == user_id else x[0] for x in self.c.fetchall()]
                for friend in friends:
                    self.c.execute("SELECT * FROM USERTABLE WHERE ID = " + str(friend))
                    data = self.c.fetchone()
                    to_return.append(User(data[1], data[2]))
            return pickle.dumps(to_return)

    def get_files(self, username):
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username == '" + username + "'")
        owner_id = self.c.fetchone()[0]
        self.c.execute("SELECT FileName FROM FILETABLE WHERE OwnerID == '" + str(owner_id) + "'")
        files = " ".join([x[0] for x in self.c.fetchall()])
        return files