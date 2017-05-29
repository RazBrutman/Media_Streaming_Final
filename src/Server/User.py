# -*- coding: utf-8 -*-
import json
import pickle

class User(object):

    def __init__(self, username, ip, list_of_media=()):
        self.username = username
        self.ip = ip
        self.files = list_of_media

    def set_media(self, list_of_media):
        self.files = list_of_media


class SharedMedia(object):

    def __init__(self, path):
        self.abs_path = path
        self.type = path.split(".")[-1]


class MyTestData(object):

    def __init__(self):
        self.users = [User('Raz', '10.0.0.8', ["D:\Music\green_day_holiday.mp3", "D:\Movies\sample.avi"]),
                      User('Gai', '10.0.0.4', ["C:\Downloads\RONDO.mp3", "C:\Downloads\NET.mp4"])]

    def get(self):
        return pickle.dumps(self.users)