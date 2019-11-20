from PyQt5 import QtWidgets
from sys import argv, exit
from skeletons.auth import Ui_Form
from skeletons.mainwind_users import Ui_MainWindow as Mw_user
import sqlite3

times_trying_to_auth = 0


class MainWindowUser(QtWidgets.QMainWindow, Mw_user):
    def __init__(self, login, posit):
        super().__init__()
        self.setupUi(self)

        self.login = login
        self.posit = posit

        self.your_login.setText("Ваш логин: " + login)
        self.your_password.setText("Ваша должность: " + posit)
        # описание деятельности


class AuthorizationWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(AuthorizationWindow, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # self.ui.Authorization.clicked.connect(self.auth)
        self.ui.Authorization.clicked.connect(self.auth)

    def auth(self):
        login = self.ui.login.text()
        password = self.ui.password.text()

        # print(login)

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute(f'''SELECT * FROM data WHERE login="{login}" AND password="{password}"''')

        posit = c.fetchall()[0][1]

        # add authing by password
        self.wind = MainWindowUser(login, posit)
        self.wind.show()


def main():
    app = QtWidgets.QApplication(argv)
    application = AuthorizationWindow()
    application.show()

    exit(app.exec_())


if __name__ == "__main__":
    main()
