from PyQt5 import QtWidgets, QtCore
from sys import argv, exit
from skeletons.auth import Ui_Form
from skeletons.mainwind_users import Ui_MainWindow as Mw_user
from skeletons.incorrect_password import Ui_Form as Err_Auth_Window
from skeletons.block import Ui_Form as Block_Skeleton
from skeletons.mainwind_admin import Ui_MainWindow as Mw_Admin
from skeletons.admin_skel.add_user import Ui_Form as AddingUserSkeleton
from skeletons.admin_skel.remove_user import Ui_Form as RemovingUserSkeleton
import sqlite3

times_trying_to_auth = 0


# class BlockWindow(QtWidgets.QWidget, Block_Skeleton):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#     def timer_Event(self):
#         global time
#         time = time.addSecs(1)
#         print(time)
#
#     app = QtCore.QCoreApplication(argv)
#
#     timer = QtCore.QTimer()
#     time = QtCore.QTime(0, 0, 0)
#
#     timer.timeout.connect(timer_Event)
#     timer.start(100)
#
#     exit(app.exec_())


class AddingUserByAdmin(QtWidgets.QWidget, AddingUserSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.registerNewUser.clicked.connect(self.registring)

    def registring(self):
        login = self.loginOfNewUser.text()
        posit = self.positionOfNewUser.currentText()

        if (login == ""):
            QtWidgets.QMessageBox.about(self, "Внимание", "Логин пуст! Введите логин.")
        else:
            conn = sqlite3.connect('databases/data.db')
            c = conn.cursor()
            c.execute(f'INSERT INTO data (login, posit, password) VALUES ("{login}", "{posit}", "123");')
            conn.commit()
            conn.close()
            self.destroy()


class RemovingUserByAdmin(QtWidgets.QWidget, RemovingUserSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainWindowAdmin(QtWidgets.QMainWindow, Mw_Admin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.addUserButton.clicked.connect(self.adding_user)
        self.removeUserButton.clicked.connect(self.removing_user)

    def adding_user(self):
        self.add_new_user = AddingUserByAdmin()
        self.add_new_user.show()

    def removing_user(self):
        self.remove_user = RemovingUserByAdmin()
        self.remove_user.show()


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

        self.qww = MainWindowAdmin()
        self.qww.show()

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

                # self.open_error()
            else:
                self.error = ErrorWindow(3 - times_trying_to_auth)
                self.error.show()

        else:
            posit = account_data[0][1]

            conn.close()

            self.wind = MainWindowUser(login, posit)
            self.wind.show()

        # add authing by password

    # def open_error(self):
    #     self.block = BlockWindow()
    #     self.block.show()


def main():
    app = QtWidgets.QApplication(argv)
    application = AuthorizationWindow()
    application.show()

    exit(app.exec_())


if __name__ == "__main__":
    main()
