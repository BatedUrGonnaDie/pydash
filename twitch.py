#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import socket
import os
import re
import Queue
from PySide.QtCore      import *

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'

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
            return False

    def check_partner_status(self):
        endpoint = "/user"
        info = self.api_call("get", endpoint = endpoint)
        if info:
            return info["partnered"]
        else:
            return False

    def json_decode(self, json_object):
        if json_object.status_code == 200:
            json_decode = json_object.json()
            return json_decode
        else:
            return False

    def api_call(self, method, endpoint, data = None):
        url = self.base_url + endpoint

        if method == "get":
            info = requests.get(url, headers = self.headers)
        elif method == "post":
            info = requests.post(url ,headers = self.headers, data = data)
        elif method == "put":
            info = requests.put(url, headers = self.headers, data = data)
        else:
            return -1

        info_decode = self.json_decode(info)
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
        params = {u"channel[status]" : title, u"channel[game]" : game}
        return_info = self.api_call("put", endpoint, params)
        return return_info

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
            success = self.api_call("post", endpoint, new_info)
            if success:
                self.last_commercial = int(time.time())
            return success

class Chat:

    show_new_message = Signal(str, str, str)

    def __init__(self, name, oauth, q):
        self.name = name
        self.oauth = "oauth:" + oauth
        self.q = q
        self.running = False

    def connect(self):
        twitch_host = "irc.twitch.tv"
        twitch_port = 6667
        self.irc = socket.socket()
        self.irc.connect((twitch_host, twitch_port))

    def irc_disconnect(self):
        try:
            self.irc.sendall("QUIT\r\n")
        except:
            pass
        self.irc.close()

    def send_irc_auth(self):
        self.irc.sendall("PASS {}\r\n".format(self.oauth))
        self.irc.sendall("NICK {}\r\n".format(self.name))

    def join_channel(self):
        self.irc.sendall("JOIN #{}\r\n".format(self.name))

    def establish_connection(self):
        self.connect()
        self.send_irc_auth()
        #self.irc.sendall("TWITCHCLIENT 3\r\n")
        time.sleep(1)
        self.join_channel()

    def parse_msg(self, msg):
        pass
        #return sender, msg, maybe color

    def send_msg(self, txt):
        pass

    def main_loop(self):
        self.establish_connection()
        self.running = True

        while self.running:
            message = self.irc.recv(4096)
            if message:
                if message.startswith("PING"):
                    self.irc.sendall("PONG tmi.twitch.tv\r\n")

                if message == "":
                    self.irc_disconnect()
                    self.establish_connection()

                message = message[:-2]
                message_parts = re.split("^:([a-z]+)!.+ PRIVMSG #\w+ :(.+)", message)
                if len(message_parts) != 1:
                    sender = message_parts[1]
                    msg = message_parts[2]
                    self.q.put([sender, "#000000", msg])
                else:
                    continue

