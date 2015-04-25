#! /usr/bin/env python2.7

import random

DEFAULT_COLORS = ["Blue", "BlueViolet", "CadetBlue", "Chocolate", "Coral", "DodgerBlue", "Firebrick", "GoldenRod", "Green", "HotPink", "OrangeRed", "Red", "SeaGreen", "SpringGreen", "YellowGreen"]

class User(object):

    def __init__(self, username, chat_color, display_name):
        self.name = username
        self.display_name = display_name.replace("\s", " ") if display_name is not "" else username
        self.chat_color = chat_color if chat_color is not "" else random.choice(DEFAULT_COLORS)
