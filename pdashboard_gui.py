# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pdashboard_gui.ui'
#
# Created: Fri Nov 07 02:35:46 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_pdt(object):
    def setupUi(self, pdt):
        pdt.setObjectName("pdt")
        pdt.resize(727, 395)
        font = QtGui.QFont()
        font.setPointSize(8)
        pdt.setFont(font)
        pdt.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        pdt.setDocumentMode(False)
        pdt.setTabShape(QtGui.QTabWidget.Rounded)
        pdt.setDockNestingEnabled(False)
        self.centralwidget = QtGui.QWidget(pdt)
        self.centralwidget.setObjectName("centralwidget")
        self.update_game_title = QtGui.QPushButton(self.centralwidget)
        self.update_game_title.setGeometry(QtCore.QRect(330, 150, 111, 161))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.update_game_title.setFont(font)
        self.update_game_title.setObjectName("update_game_title")
        self.oauth_get = QtGui.QPushButton(self.centralwidget)
        self.oauth_get.setGeometry(QtCore.QRect(330, 50, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.oauth_get.setFont(font)
        self.oauth_get.setObjectName("oauth_get")
        self.title_label = QtGui.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(10, 190, 46, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setScaledContents(True)
        self.title_label.setObjectName("title_label")
        self.nick_label = QtGui.QLabel(self.centralwidget)
        self.nick_label.setGeometry(QtCore.QRect(10, 50, 46, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.nick_label.setFont(font)
        self.nick_label.setFrameShadow(QtGui.QFrame.Plain)
        self.nick_label.setScaledContents(True)
        self.nick_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.nick_label.setObjectName("nick_label")
        self.viewer_text = QtGui.QLabel(self.centralwidget)
        self.viewer_text.setEnabled(True)
        self.viewer_text.setGeometry(QtCore.QRect(70, 330, 211, 31))
        self.viewer_text.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setWeight(75)
        font.setBold(True)
        self.viewer_text.setFont(font)
        self.viewer_text.setFrameShadow(QtGui.QFrame.Plain)
        self.viewer_text.setScaledContents(True)
        self.viewer_text.setAlignment(QtCore.Qt.AlignCenter)
        self.viewer_text.setMargin(0)
        self.viewer_text.setIndent(-1)
        self.viewer_text.setObjectName("viewer_text")
        self.viewer_number = QtGui.QLCDNumber(self.centralwidget)
        self.viewer_number.setGeometry(QtCore.QRect(280, 320, 81, 51))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.viewer_number.setFont(font)
        self.viewer_number.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.viewer_number.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.viewer_number.setAutoFillBackground(False)
        self.viewer_number.setInputMethodHints(QtCore.Qt.ImhDialableCharactersOnly|QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhLowercaseOnly|QtCore.Qt.ImhUppercaseOnly)
        self.viewer_number.setFrameShape(QtGui.QFrame.NoFrame)
        self.viewer_number.setFrameShadow(QtGui.QFrame.Plain)
        self.viewer_number.setMidLineWidth(0)
        self.viewer_number.setMode(QtGui.QLCDNumber.Dec)
        self.viewer_number.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.viewer_number.setObjectName("viewer_number")
        self.chat_container = QtGui.QGroupBox(self.centralwidget)
        self.chat_container.setGeometry(QtCore.QRect(450, 0, 271, 371))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.chat_container.setFont(font)
        self.chat_container.setAcceptDrops(True)
        self.chat_container.setFlat(False)
        self.chat_container.setObjectName("chat_container")
        self.send_message = QtGui.QPushButton(self.chat_container)
        self.send_message.setGeometry(QtCore.QRect(220, 330, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.send_message.setFont(font)
        self.send_message.setObjectName("send_message")
        self.chat_send = QtGui.QLineEdit(self.chat_container)
        self.chat_send.setGeometry(QtCore.QRect(10, 330, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chat_send.setFont(font)
        self.chat_send.setDragEnabled(True)
        self.chat_send.setObjectName("chat_send")
        self.chat_box = QtGui.QTextEdit(self.chat_container)
        self.chat_box.setGeometry(QtCore.QRect(10, 23, 251, 301))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chat_box.sizePolicy().hasHeightForWidth())
        self.chat_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.chat_box.setFont(font)
        self.chat_box.setAcceptDrops(False)
        self.chat_box.setFrameShape(QtGui.QFrame.StyledPanel)
        self.chat_box.setFrameShadow(QtGui.QFrame.Sunken)
        self.chat_box.setLineWidth(1)
        self.chat_box.setMidLineWidth(0)
        self.chat_box.setReadOnly(True)
        self.chat_box.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.chat_box.setObjectName("chat_box")
        self.game_label = QtGui.QLabel(self.centralwidget)
        self.game_label.setGeometry(QtCore.QRect(10, 150, 46, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.game_label.setFont(font)
        self.game_label.setScaledContents(True)
        self.game_label.setObjectName("game_label")
        self.refresh = QtGui.QToolButton(self.centralwidget)
        self.refresh.setGeometry(QtCore.QRect(10, 230, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.refresh.setFont(font)
        self.refresh.setObjectName("refresh")
        self.nick = QtGui.QLineEdit(self.centralwidget)
        self.nick.setGeometry(QtCore.QRect(70, 50, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nick.setFont(font)
        self.nick.setMouseTracking(False)
        self.nick.setAcceptDrops(False)
        self.nick.setReadOnly(True)
        self.nick.setObjectName("nick")
        self.game = QtGui.QLineEdit(self.centralwidget)
        self.game.setGeometry(QtCore.QRect(70, 150, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.game.setFont(font)
        self.game.setObjectName("game")
        self.auth_code = QtGui.QLabel(self.centralwidget)
        self.auth_code.setGeometry(QtCore.QRect(10, 10, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.auth_code.setFont(font)
        self.auth_code.setFrameShadow(QtGui.QFrame.Plain)
        self.auth_code.setScaledContents(True)
        self.auth_code.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.auth_code.setObjectName("auth_code")
        self.authorize_button = QtGui.QPushButton(self.centralwidget)
        self.authorize_button.setGeometry(QtCore.QRect(330, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.authorize_button.setFont(font)
        self.authorize_button.setObjectName("authorize_button")
        self.auth_input = QtGui.QLineEdit(self.centralwidget)
        self.auth_input.setGeometry(QtCore.QRect(70, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.auth_input.setFont(font)
        self.auth_input.setMouseTracking(False)
        self.auth_input.setAcceptDrops(False)
        self.auth_input.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.auth_input.setReadOnly(False)
        self.auth_input.setObjectName("auth_input")
        self.chat_connect = QtGui.QPushButton(self.centralwidget)
        self.chat_connect.setGeometry(QtCore.QRect(330, 90, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.chat_connect.setFont(font)
        self.chat_connect.setObjectName("chat_connect")
        self.ads_label = QtGui.QLabel(self.centralwidget)
        self.ads_label.setGeometry(QtCore.QRect(10, 100, 46, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.ads_label.setFont(font)
        self.ads_label.setFrameShadow(QtGui.QFrame.Plain)
        self.ads_label.setScaledContents(True)
        self.ads_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ads_label.setObjectName("ads_label")
        self.ad_30 = QtGui.QPushButton(self.centralwidget)
        self.ad_30.setGeometry(QtCore.QRect(70, 100, 31, 31))
        self.ad_30.setObjectName("ad_30")
        self.ad_60 = QtGui.QPushButton(self.centralwidget)
        self.ad_60.setGeometry(QtCore.QRect(110, 100, 31, 31))
        self.ad_60.setObjectName("ad_60")
        self.ad_150 = QtGui.QPushButton(self.centralwidget)
        self.ad_150.setGeometry(QtCore.QRect(230, 100, 31, 31))
        self.ad_150.setObjectName("ad_150")
        self.ad_120 = QtGui.QPushButton(self.centralwidget)
        self.ad_120.setGeometry(QtCore.QRect(190, 100, 31, 31))
        self.ad_120.setObjectName("ad_120")
        self.ad_90 = QtGui.QPushButton(self.centralwidget)
        self.ad_90.setGeometry(QtCore.QRect(150, 100, 31, 31))
        self.ad_90.setObjectName("ad_90")
        self.ad_180 = QtGui.QPushButton(self.centralwidget)
        self.ad_180.setGeometry(QtCore.QRect(270, 100, 31, 31))
        self.ad_180.setObjectName("ad_180")
        self.title = QtGui.QTextEdit(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(70, 200, 251, 111))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.title.setFont(font)
        self.title.setAcceptRichText(False)
        self.title.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.title.setObjectName("title")
        pdt.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(pdt)
        self.statusBar.setObjectName("statusBar")
        pdt.setStatusBar(self.statusBar)

        self.retranslateUi(pdt)
        QtCore.QMetaObject.connectSlotsByName(pdt)
        pdt.setTabOrder(self.oauth_get, self.update_game_title)

    def retranslateUi(self, pdt):
        pdt.setWindowTitle(QtGui.QApplication.translate("pdt", "Python Dashboard", None, QtGui.QApplication.UnicodeUTF8))
        self.update_game_title.setText(QtGui.QApplication.translate("pdt", "Update Game\n"
"and Title", None, QtGui.QApplication.UnicodeUTF8))
        self.oauth_get.setText(QtGui.QApplication.translate("pdt", "Authorize", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("pdt", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.nick_label.setText(QtGui.QApplication.translate("pdt", "Nick:", None, QtGui.QApplication.UnicodeUTF8))
        self.viewer_text.setText(QtGui.QApplication.translate("pdt", "Current Viewers:", None, QtGui.QApplication.UnicodeUTF8))
        self.chat_container.setTitle(QtGui.QApplication.translate("pdt", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.send_message.setText(QtGui.QApplication.translate("pdt", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.game_label.setText(QtGui.QApplication.translate("pdt", "Game:", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh.setText(QtGui.QApplication.translate("pdt", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.auth_code.setText(QtGui.QApplication.translate("pdt", "Auth:", None, QtGui.QApplication.UnicodeUTF8))
        self.authorize_button.setText(QtGui.QApplication.translate("pdt", "Get Auth Code", None, QtGui.QApplication.UnicodeUTF8))
        self.chat_connect.setText(QtGui.QApplication.translate("pdt", "Connect to Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.ads_label.setText(QtGui.QApplication.translate("pdt", "Ads:", None, QtGui.QApplication.UnicodeUTF8))
        self.ad_30.setText(QtGui.QApplication.translate("pdt", "30", None, QtGui.QApplication.UnicodeUTF8))
        self.ad_60.setText(QtGui.QApplication.translate("pdt", "60", None, QtGui.QApplication.UnicodeUTF8))
        self.ad_150.setText(QtGui.QApplication.translate("pdt", "150", None, QtGui.QApplication.UnicodeUTF8))
        self.ad_120.setText(QtGui.QApplication.translate("pdt", "120", None, QtGui.QApplication.UnicodeUTF8))
        self.ad_90.setText(QtGui.QApplication.translate("pdt", "90", None, QtGui.QApplication.UnicodeUTF8))
        self.ad_180.setText(QtGui.QApplication.translate("pdt", "180", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setHtml(QtGui.QApplication.translate("pdt", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

