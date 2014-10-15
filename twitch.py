#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import requests

class Twitch:

    def __init__(self, channel, token = ""):
        self.oauth_token = token
        self.channel = channel
        self.base_url = "https://api.twitch.tv/kraken"
        self.headers = {"Accept" : "application/vnd.twitchtv.v3+json"}

    def api_call_get(self, endpoint = ""):
        url = self.base_url + "{}/{}".format(endpoint, self.channel) if endpoint != "" else self.base_url
        data = requests.get(url, headers = self.headers)

    def api_call_post(self, endpoint, post_send):
        pass

    def get_game_and_title(self):
        pass

    def set_game_and_title(self, title, game):
        pass

    def run_commercial(self, length):
        pass
