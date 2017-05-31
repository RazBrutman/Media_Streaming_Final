import sqlite3
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


    def static_users_for_test(self):
        static_users = [['Raz', '10.0.0.8', ["D:\Music\green_day_holiday.mp3",
                                             "D:\Movies\sample.avi"]],
                        ['Gai', '10.0.0.4', ["C:\Users\gai\Downloads\RONDO.mp3",
                                             "C:\Users\gai\Downloads\NET.mp4",
                                             "C:\Downloads\Rey.mp4"]],
                        ['Yuval', '10.0.0.10', ["C:\Music\pentatonix_song.mp3",
                                                "C:\Movies\Frozen.mp4"]],
                        ['Baruch', '10.0.0.7', ["C:\My_music\Beethoven_fifth.mp3",
                                                "C:\Personal\Movies\Jason_bourne.avi",
                                                "C:\Personal\Movies\Jason_bourne_2.avi"]]]
        static_relationships = [('Raz', 'Gai'),
                                ('Raz', 'Yuval'),
                                ('Raz', 'Baruch'),
                                ('Gai', 'Baruch'),
                                ('Yuval', 'Baruch')]

        for user in static_users:
            self.add_user(user[0], user[1])
            for file in user[2]:
                self.add_file(file, user[0])

        for rel in static_relationships:
            print rel[0], rel[1]
            self.add_relationship(rel[0], rel[1])

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
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username == '" + u1 + "'")
        u1ID = self.c.fetchone()[0]
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username == '" + u2 + "'")
        u2ID = self.c.fetchone()[0]
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

    def get_friends(self, username):
        self.c.execute("SELECT ID FROM USERTABLE WHERE Username = '" + username + "'")
        user_id = self.c.fetchone()[0]
        if user_id:
            self.c.execute("SELECT * FROM FRIENDSTABLE WHERE (F1ID = " + str(user_id) + " OR F2ID = " + str(user_id) + ")")
            friends = [x[1] if x[0] == user_id else x[0] for x in self.c.fetchall()]
            to_return = []
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