from PyQt5 import QtWidgets, QtCore, QtGui
from sys import argv, exit
from skeletons.auth import Ui_Form
from skeletons.mainwind_users import Ui_MainWindow as Mw_user
from skeletons.incorrect_password import Ui_Form as Err_Auth_Window
from skeletons.mainwind_admin import Ui_MainWindow as Mw_Admin
from skeletons.admin_skel.add_user import Ui_Form as AddingUserSkeleton
from skeletons.admin_skel.remove_user import Ui_Form as RemovingUserSkeleton
from skeletons.admin_skel.add_role import Ui_Form as AddingRoleSkeleton
from skeletons.system_blocked import Ui_Form as BlockingUser
from skeletons.admin_skel.loghistory import Ui_Form as LogHistorySkeleton
import socket
import datetime
import sqlite3

times_trying_to_auth = 0


class LogHistoryWindow(QtWidgets.QWidget, LogHistorySkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        log = open('sysfiles/log.txt', 'r')

        data = ''
        for line in log.readlines():
            data += line
        self.logBrowser.setText(data)
        log.close()


class BlockWind(QtWidgets.QWidget, BlockingUser):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.minutes_render.display("4")
        self.seconds_render.display("59")

        self.timer = QtCore.QTimer()
        self.time = QtCore.QTime(0, 0, 0)

        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)

        finish = QtWidgets.QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)


    def closeEvent(self, event):
        event.ignore()

    def timer_event(self):
        self.time = self.time.addSecs(1)

        if int(self.time.toString("m")) == 4 and int(self.time.toString("s")) == 59:
            self.timer.stop()

            self.reauthing = AuthorizationWindow()
            self.reauthing.show()

            self.close()
            self.destroy()

        minutes = str(4 - int(self.time.toString("m")))
        seconds = str(59 - int(self.time.toString("s")))
        self.minutes_render.display(minutes)
        self.seconds_render.display(seconds)
        print(self.time.toString("mm:ss"))


