# -*- coding: utf-8 -*-
'''
@author: redstar
'''
import datetime


def now(formater="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(formater)
