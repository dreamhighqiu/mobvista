# -*- coding: utf-8 -*-
'''
@author: redstar
'''
import base64


class Base64Coder():

    def __init__(self, obj):
        self.obj = obj

    def encode(self):
        if isinstance(self.obj, str):
            return base64.urlsafe_b64encode(self.obj)
        elif isinstance(self.obj, unicode):
            return base64.urlsafe_b64encode(self.obj.encode("utf-8"))
        elif isinstance(self.obj, file):
            return base64.b64encode(self.obj.read())
        else:
            return None

    def decode(self):
        if isinstance(self.obj, str):
            return base64.urlsafe_b64decode(self.obj)
        elif isinstance(self.obj, unicode):
            return base64.urlsafe_b64decode(self.obj.encode("utf-8"))
        elif isinstance(self.obj, file):
            return base64.b64decode(self.obj.read())
        else:
            return None