class AddingRoleByAdmin(QtWidgets.QWidget, AddingRoleSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.addRoleButton.clicked.connect(self.addingRole)

    def addingRole(self):
        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()
        c.execute(f'SELECT posit FROM roles WHERE posit="{self.roleName.toPlainText()}"')

        if len(c.fetchall()):
            QtWidgets.QMessageBox.about(self, 'Внимание!', 'Такая роль уже существует!')
        else:
            c.execute(f'INSERT INTO roles (posit) VALUES ("{self.roleName.toPlainText()}")')
            QtWidgets.QMessageBox.about(self, 'Внимание!', f'Роль "{self.roleName.toPlainText()}" успешно создана')

        conn.close()


class AddingUserByAdmin(QtWidgets.QWidget, AddingUserSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM roles;')
        arr = []
        for i in c.fetchall():
            arr.append(i[0])
        conn.close()

        for i in range(len(arr)):
            self.positionOfNewUser.addItem(arr[i])

        self.registerNewUser.clicked.connect(self.registring)

    def registring(self):
        login = self.loginOfNewUser.text()

        posit = self.positionOfNewUser.currentText()

        if login == "":
            QtWidgets.QMessageBox.about(self, "Внимание", "Логин пуст! Введите логин.")
        else:
            conn = sqlite3.connect('databases/data.db')
            c = conn.cursor()

            c.execute(f'SELECT * FROM data WHERE login="{login}";')

            if len(c.fetchall()):
                QtWidgets.QMessageBox.about(self, 'Внимание!',
                                            f'Пользователь с логином {login} уже существует в системе!')
            else:
                c.execute(f'INSERT INTO data (login, posit, password) VALUES ("{login}", "{posit}", "123");')
                conn.commit()
                conn.close()

                QtWidgets.QMessageBox.about(self, 'Внимание!', f'Пользователь с логином "{login}" успешно добавлен!')

            self.close()


class RemovingUserByAdmin(QtWidgets.QWidget, RemovingUserSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.deleteUser.setText('Удалить')

        self.deleteUser.clicked.connect(self.removingUserFunc)

    def removingUserFunc(self):
        if self.userLogin.text() == "":
            QtWidgets.QMessageBox.about(self, 'Внимание!', 'Логин пуст! Введите логин')
        else:
            login = self.userLogin.text()

            conn = sqlite3.connect('databases/data.db')
            c = conn.cursor()
            c.execute(f'SELECT * FROM data WHERE login="{login}";')

            account_data = c.fetchall()

            if not len(account_data):
                QtWidgets.QMessageBox.about(self, 'Внимание!', 'Такого логина не существует!')

            else:
                c.execute(f'DELETE FROM data WHERE login="{login}";')
                conn.commit()
                QtWidgets.QMessageBox.about(self, 'Внимание!', f'Аккаунт с логином {login} успешно удалён')
                self.close()
            conn.close()


class MainWindowAdmin(QtWidgets.QMainWindow, Mw_Admin):
    def __init__(self, login):
        super().__init__()
        self.setupUi(self)

        self.login = login

        self.setWindowTitle('Профиль - ' + login)

        self.your_login.setText("Ваш логин: " + login)
        self.your_password.setText("Ваша должность: Администратор/разработчик системы")

        self.addUserButton.clicked.connect(self.adding_user)
        self.removeUserButton.clicked.connect(self.removing_user)
        self.addRoleButton.clicked.connect(self.adding_role)
        self.logButton.clicked.connect(self.checking_log)

        self.action.triggered.connect(self.leaving)

    def checking_log(self):
        self.log_window_func = LogHistoryWindow()
        self.log_window_func.show()

    def adding_role(self):
        self.open_add_role = AddingRoleByAdmin()
        self.open_add_role.show()

    def leaving(self):
        log = open('sysfiles/log.txt', 'r')
        data = log.readlines()
        print(data)
        log.close()
        log = open('sysfiles/log.txt', 'w')
        for i in data:
            if i != "\n":
                print(i, file=log)
        print('leaving', datetime.datetime.today(), socket.gethostbyname(socket.gethostname()), self.login,
              "Администратор/разработчик системы", sep=' - ',
              file=log)
        log.close()

        self.reauth = AuthorizationWindow()
        self.reauth.show()
        self.close()

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

        self.setWindowTitle('Профиль - ' + self.login)

        self.your_login.setText("Ваш логин: " + login)
        self.your_password.setText("Ваша должность: " + posit)
        # описание деятельности

        self.action.triggered.connect(self.leavingThis)

    def leavingThis(self):
        log = open('sysfiles/log.txt', 'r')
        data = log.readlines()
        print(data)
        log.close()
        log = open('sysfiles/log.txt', 'w')
        for i in data:
            if i != "\n":
                print(i, file=log)
        print('leaving', datetime.datetime.today(), socket.gethostbyname(socket.gethostname()), self.login, self.posit,
              sep=' - ',
              file=log)
        log.close()

        self.reauth = AuthorizationWindow()
        self.reauth.show()
        self.close()


class AuthorizationWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(AuthorizationWindow, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # finish = QtWidgets.QAction("Quit", self)
        # finish.triggered.connect(self.closeEvent)

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

                self.blockinWindow = BlockWind()
                self.blockinWindow.show()

                self.close()

            else:
                self.error = ErrorWindow(3 - times_trying_to_auth)
                self.error.show()

        else:
            posit = account_data[0][1]

            conn.close()

            log = open('sysfiles/log.txt', 'r')
            data = log.readlines()
            print(data)
            log.close()
            log = open('sysfiles/log.txt', 'w')
            for i in data:
                if i != "\n":
                    print(i, file=log)
            print('login', datetime.datetime.today(), socket.gethostbyname(socket.gethostname()), login, posit,
                  sep=' - ',
                  file=log)
            log.close()

            if posit == "Администратор/разработчик системы":
                self.windadm = MainWindowAdmin(login)
                self.windadm.show()
            else:
                self.wind = MainWindowUser(login, posit)
                self.wind.show()
            self.close()


def main():
    app = QtWidgets.QApplication(argv)
    application = AuthorizationWindow()
    application.show()

    exit(app.exec_())


if __name__ == "__main__":
    main()
