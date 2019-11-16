from PyQt5 import QtWidgets
from sys import argv, exit
from skeletons.auth import Ui_Form


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(argv)
    application = MainWindow()
    application.show()
    exit(app.exec_())


if __name__ == "__main__":
    main()
