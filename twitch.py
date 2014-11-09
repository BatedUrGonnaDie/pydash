#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import socket

scope = ["user_read", "channel_editor", "channel_commercial", "chat_login"]

class API:

    def __init__(self, token, channel = ""):
        self.oauth_token = token
        self.channel = channel
        self.base_url = "https://api.twitch.tv/kraken"
        self.last_commercial = 0
        self.headers = {}

    def set_headers(self, oauth):
        self.headers = {"Accept" : "application/vnd.twitchtv.v3+json", "Authorization" : "OAuth " + oauth}

    def check_auth_status(self):
        endpoint = '/'
        info = self.api_call("get", endpoint = endpoint)
        if info["token"]["valid"] and info["token"]["authorization"]["scopes"] == scope:
            return info
        else:
            #status thing
            return False

    def check_partner_status(self):
        endpoint = "/user"
        info = self.api_call("get", endpoint = endpoint)
        if info:
            return info["partnered"]
        else:
            return False

    def json_decode(self, json_object):
        # if json_object.status_code == 200:
        #     json_decode = json_object.json()
        #     return json_decode
        # else:
        #     return False
        return json_object.json()

    def api_call(self, method, endpoint, data = None):
        url = self.base_url + endpoint
        print url
        print data
        if method == "get":
            info = requests.get(url, headers = self.headers)
        elif method == "post":
            info = requests.post(url ,headers = self.headers, data = data)
        elif method == "put":
            info = requests.put(url, headers = self.headers, data = data)
        else:
            return -1

        info_decode = self.json_decode(info)
        print info_decode
        return info_decode

    def get_gt(self):
        endpoint = "/channels/" + self.channel
        info = self.api_call("get", endpoint = endpoint)
        if info:
            return info["status"], info["game"]
        else:
            return False, False

    def set_gt(self, title, game):
        endpoint = "/channels/" + self.channel
        new_info = {"channel" : {"status" : title, "game" : game}}
        return_info = self.api_call("put", endpoint, new_info)
        print return_info
        return True if return_info else False

    def get_stream_object(self):
        endpoint = "/streams/" + self.channel
        info = self.api_call("get", endpoint = endpoint)
        if info:
            return info
        else:
            return False

    def run_commercial(self, length):
        if time.time() - self.last_commercial > 480:
            new_info = {"length" : length}
            endpoint = "/channels/{}/commercial".format(self.channel)
            self.api_call("post", endpoint, new_info)
            self.last_commercial = int(time.time())

class Chat:

    def __init__(self, name, oauth):

        self.name = name
        self.oauth = oauth

    def connect(self):
        pass

    def join_channel(self, channel):
        pass

    def parse_msg(self, msg):
        pass
        #return sender, msg, maybe color

    def send_msg(self, txt):
        pass
