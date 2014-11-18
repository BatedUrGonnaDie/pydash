#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from PySide.QtCore      import *
from PySide.QtGui       import *
from pdashboard_gui     import Ui_pdt

import sys
import threading
import time

import twitch
import configuration    as config

class Dashboard(QMainWindow, Ui_pdt):

    auth_set            = Signal(str)
    nick_set            = Signal(str)
    title_set           = Signal(str)
    game_set            = Signal(str)
    status_set          = Signal(str)
    update_status       = Signal()
    show_new_message    = Signal(str, str, str)

    def __init__(self, parent = None):
        super(Dashboard, self).__init__(parent)
        self.setupUi(self)

        self.authorized = False
        self.chat_connected = False
        self.partner = False
        self.live = False

        self.configure = config.Configurer()

        #set up label for status bar
        self.status_bools = QLabel(self.centralwidget)
        self.status_bools.setObjectName("status_bool_text")
        self.status_bools.setFrameShadow(QFrame.Plain)
        self.statusBar.addPermanentWidget(self.status_bools)

        #set up auto-complete for game
        self.games_list = self.configure.get_completer_list()
        self.game_completer = QCompleter(self.games_list, self.game)
        self.game_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.game.setCompleter(self.game_completer)

        self.authorize_button.clicked.connect(self.configure.get_auth_code)
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

        self.send_message.clicked.connect(self.message_send)

        self.auth_set.connect(self.set_auth_text)
        self.nick_set.connect(self.set_nick_text)
        self.title_set.connect(self.set_title_text)
        self.game_set.connect(self.set_game_text)
        self.status_set.connect(self.status_temp_text)
        self.update_status.connect(self.set_perm_status_text)
        self.show_new_message.connect(self.set_new_message)

        self.user_config = self.configure.load_file()
        

        auto_minute = threading.Thread(target = self.minute_loop)
        auto_minute.daemon = True
        auto_minute.start()

        self.update_status.emit()

        if self.user_config["oauth"] != "":
            self.auth_set.emit(self.user_config["oauth"])
            checker = threading.Thread(target = self.check_code)
            checker.daemon = True
            checker.start()

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
                else:
                    self.status_set.emit("Authenticated")
            else:
                self.status_set.emit("Bad OAuth, Please Retrieve Another")
        self.update_status.emit()

    def connect_to_chat(self):
        if self.authorized:
            if self.chat_connected:
                del self.chat_worker
                self.chat_connected = False
                self.chat_connect.setText("Connect to Chat")
            else:
                nick = self.nick.text()
                oauth = self.api_worker.oauth_token
                self.chat_worker = twitch.Chat(nick, oauth)
                self.chat_connected = True
                self.chat_connect.setText("Disconnect")

                #chat stuff

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

    def set_new_message(self, sender, color, msg):
        pass
        
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
            title = self.title.toPlainText().strip()
            game = self.game.text().strip()
            success = self.api_worker.set_gt(title, game)
            if success["game"] == game and success["status"] == title:
                self.status_set.emit("Updated Game and Title")
            else:
                self.status_set.emit("Failed to Updated")
    
    def refresh_gt(self):
        if self.authorized:
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
                        viewers = info["stream"]["viewers"]
                        self.viewer_number.display(viewers)
                        if viewers > self.user_config["max_viewers"]:
                            self.user_config = self.configure.set_param("max_viewers", viewers)
                    else:
                        self.viewer_number.display(0)
            time.sleep(60)
            self.update_status.emit()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    window.setFixedSize(window.size())
    sys.exit(app.exec_())
