#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from PySide.QtCore      import *
from PySide.QtGui       import *
from PySide             import QtSvg, QtXml
from pdashboard_gui     import Ui_pdt

import sys
import os
import threading
import time
import Queue

import twitch
import configuration    as config

q = Queue.Queue()

image_folder = "images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

class Dashboard(QMainWindow, Ui_pdt):

    auth_set            = Signal(str)
    nick_set            = Signal(str)
    title_set           = Signal(str)
    game_set            = Signal(str)
    status_set          = Signal(str)
    update_status       = Signal()
    show_new_message    = Signal(str)

    def __init__(self, parent = None):
        super(Dashboard, self).__init__(parent)
        self.setupUi(self)

        self.authorized = False
        self.chat_connected = False
        self.partner = False
        self.live = False
        self.peak_viewer = 0

        self.configure = config.Configurer()

        #set up label for status bar
        self.status_bools = QLabel(self.centralwidget)
        self.status_bools.setObjectName("status_bool_text")
        self.status_bools.setFrameShadow(QFrame.Plain)
        self.statusBar.addPermanentWidget(self.status_bools)

        self.authorize_button.clicked.connect(self.configure.get_auth_code)
        self.auth_input.returnPressed.connect(self.check_code)
        self.oauth_get.clicked.connect(self.check_code)
        self.chat_connect.clicked.connect(self.connect_to_chat)

        self.ad_30.clicked.connect(self.ad_click)
        self.ad_60.clicked.connect(self.ad_click)
        self.ad_90.clicked.connect(self.ad_click)
        self.ad_120.clicked.connect(self.ad_click)
        self.ad_150.clicked.connect(self.ad_click)
        self.ad_180.clicked.connect(self.ad_click)

        self.refresh.clicked.connect(self.refresh_gt)
        self.update_game_title.clicked.connect(self.set_game_title)

        self.chat_send.returnPressed.connect(self.message_send)
        self.send_message.clicked.connect(self.message_send)

        self.auth_set.connect(self.set_auth_text)
        self.nick_set.connect(self.set_nick_text)
        self.title_set.connect(self.set_title_text)
        self.game_set.connect(self.set_game_text)
        self.status_set.connect(self.status_temp_text)
        self.update_status.connect(self.set_perm_status_text)
        self.show_new_message.connect(self.set_new_message)

        self.user_config = self.configure.load_file()
        
        self.setGeometry(self.user_config["position"][0], self.user_config["position"][1], 850, 385)
        self.update_status.emit()

        if self.user_config["oauth"] != "":
            self.auth_set.emit(self.user_config["oauth"])
            checker = threading.Thread(target = self.check_code)
            checker.daemon = True
            checker.start()

        auto_minute = threading.Thread(target = self.minute_loop)
        auto_minute.daemon = True
        auto_minute.start()

    def check_code(self):
        if not self.authorized:
            oauth = self.auth_input.text()
            self.api_worker = twitch.API(oauth)
            self.api_worker.set_headers(oauth)
            info = self.api_worker.check_auth_status()
            if info:
                self.authorized = True
                self.user_config = self.configure.set_param("channel", info["token"]["user_name"])
                self.user_config = self.configure.set_param("oauth", oauth)
                self.nick_set.emit(info["token"]["user_name"])
                self.api_worker.channel = self.user_config["channel"]
                self.auth_input.setReadOnly(True)
                self.refresh_gt()
                self.partner = self.api_worker.check_partner_status()
                if self.partner:
                    self.status_set.emit("Authenticated | Partner: Commercial Buttons Enabled")
                    self.ad_30.setEnabled(True)
                    self.ad_60.setEnabled(True)
                    self.ad_90.setEnabled(True)
                    self.ad_120.setEnabled(True)
                    self.ad_150.setEnabled(True)
                    self.ad_180.setEnabled(True)
                else:
                    self.status_set.emit("Authenticated")
            else:
                self.status_set.emit("Bad OAuth, Please Retrieve Another")
                self.auth_input.setText("")
        self.update_status.emit()

    def set_completer(self):
        #set up auto-complete for game if it is present
        self.games_list = self.configure.get_completer_list()
        if self.games_list:
            self.game_completer = QCompleter(self.games_list, self.game)
            self.game_completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.game.setCompleter(self.game_completer)

    def connect_to_chat(self):
        if self.authorized:
            if self.chat_connected:
                self.chat_worker.running = False
                self.chat_worker.irc_disconnect()
                del self.chat_worker
                del self.chat_sender
                self.msg_bool_loop = False
                del self.msg_queue
                self.chat_connected = False
                self.chat_connect.setText("Connect to Chat")
                self.send_message.setEnabled(False)
                self.update_status.emit()
            else:
                nick = self.nick.text()
                oauth = self.api_worker.oauth_token
                self.chat_worker = twitch.Chat(nick, oauth, q)
                self.chat_worker.init_icons(self.partner)
                self.chat_sender = twitch.Chat(nick, oauth, q)
                self.chatter = threading.Thread(target = self.chat_worker.main_loop)
                self.chatter.daemon = True
                self.chatter.start()
                self.chat_connected = True
                self.chat_connect.setText("Disconnect")
                self.update_status.emit()
                self.msg_bool_loop = True
                self.msg_queue = threading.Thread(target = self.get_new_msg)
                self.msg_queue.daemon = True
                self.msg_queue.start()
                self.send_message.setEnabled(True)

    def get_new_msg(self):
        while self.msg_bool_loop:
            data = q.get()
            self.show_new_message.emit(data)

    def set_auth_text(self, text):
        self.auth_input.setText(text)

    def set_nick_text(self, text):
        self.nick.setText(text)

    def set_title_text(self, text):
        self.title.setPlainText(text)

    def set_game_text(self, text):
        self.game.setText(text)

    def status_temp_text(self, text):
        self.statusBar.showMessage(text)

    def set_perm_status_text(self):
        self.status_bools.setText("Connected to Chat: " + str(self.chat_connected) + " | Live: " + str(self.live))

    def set_new_message(self, msg):
        #print msg
        self.chat_box.append(msg)

    def ad_click(self):
        if self.authorized and self.partner:
            length = int(self.sender().text())
            success = self.api_worker.run_commercial(length)
            if success:
                self.ad_cooldown(length)
            else:
                self.status_set.emit("Commercial Failed to Run")

    def set_game_title(self):
        if self.authorized:
            self.status_set.emit("Updating Game and Title...")
            title = self.title.toPlainText().strip()
            game = self.game.text().strip()
            success = self.api_worker.set_gt(title, game)
            if success["game"] == game and success["status"] == title:
                self.status_set.emit("Updated Game and Title")
            else:
                self.status_set.emit("Failed to Updated")
    
    def refresh_gt(self):
        if self.authorized:
            self.status_set.emit("Refreshing Game and Title...")
            title, game = self.api_worker.get_gt()
            if title and game:
                self.title_set.emit(title)
                self.game_set.emit(game)
                self.status_set.emit("Game and Title Refreshed")
            else:
                self.status_set.emit("Failed to Refresh")

    def message_send(self):
        if self.chat_connected:
            msg = self.chat_send.text()
            self.chat_send.setText("")
            if msg:
                tmp_thread = threading.Thread(target = self.thread_send_message, args = [msg])
                tmp_thread.start()
        else:
            self.chat_send.setText("")

    def thread_send_message(self, msg):
        self.chat_sender.establish_connection()
        if self.chat_sender.send_msg(msg):
            self.chat_sender.irc_disconnect()
            return
        else:
            raise Exception

    def ad_cooldown(self, length):
        current_status = self.statusBar.currentMessage()
        while length > 0:
            if current_status:
                self.update_status.emit(current_status + " | Last Ad: " + length)
            else:
                self.update_status.emit("Last Ad: " + length)
            --length
            time.sleep(1)

    def minute_loop(self):
        while True:
            if self.authorized:
                info = self.api_worker.get_stream_object()
                if info:
                    if info["stream"] != None:
                        self.live = True
                        viewers = info["stream"]["viewers"]
                        self.viewer_number.setText(str(viewers))
                        if viewers > self.peak_viewer:
                            self.peak_viewer_number.setText(str(viewers))
                            self.peak_viewer = viewers
                        if viewers > self.user_config["max_viewers"]:
                            self.user_config = self.configure.set_param("max_viewers", viewers)
                    else:
                        self.live = False
                        self.viewer_number.setText(str(0))

            self.update_status.emit()
            time.sleep(60)

    def closeEvent(self, event):
        for files in os.listdir(image_folder):
            file_path = os.path.join(image_folder, files)
            try:
                os.unlink(file_path)
            except Exception, e:
                print e

        if self.chat_connected:
            self.chat_worker.irc_disconnect()

        position = [self.pos().x(), self.pos().y()]
        self.user_config = self.configure.set_param("position", (position))
        QMainWindow.closeEvent(self, event)
            

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    window.setFixedSize(window.size())
    window.set_completer()
    sys.exit(app.exec_())
