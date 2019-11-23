import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from skeletons.system_blocked import Ui_Form as BlockingUser


class MainWindow(QtWidgets.QWidget, BlockingUser):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)

        finish = QtWidgets.QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

        # menubar = self.menuBar()
        # fmenu = menubar.addMenu("File")
        # fmenu.addAction(finish)

    def closeEvent(self, event):
        event.ignore()
        # close = QMessageBox.question(self,
        #                              "QUIT",
        #                              "Sure?",
        #                              QMessageBox.Yes | QMessageBox.No)
        # if close == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()

    def timer_event(self):
        self.time = self.time.addSecs(1)
        minutes = str(4 - int(self.time.toString("m")))
        seconds = str(59 - int(self.time.toString("s")))
        self.minutes_render.display(minutes)
        self.seconds_render.display(seconds)
        print(self.time.toString("mm:ss"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()

    print('here')

    exit(app.exec_())


if __name__ == "__main__":
    main()
