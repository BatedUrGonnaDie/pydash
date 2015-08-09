#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import logging
import os
import re
import shutil
import socket
import sys
import time

import requests

import user

os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(getattr(sys, "_MEIPASS", os.path.abspath(".")), "cacert.pem")
logging.error(os.environ["REQUESTS_CA_BUNDLE"])

class API(object):

    def __init__(self, token, channel = ""):
        self.oauth_token = token
        self.channel = channel
        self.base_url = "https://api.twitch.tv/kraken"
        self.last_commercial = 0
        self.headers = {"Accept" : "appliaction/vnd.twitchtv.v3+json", "Authorization": None}

    def set_oauth_header(self, oauth):
        self.headers["Authorization"] = "OAuth " + oauth

    def check_auth_status(self):
        endpoint = '/'
        info = self.api_call("get", endpoint=endpoint)
        if info:
            return info
        else:
            return False

    def get_twitch_id(self, username):
        endpoint = "/channels/{}".format(username)
        info = self.api_call("get", endpoint)
        return info

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

        try:
            if method == "get":
                info = requests.get(url, headers=self.headers)
            elif method == "post":
                info = requests.post(url, headers=self.headers, data=data)
            elif method == "put":
                info = requests.put(url, headers=self.headers, data=data)
            else:
                raise Exception
            info.raise_for_status()
            info_decode = self.json_decode(info)
            return info_decode
        except Exception, e:
            logging.exception(e)
            return False

    def get_gt(self):
        endpoint = "/channels/" + self.channel
        info = self.api_call("get", endpoint=endpoint)
        if info:
            return info["status"], info["game"]
        else:
            return False, False

    def set_gt(self, title, game):
        endpoint = "/channels/" + self.channel
        params = {u"channel[status]": title, u"channel[game]": game}
        return_info = self.api_call("put", endpoint, params)
        return return_info

    def get_stream_object(self):
        endpoint = "/streams/" + self.channel
        info = self.api_call("get", endpoint=endpoint)
        if info:
            return info
        else:
            return False

    def get_hosting_object(self, twitch_id):
        hosters = requests.get("https://tmi.twitch.tv/hosts?include_logins=1&target={}".format(twitch_id))
        return self.json_decode(hosters)

    def run_commercial(self, length):
        if time.time() - self.last_commercial > 480:
            new_info = {"length" : length}
            endpoint = "/channels/{}/commercial".format(self.channel)
            success = self.api_call("post", endpoint, new_info)
            if success:
                self.last_commercial = int(time.time())
            return success

