from PyQt5 import QtWidgets
from sys import argv, exit
from skeletons.auth import Ui_Form
from skeletons.mainwind_users import Ui_MainWindow as Mw_user
from skeletons.incorrect_password import Ui_Form as Err_Auth_Window
import sqlite3

times_trying_to_auth = 0


class ErrorWindow(QtWidgets.QWidget, Err_Auth_Window):
    def __init__(self, times):
        super().__init__()
        self.setupUi(self)

        self.Hey.setText('Пароль введен неправильно! Количество оставшихся попыток: ' + str(times))

        self.OK.clicked.connect(self.leave)

    def leave(self):
        self.close()


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

        self.ui.Authorization.clicked.connect(self.auth)

    def auth(self):
        global times_trying_to_auth

        login = self.ui.login.text()
        password = self.ui.password.text()

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute(f'''SELECT * FROM data WHERE login="{login}" AND password="{password}"''')

        account_data = c.fetchall()

        if not len(account_data):
            times_trying_to_auth += 1

            if times_trying_to_auth == 3:
                times_trying_to_auth = 0

            self.error = ErrorWindow(3 - times_trying_to_auth)
            self.error.show()

        else:
            posit = account_data[0][1]

            conn.close()

            self.wind = MainWindowUser(login, posit)
            self.wind.show()

        # add authing by password


def main():
    app = QtWidgets.QApplication(argv)
    application = AuthorizationWindow()
    application.show()

    exit(app.exec_())


if __name__ == "__main__":
    main()
