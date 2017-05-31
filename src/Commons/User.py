# -*- coding: utf-8 -*-
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
