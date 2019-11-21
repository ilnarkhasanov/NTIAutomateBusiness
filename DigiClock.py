from PyQt5.QtWidgets import QApplication, QLCDNumber
from PyQt5.QtCore import QTimer, QTime
import sys


class Clock(QLCDNumber):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Система заблкирована')
        self.setGeometry(300, 300, 300, 300)
        self.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)

        timer.start(1000)

        self.now_its_minutes = QTime.currentTime().minute()
        self.now_its_seconds = QTime.currentTime().second()
        print(self.now_its_minutes, self.now_its_seconds)

        self.showTime()

    def showTime(self):
        time = QTime()
        time.currentTime()
        # time.setHMS(0, 4 - (QTime.currentTime().minute() - self.now_its_minutes),
        #             60 - (QTime.currentTime().second() - self.now_its_seconds))
        # if QTime.currentTime().minute() - self.now_its_minutes == 1 and QTime.currentTime().second() - self.now_its_seconds == 0:
        #     self.destroy()
        text = time.toString('mm:ss')
        print(QTime.currentTime().hour(),
              QTime.currentTime().minute(),
              QTime.currentTime().second())
        if time.second() % 2 == 0:
            text = text[:2] + ' ' + text[3:]
        self.display(text)


app = QApplication(sys.argv)
clock = Clock()
clock.show()
app.exec()
