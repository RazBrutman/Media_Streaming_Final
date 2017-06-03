
def static(self):
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
        self.edit_relationship(rel[0], rel[1], "False")