class Chat(object):

    def __init__(self, name, oauth, signals):
        self.channel = name
        self.oauth = "oauth:" + oauth
        self.signals = signals
        self.running = False
        self.user_irc_tags = {}
        self.sender_badge_template = ""
        self.chatters = {}
        self.badges = {}
        self.emotes_dict = {}
        self.ffz_url = "https://api.frankerfacez.com/v1"
        self.ffz_cdn = "http://cdn.frankerfacez.com/channel"
        self.ffz_emotes = []
        self.ffz_g_emotes = ["BeanieHipster", "LilZ", "ManChicken", "YellowFever", "YooHoo", "ZreknarF"]
        self.ffz_dict = {}
        self.custom_mod = False
        logging.info("Chat object initialized")

    def emit_status_msg(self, s_msg):
        self.signals.show_new_message.emit('<div style="margin-top: 2px; margin-bottom: 2px; color: #858585;">{}</div>'.format(s_msg))

    def init_icons(self, partner, start_loop_func):
        logging.info("Init icons started")
        self.ffz_user_check()
        self.ffz_global_check()
        self.get_chat_badges()
        if partner and not os.path.exists("images/sub_icon.png"):
            self.get_sub_badge()
            logging.info("Sub badge loaded")
        logging.info("Launching main loop from init_icons")
        start_loop_func()

    def ffz_user_check(self):
        try:
            url = "{}/room/{}".format(self.ffz_url, self.channel)
            data = requests.get(url)
            data.raise_for_status()
            data_decode = data.json()
            set_id = data_decode["room"]["set"]
            for i in data_decode["sets"][str(set_id)]["emoticons"]:
                self.ffz_emotes.append({"name": i["name"], "url": "https:{}".format(i["urls"]["1"])})
        except Exception, e:
            logging.exception(e)
            self.ffz_user_check()

    def ffz_global_check(self):
        try:
            url = "{}/set/global".format(self.ffz_url)
            data = requests.get(url)
            data.raise_for_status()
            data_decode = data.json()
            set_ids = data_decode["default_sets"]
            for i in set_ids:
                for j in data_decode["sets"][str(i)]["emoticons"]:
                    self.ffz_emotes.append({"name": j["name"], "url": "https:{}".format(j["urls"]["1"])})
        except Exception, e:
            logging.exception(e)
            self.ffz_global_check()

    def ffz_ff_check(self):
        try:
            url = "https://cdn.frankerfacez.com/script/event.json"
            data = requests.get(url)
            data.raise_for_status()
            data_decode = data.json()
            # need example response
        except Exception, e:
            logging.exception(e)
            self.ffz_ff_check()

    def save_chat_badges(self, url, key, f_name):
        try:
            image = requests.get(url, stream=True)
            image.raise_for_status()
            with open(f_name, "wb") as i_file:
                shutil.copyfileobj(image.raw, i_file)
            self.badges[key] = f_name
        except Exception, e:
            logging.exception(e)
            self.save_chat_badges(url, key, f_name)

    def get_chat_badges(self):
        logging.debug("Retrieving Chat Badges")
        if not os.path.exists("images/broadcaster_icon.png"):
            bc_url = "http://chat-badges.s3.amazonaws.com/broadcaster.png"
            self.save_chat_badges(bc_url, "broadcaster", "images/broadcaster_icon.png")

        if not os.path.exists("/images/mod_icon.png"):
            if self.custom_mod:
                mod_url = self.ffz_url + "/" + self.channel + "/mod_icon.png"
            else:
                mod_url = "http://chat-badges.s3.amazonaws.com/mod.png"
            self.save_chat_badges(mod_url, "mod", "images/mod_icon.png")

        if not os.path.exists("images/staff.png"):
            staff_url = "http://chat-badges.s3.amazonaws.com/staff.png"
            self.save_chat_badges(staff_url, "staff", "images/staff_icon.png")

        if not os.path.exists("images/global_mod.png"):
            global_url = "http://chat-badges.s3.amazonaws.com/globalmod.png"
            self.save_chat_badges(global_url, "global_mod", "images/global_mod.png")

        if not os.path.exists("images/turbo_icon.png"):
            turbo_url = "http://chat-badges.s3.amazonaws.com/turbo.png"
            self.save_chat_badges(turbo_url, "turbo", "images/turbo_icon.png")
        logging.info("Chat Badges Downloaded")

    def get_sub_badge(self):
        logging.debug("Retrieving Sub Badge")
        url = "https://api.twitch.tv/kraken/chat/{}/badges".format(self.channel)
        badge_links = requests.get(url)
        self.save_chat_badges(badge_links["subscriber"]["image"], "subscriber", "images/sub_icon.png")
        logging.info("Sub Badge Downloaded")

    def connect(self):
        logging.debug("Connecting to Twitch")
        twitch_host = "irc.twitch.tv"
        twitch_port = 6667
        self.irc = socket.socket()
        self.irc.settimeout(600)
        self.irc.connect((twitch_host, twitch_port))
        logging.debug("Connection Complete")

    def irc_disconnect(self):
        try:
            self.irc.sendall("QUIT\r\n")
        except Exception:
            pass
        finally:
            self.irc.close()

    def send_ping(self):
        self.irc.sendall("PING\r\n")
        return

    def send_irc_auth(self):
        logging.debug("Sending Authentication")
        self.irc.sendall("PASS {}\r\n".format(self.oauth))
        self.irc.sendall("NICK {}\r\n".format(self.channel))
        logging.debug("Authentication Sent")

    def join_channel(self):
        logging.debug("Joining Channel and Getting Tags")
        self.irc.sendall("JOIN #{}\r\n".format(self.channel))
        join_info = self.irc.recv(4096)
        join_lines = join_info.split("\r\n")
        for i in join_lines:
            if i.startswith('@'):
                parts = i.split(' ')
                if parts[2] == "USERSTATE":
                    self.user_irc_tags = dict(item.split('=') for item in parts[0][1:].split(';'))
        try:
            self.user_irc_tags["color"]
        except KeyError:
            self.irc.sendall("PART #batedurgonnadie")
            self.join_channel()
        logging.debug("Joined Channel and Requested Tags")

    def establish_connection(self):
        self.connect()
        self.send_irc_auth()
        success = self.irc.recv(4096)
        logging.debug("Retrieving Initial Messages")
        if success == ":tmi.twitch.tv NOTICE * :Login unsuccessful\r\n":
            logging.error("Oauth failed to login user")
            raise Exception
        self.irc.sendall("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n")
        self.irc.recv(1024)
        self.join_channel()
        self.set_sender_badges(2)

    def re_establish_connection(self):
        try:
            self.irc_disconnect()
        except Exception:
            pass
        self.connect()
        self.irc.sendall("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n")
        time.sleep(.1)
        self.irc.recv(1024)
        self.send_irc_auth()
        self.irc.recv(4096)
        self.join_channel()
        return

    def set_sender_badges(self, sleeper):
        try:
            self.user_emotes = requests.get("https://api.twitch.tv/kraken/chat/emoticon_images?on_site=1&emotesets=" + self.user_irc_tags["emote-sets"]).json()
        except Exception:
            sleeper = sleeper ** 2
            time.sleep(sleeper)
            self.set_sender_badges(sleeper)
        self.sender_badge_template = self.twitch_badges({"tags": self.user_irc_tags, "sender": self.channel})

    def send_msg(self, txt):
        try:
            self.irc.sendall("PRIVMSG #{} :{}\r\n".format(self.channel, txt))
        except Exception, e:
            logging.exception(e)
            return False

        msg_time = self.get_timestamp()
        if txt.startswith('/') or txt.startswith('.'):
            final_msg = '<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> {}<span style="color: {};">{}</span>: {}</div>'\
                        .decode("utf-8").format(msg_time, self.sender_badge_template, self.user_irc_tags["color"], self.channel, txt.decode("utf-8"))
            self.signals.show_new_message.emit(final_msg)
            return True

        msg = txt
        for v in self.user_emotes.values():
            for v2 in v.values():
                for i in v2:
                    if re.search(i["code"], msg):
                        emote_url = "http://static-cdn.jtvnw.net/emoticons/v1/{}/1.0".format(i["id"])
                        image_file = self.get_emote_key(str(i["id"]), self.emotes_dict, emote_url)
                        emote_replace = '<img src="{}" />'.format(image_file)
                        msg = re.sub(i["code"], emote_replace, msg)
        msg = self.ffz_parse(msg)
        final_msg = '<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> {}<span style="color: {};">{}</span>: {}</div>'\
                    .decode("utf-8").format(msg_time, self.sender_badge_template, self.user_irc_tags["color"], self.channel, self.escape_html(msg.decode("utf-8")))
        self.signals.show_new_message.emit(final_msg)
        return True

    def get_emote_key(self, key, e_dict, url):
        try:
            image_file = e_dict[key]
        except KeyError:
            print url
            image_file = e_dict[key] = self.download_image(url, key)

        return image_file

    def download_image(self, url, name):
        try:
            image = requests.get(url, stream=True)
            image.raise_for_status()
            with open("images/{0}.png".format(name), "wb") as i_file:
                image.raw.decode_content = True
                shutil.copyfileobj(image.raw, i_file)
            return "images/{}.png".format(name)
        except Exception, e:
            logging.exception(e)
            return name

    def badge_html(self, badge_file):
        return '<img src="{}" height="18" width="18" /> '.format(badge_file)

    def twitch_badges(self, msg_dict):
        badges = ''
        m_tags = msg_dict["tags"]

        if msg_dict["sender"] == self.channel:
            badges += self.badge_html(self.badges["broadcaster"])
        elif m_tags["user-type"]:
            if m_tags["user-type"] == "staff":
                badges += self.badge_html(self.badges["staff"])
            elif m_tags["user-type"] == "admin":
                badges += self.badge_html(self.badges["admin"])
            elif m_tags["user-type"] == "global_mod":
                badges += self.badge_html(self.badges["global_mod"])
            elif m_tags["user-type"] == "mod":
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
            if i["name"] in msg:
                emote_url = i["url"]
                image_file = self.get_emote_key(i["name"], self.ffz_dict, emote_url)
                emote_replace = '<img src="{}" />'.format(image_file)
                msg = msg.replace(i["name"], emote_replace)

        return msg

    def escape_html(self, msg):
        msg = re.sub("(?<!/)>", "&#62;", msg)
        msg = re.sub("<(?!i)", "&#60;", msg)
        return msg

    def parse_msg(self, msg_dict):
        try:
            chatter_obj = self.chatters[msg_dict["sender"].lower()]
            username = chatter_obj.display_name if chatter_obj.display_name is not None else chatter_obj.name
        except KeyError:
            chatter_obj = user.User(username=msg_dict["sender"], chat_color=msg_dict["tags"]["color"], display_name=msg_dict["tags"]["display-name"])
            self.chatters[msg_dict["sender"].lower()] = chatter_obj
            username = chatter_obj.display_name
        text_color = "#000000"
        offset = False
        if msg_dict["message"].startswith("\x01ACTION "):
            offset = True
            msg_dict["message"] = msg_dict["message"][7:-1]
            text_color = chatter_obj.chat_color
        badges = self.twitch_badges(msg_dict)
        if msg_dict["tags"]["color"] and msg_dict["tags"]["color"] != chatter_obj.chat_color:
            chatter_obj.chat_color = msg_dict["tags"]["color"]
        twitch_e_msg = self.twitch_emote_parse(msg_dict["message"], msg_dict["tags"])
        twitch_ffz_msg = self.ffz_parse(twitch_e_msg)
        if not offset:
            twitch_ffz_msg = ": " + twitch_ffz_msg
        msg_time = self.get_timestamp()
        final_msg = '<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> {}<span style="color: {};">{}</span><span style="color: {};">{}</span></div>'\
                    .decode("utf-8").format(msg_time, badges, chatter_obj.chat_color, username, text_color, self.escape_html(twitch_ffz_msg))
        return final_msg

    def get_timestamp(self):
        msg_time = time.strftime("%I:%M")
        if msg_time.startswith('0'):
            msg_time = msg_time[1:]
        return msg_time

    def main_loop(self):
        logging.info("Main Loop Started")
        self.establish_connection()
        self.running = True
        self.emit_status_msg("Connected to chat!")
        message = ""
        while self.running:
            try:
                try:
                    message += self.irc.recv(4096).decode("utf-8")
                except socket.timeout:
                    logging.warning("Socket timed out")
                    if self.running:
                        self.re_establish_connection()
                    continue

                if message == "":
                    logging.warning("Received empty string")
                    if self.running:
                        self.re_establish_connection()
                    continue

                msg_list = message.split("\r\n")
                while len(msg_list) > 1:
                    current_message = msg_list.pop(0)
                    self.signals.update_msg_time.emit(int(time.time()))
                    if current_message.startswith("PING"):
                        self.irc.sendall(current_message.replace("PING", "PONG"))
                        continue
                    try:
                        current_message = current_message.strip()
                        msg_parts = current_message.split(' ')
                        if current_message.startswith(':'):
                            action = msg_parts[1]
                            msg_parts.insert(0, '')
                        elif current_message.startswith('@'):
                            action = msg_parts[2]
                        else:
                            try:
                                print current_message
                                continue
                            except Exception:
                                continue

                    except Exception:
                        print current_message
                        continue
                    if action == "PRIVMSG":
                        c_msg = {}
                        if msg_parts[0]:
                            c_msg["tags"] = dict(item.split('=') for item in msg_parts[0][1:].split(';'))
                        else:
                            c_msg["tags"] = {"color": "", "emotes": {}, "subscriber": 0, "turbo": 0, "user-type": ""}
                        c_msg["sender"] = msg_parts[1][1:].split('!')[0]
                        c_msg["action"] = msg_parts[2]
                        c_msg["channel"] = msg_parts[3]
                        c_msg["message"] = " ".join(msg_parts[4:])[1:]
                        try:
                            print c_msg
                        except Exception, e:
                            print e
                        if c_msg["sender"] == "jtv":
                            jtv_parts = c_msg["message"].split(' ')
                            if jtv_parts[0] == "USERCOLOR":
                                new_color = jtv_parts[2].split("\r\n")[0]
                                self.user_irc_tags["color"] = new_color
                                logging.debug("Chat color set to: {}".format(new_color))
                            else:
                                display_msg = '<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> <span style="color: #858585;">{}</div>'\
                                                .format(self.get_timestamp(), c_msg["message"])
                                self.signals.show_new_message.emit(display_msg)
                        elif c_msg["sender"] == "twitchnotify":
                            try:
                                sub_badge = self.badge_html(self.badges["subscriber"])
                            except KeyError:
                                continue
                            display_msg = '<div style="margin-top: 2px; margin-bottom: 2px;"><span style="font-size: 6pt;">{}</span> {} <span style="color: #858585;">{}</div>'\
                                    .format(self.get_timestamp(), sub_badge, c_msg["message"])
                            self.signals.show_new_message(display_msg)
                        else:
                            self.signals.show_new_message.emit(self.parse_msg(c_msg))
                    else:
                        print current_message
                message = msg_list[0]
            except Exception, e:
                self.re_establish_connection()
                logging.exception(e)
