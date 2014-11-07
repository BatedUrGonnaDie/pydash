#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import json
import webbrowser

redirect_url = "https://leagueofnewbs.com/twitch/dashboard/out"

class Configurer:

    def __init__(self):
        pass
        
    def open_file(self, open_type):
        with open("config.json", open_type) as config_file:
            user_config = json.load(config_file, encoding = "utf-8")
        return user_config

    def dump_file(self, user_object, open_type):
        with open('config.json', open_type) as config_file:
            json.dump(user_object, config_file, sort_keys = True, indent = 4, ensure_ascii=False, encoding = "utf-8")

    def load_file(self):

        try:
            user_config = self.open_file('r')
        except:
            user_config = {"channel" : "", "oauth" : "", "max_viewers" : 0}
            self.dump_file(user_config, 'w')
            webbrowser.open(redirect_url, new = 2)
            #if you are worried about me saving any of your info the source is at https://github.com/batedurgonnadie/salty_web

        return user_config

    def set_param(self, param, info):
        config_tmp = self.open_file('r')
        config_tmp[param] = info
        self.dump_file(config_tmp, 'w')
        return config_tmp


    def get_auth_code(self):
        webbrowser.open(redirect_url, new = 1)
