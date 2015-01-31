#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import socket
import os
import shutil
import re
import Queue
import time

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'

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
        if info:
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
            raise Exception

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

    def __init__(self, name, oauth, q):
        self.channel = name
        self.oauth = "oauth:" + oauth
        self.q = q
        self.running = False
        self.badges = {}
        self.emotes_dict = {}
        self.ffz_url = "http://cdn.frankerfacez.com/channel"
        self.ffz_emotes = []
        self.ffz_dict = {}
        self.custom_mod = False

    def init_icons(self, partner, start_loop_func):
        self.ffz_check()
        self.get_chat_badges()
        if partner:
            self.get_sub_badge()
        start_loop_func()

    def ffz_check(self):
        url = "{}/{}.css".format(self.ffz_url, self.channel)
        data = requests.get(url)
        if data.status_code == 200:
            if "!important" in data.text:
                self.custom_mod = True

            lines = data.text.split("\r\n")
            for i in lines:
                mod_line = ' '.join(i.split(' ')[1:])[1:-1]
                emote = re.findall('content: "(.+)";', i)[0]
                self.ffz_emotes.append(emote)

    def save_chat_badges(self, url, key, f_name):
        image = requests.get(url, stream = True)
        with open(f_name, "wb") as i_file:
            shutil.copyfileobj(image.raw, i_file)
        self.badges[key] = f_name

    def get_chat_badges(self):
        bc_url = "http://chat-badges.s3.amazonaws.com/broadcaster.png"
        self.save_chat_badges(bc_url, "broadcaster", "images/broadcaster_icon.png")

        if self.custom_mod:
            mod_url = self.ffz_url + "/" + self.channel + "/mod_icon.png"
        else:
            mod_url = "http://chat-badges.s3.amazonaws.com/mod.png"
        self.save_chat_badges(mod_url, "mod", "images/mod_icon.png")

        staff_url = "http://chat-badges.s3.amazonaws.com/staff.png"
        self.save_chat_badges(staff_url, "staff", "images/staff_icon.png")

        global_url = "http://chat-badges.s3.amazonaws.com/globalmod.png"
        self.save_chat_badges(global_url, "global_mod", "images/global_mod.png")

        turbo_url = "http://chat-badges.s3.amazonaws.com/turbo.png"
        self.save_chat_badges(turbo_url, "turbo", "images/turbo_icon.png")

    def get_sub_badge(self):
        url = "https://api.twitch.tv/kraken/chat/{}/badges".format(self.channel)
        badge_links = requests.get(url)
        self.save_chat_badges(badge_links["subscriber"]["image"], "subscriber", "images/sub_icon.png")

    def connect(self):
        twitch_host = "irc.twitch.tv"
        twitch_port = 6667
        self.irc = socket.socket()
        self.irc.connect((twitch_host, twitch_port))

    def irc_disconnect(self):
        try:
            self.irc.sendall("QUIT\r\n")
        except Exception:
            pass
        self.irc.close()

    def send_irc_auth(self):
        self.irc.sendall("PASS {}\r\n".format(self.oauth))
        self.irc.sendall("NICK {}\r\n".format(self.channel))

    def join_channel(self):
        self.irc.sendall("JOIN #{}\r\n".format(self.channel))
        self.irc.sendall('CAP REQ :twitch.tv/tags\r\n')

    def establish_connection(self):
        self.connect()
        self.send_irc_auth()
        success = self.irc.recv(4096)
        if success == ":tmi.twitch.tv NOTICE * :Login unsuccessful\r\n":
            raise Exception
        time.sleep(1)
        self.join_channel()
        self.q.put('<div style="margin-top: 2px; margin-bottom: 2px; color: #858585;">Connected to chat!</div>')

    def send_msg(self, txt):
        self.irc.sendall("PRIVMSG #{} :{}\r\n".format(self.channel, txt))
        return True

    def get_emote_key(self, key, e_dict, url):
        try:
            image_file = e_dict[key]
        except KeyError:
            print url
            image = requests.get(url, stream = True)
            with open("images/" + key + ".png", 'wb') as i_file:
                image.raw.decode_content = True
                shutil.copyfileobj(image.raw, i_file)
            image_file = e_dict[key] = "images/" + key + ".png"
        return image_file

    def badge_html(self, badge_file):
        return '<img src="{}" height="18" width="18" /> '.format(badge_file)

    def twitch_badges(self, msg_dict):
        badges = ''
        m_tags = msg_dict["tags"]

        if msg_dict["sender"] == self.channel:
            badges += self.badge_html(self.badges["broadcaster"])
        elif m_tags["user_type"]:
            if m_tags["user_type"] == "staff":
                badges += self.badge_html(self.badges["staff"])
            elif m_tags["user_type"] == "admin":
                badges += self.badge_html(self.badges["admin"])
            elif m_tags["user_type"] == "global_mod":
                badges += self.badge_html(self.badges["global_mod"])
            elif m_tags["user_type"] == "mod":
                badges += self.badge_html(self.badges["mod"])

        if m_tags["turbo"] == '1':
            badges += self.badge_html(self.badges["turbo"])
        if m_tags["subscriber"] == '1':
            badges += self.badge_html(self.badges["subscriber"])

        return badges

    def twitch_emote_parse(self, msg, e_tags):
        if not e_tags["emotes"]:
            return msg

        emotes = []
        e_array = e_tags["emotes"].split('/')

        for i in e_array:
            tmp = i.split(':')
            emotes.append({tmp[0] : tmp[1]})

        emotes_long = []
        for i in emotes:
            for k, v in i.iteritems():
                tmp = v.split(',')
                for i in tmp:
                    emotes_long.append({k : i})

        emotes_sorted = sorted(emotes_long, key=lambda k: int(k.values()[0].split('-')[0]), reverse=True) 
        for i in emotes_sorted:
            for k, v in i.iteritems():
                emote_url = "http://static-cdn.jtvnw.net/emoticons/v1/{}/1.0".format(k)
                image_file = self.get_emote_key(k, self.emotes_dict, emote_url)
                emote_replace = '<img src="{}" />'.format(image_file)
                e_range = v.split('-')
                msg = msg[0:int(e_range[0])] + emote_replace + msg[(int(e_range[1]) + 1):]

        return msg

    def ffz_parse(self, msg):
        for i in self.ffz_emotes:
            if i in msg:
                emote_url = self.ffz_url + '/' + self.channel + '/' + i + ".png"
                image_file = self.get_emote_key(i, self.ffz_emotes, emote_url)
                emote_replace = '<img src="{}" />'.format(image_file)
                msg = msg.replace(i, emote_replace)
        return msg

    def parse_msg(self, msg_dict):
        badges = self.twitch_badges(msg_dict)
        twitch_e_msg = self.twitch_emote_parse(msg_dict["message"], msg_dict["tags"])
        twitch_ffz_msg = self.ffz_parse(twitch_e_msg)
        msg_time = self.get_timestamp()
        final_msg = '<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> {}<span style="color: {};">{}</span>: {}</div>'\
                    .format(msg_time, badges, msg_dict["tags"]["color"], msg_dict["sender"], twitch_ffz_msg)
        return final_msg

    def get_timestamp(self):
        msg_time = time.strftime("%I:%M")
        if msg_time.startswith('0'):
            msg_time = msg_time[1:]
        return msg_time

    def main_loop(self):
        self.establish_connection()
        self.running = True

        while self.running:
            message = self.irc.recv(4096)
            if message:
                if message.startswith("PING"):
                    self.irc.sendall("PONG tmi.twitch.tv\r\n")
                    continue

                if message == "":
                    self.irc_disconnect()
                    self.establish_connection()
                    continue
                elif message.startswith(":jtv!"):
                    message = message.strip()
                    msg_type = message.split(' ')
                    print msg_type
                    if msg_type[1] == "PRIVMSG" and msg_type[2] == self.channel:
                        send_msg = ' '.join(msg_type[3:])[1:]
                        self.q.put('<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> <span style="color: #858585;">{}</span></div>'\
                                   .format(self.get_timestamp(), send_msg))
                        continue

                try:
                    action = message.split(' ')[2]
                except:
                    print message
                    continue
                if action == "PRIVMSG":
                    msg_parts = message.split(' ')
                    c_msg = {}
                    c_msg["tags"] = dict(item.split('=') for item in msg_parts[0][1:].split(';'))
                    c_msg["sender"] = msg_parts[1][1:].split('!')[0]
                    c_msg["action"] = msg_parts[2]
                    c_msg["channel"] = msg_parts[3]
                    c_msg["message"] = ' '.join(msg_parts[4:])[1:].strip()
                    print c_msg
                    self.q.put(self.parse_msg(c_msg))
