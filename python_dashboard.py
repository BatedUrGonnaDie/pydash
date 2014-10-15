from PySide.QtCore import *
from PySide.QtGui import *
from pdashboard_gui import Ui_pdt
import sys
import twitch
import configuration as config


class Dashboard(QMainWindow, Ui_pdt):

    def __init__(self, parent = None):
        super(Dashboard, self).__init__(parent)
        self.setupUi(self)
        user_config = config.open_file()

        self.connect(self.send_message, SIGNAL("clicked()"), self.twitch_send_message)

        self.worker_thread = WorkerThread()

        self.connect(self.worker_thread, SIGNAL("update_nick()"), self.thread_done, Qt.DirectConnection)

    def thread_done(self):
        self.nick.setText("BatedUrGonnaDie")

    def twitch_send_message(self):
        self.worker_thread.start()
        pass

class WorkerThread(QThread):

    def __init__(self, parent = None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        self.emit(SIGNAL("update_nick()"))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
