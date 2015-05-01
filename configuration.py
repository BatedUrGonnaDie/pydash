#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import logging
import webbrowser

redirect_url = "https://leagueofnewbs.com/twitch/pydash/out"

class Configurer(object):

    def __init__(self):
        pass

    def open_file(self, open_type):
        try:
            with open("config.json", open_type) as config_file:
                user_config = json.load(config_file, encoding = "utf-8")
            return user_config
        except IOError:
            raise
        except Exception, e:
            logging.exception(e)
            return False

    def dump_file(self, user_object, open_type):
        with open('config.json', open_type) as config_file:
            json.dump(user_object, config_file, sort_keys=True, indent=4, ensure_ascii=False, encoding="utf-8")

    def load_file(self):
        user_default = {"channel": "", "oauth": "", "twitch_id": 0, "max_viewers": 0, "position": [0, 0], "debug": True}
        try:
            user_config = self.open_file('r')
            user_default.update(user_config)
        except IOError:
            self.dump_file(user_default, 'w')
            user_config = user_default
            logging.info("New Config File Created")
        if user_config != user_default:
            self.dump_file(user_default, 'w')
            logging.info("New config option added to the file")
        return user_default

    def get_completer_list(self):
        try:
            with open("games_list.txt", 'r') as games_file:
                games_list = games_file.readlines()
            for i in range(len(games_list)):
                games_list[i] = games_list[i][:-1]
            return games_list
        except Exception, e:
            logging.exception(e)
            return False

    def set_param(self, param, info):
        config_tmp = self.open_file('r')
        config_tmp[param] = info
        self.dump_file(config_tmp, 'w')
        return config_tmp


    def get_auth_code(self):
        webbrowser.open(redirect_url, new=1)
