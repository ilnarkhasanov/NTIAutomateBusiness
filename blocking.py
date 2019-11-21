import sys
from PyQt5 import QtCore, QtWidgets
from skeletons.block import Ui_Form as Skeleton


class BlockWindow(QtWidgets.QWidget, Skeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def timer_Event(self):
        global time
        time = time.addSecs(1)
        print(time)

    app = QtCore.QCoreApplication(sys.argv)

    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)

    timer.timeout.connect(timer_Event)
    timer.start(100)

    exit(app.exec_())
