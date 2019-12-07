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
from skeletons.admin_skel.remove_role import Ui_Form as RemoveRoleSkeleton
from skeletons.putter_skel.add_detail import Ui_Form as Putter_AddDetailSkeleton
from skeletons.mainwind_kladov import Ui_MainWindow as Mw_kladov
from skeletons.putter_skel.giving_the_access import Ui_Form as Putter_GivingAccessSkeleton
from skeletons.putter_skel.depriving_the_access import Ui_Form as Putter_DeprivingAccessSkeleton
import socket
import datetime
import sqlite3
import xlsxwriter
import xlrd
import xlwt
from xlutils.copy import copy

times_trying_to_auth = 0
possible_symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

get_row = open('sysfiles/rowis.txt', 'r')
row = int(get_row.readline())
get_row.close()

get_wrong_row = open('sysfiles/wrong_times.txt', 'r')
wrong_row = int(get_wrong_row.readline())
get_wrong_row.close()


class DepriveAccessWindow(QtWidgets.QWidget, Putter_DeprivingAccessSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()
        c.execute('SELECT login FROM abilityToAddDetail;')
        for i in c.fetchall():
            self.loginsCombo.addItem(i[0])
        conn.close()

        self.depriveAccessButton.clicked.connect(self.depriving)

    def depriving(self):
        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute(f'SELECT posit FROM data WHERE login="{self.loginsCombo.currentText()}"')
        print(c.fetchall()[0][0])

        if c.fetchall()[0][0] == "Кладовщик":
            QtWidgets.QMessageBox.about(self, 'Внимание!', 'Нельзя лишить кладовщика доступа к добавлению деталей')
        else:
            c.execute(f'DELETE FROM abilityToAddDetail WHERE login="{self.loginsCombo.currentText()}";')
            conn.commit()
            QtWidgets.QMessageBox.about(self, 'Внимание!',
                                        f'Пользователь {self.loginsCombo.currentText()} больше не имеет доступа к '
                                        f'добавлению деталей')
        conn.close()


class GiveAccessWindow(QtWidgets.QWidget, Putter_GivingAccessSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute('SELECT login FROM data;')

        logins = []

        for i in c.fetchall():
            logins.append(i[0])

        for i in logins:
            self.loginsCombo.addItem(i)

        conn.close()

        self.giveAccessButton.clicked.connect(self.giving)

    def giving(self):
        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()
        c.execute(f'SELECT login FROM abilityToAddDetail WHERE login="{self.loginsCombo.currentText()}";')
        if len(c.fetchall()):
            QtWidgets.QMessageBox.about(self, 'Внимание!',
                                        f'Пользователь {self.loginsCombo.currentText()} уже имеет доступ к добавлению деталей')
        else:
            c.execute(f'INSERT INTO abilityToAddDetail (login) VALUES ("{self.loginsCombo.currentText()}")')
            conn.commit()
            QtWidgets.QMessageBox.about(self, 'Внимание!',
                                        f'Пользователь {self.loginsCombo.currentText()} получил доступ к добавлению деталей')
        conn.close()


class AddDetailWindow(QtWidgets.QWidget, Putter_AddDetailSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.addButton.clicked.connect(self.adding)

    def adding(self):
        global row, possible_symbols, wrong_row

        rb = xlrd.open_workbook('WrongDetails.xls')
        wb = copy(rb)
        sheet = wb.get_sheet("data")

        data = [self.nameOfDetail.toPlainText(),
                self.Type.toPlainText(),
                self.Weight.toPlainText(),
                self.Article.toPlainText(),
                self.YearOfIssue.date().toString()]

        if len(self.nameOfDetail.toPlainText()) < 100:
            QtWidgets.QMessageBox.about(self, 'Внимание!', 'Формат названия детали неверен')
            sheet.write(wrong_row, 0, self.nameOfDetail.toPlainText())
            sheet.write(wrong_row, 1, self.Type.toPlainText())
            sheet.write(wrong_row, 2, self.Weight.toPlainText())
            sheet.write(wrong_row, 3, self.Article.toPlainText())
            sheet.write(wrong_row, 4, self.YearOfIssue.date().toString())

            wrong_row += 1
            set_new_wrong = open('sysfiles/wrong_times.txt', 'w')
            print(wrong_row, file=set_new_wrong)
            set_new_wrong.close()

            wb.save('WrongDetails.xls')
            return

        if '' in data:
            QtWidgets.QMessageBox.about(self, 'Внимание!', 'Данные введены неверно')
            sheet.write(wrong_row, 0, self.nameOfDetail.toPlainText())
            sheet.write(wrong_row, 1, self.Type.toPlainText())
            sheet.write(wrong_row, 2, self.Weight.toPlainText())
            sheet.write(wrong_row, 3, self.Article.toPlainText())
            sheet.write(wrong_row, 4, self.YearOfIssue.date().toString())

            wrong_row += 1
            set_new_wrong = open('sysfiles/wrong_times.txt', 'w')
            print(wrong_row, file=set_new_wrong)
            set_new_wrong.close()

            wb.save('WrongDetails.xls')
            return

        for symbol in self.Article.toPlainText():
            if symbol not in possible_symbols:
                QtWidgets.QMessageBox.about(self, 'Внимание!', 'Формат артикля детали неверен')
                sheet.write(wrong_row, 0, self.nameOfDetail.toPlainText())
                sheet.write(wrong_row, 1, self.Type.toPlainText())
                sheet.write(wrong_row, 2, self.Weight.toPlainText())
                sheet.write(wrong_row, 3, self.Article.toPlainText())
                sheet.write(wrong_row, 4, self.YearOfIssue.date().toString())

                wrong_row += 1
                set_new_wrong = open('sysfiles/wrong_times.txt', 'w')
                print(wrong_row, file=set_new_wrong)
                set_new_wrong.close()

                wb.save('WrongDetails.xls')
                return

        wb.save('WrongDetails.xls')

        rb = xlrd.open_workbook('Details.xls')
        wb = copy(rb)

        isUsed = open('sysfiles/used.txt', 'r')
        for detail in isUsed.readlines():
            flag = True
            for i in range(len(detail.split(' - '))):
                if detail.split(' - ')[i] != data[i]:
                    flag = False
            if flag:
                QtWidgets.QMessageBox.about(self, 'Внимание!',
                                            'Такая деталь уже существует!')
                isUsed.close()
                return

        self.YearOfIssue.setDisplayFormat("dd/MM/yyyy")

        sheet = wb.get_sheet("data")

        sheet.write(row, 0, self.nameOfDetail.toPlainText())
        sheet.write(row, 1, self.Type.toPlainText())
        sheet.write(row, 2, self.Weight.toPlainText())
        sheet.write(row, 3, self.Article.toPlainText())
        sheet.write(row, 4, self.YearOfIssue.date().toString())

        wb.save('Details.xls')

        row += 1
        set_row = open('sysfiles/rowis.txt', 'w')
        print(str(row), file=set_row)
        set_row.close()

        log = open('sysfiles/used.txt', 'r')
        dataDoc = log.readlines()
        log.close()
        logDetail = open('sysfiles/used.txt', 'w')
        for i in dataDoc:
            if i != "\n":
                print(i, file=logDetail)
        print(' - '.join(data))
        logDetail.close()

        QtWidgets.QMessageBox.about(self, "Внимание!", "Деталь успешно загружена")


class RemoveRoleWindow(QtWidgets.QWidget, RemoveRoleSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM roles;')

        for i in c.fetchall():
            self.rolesBox.addItem(i[0])

        conn.close()

        self.deleteRole.clicked.connect(self.deleting_role_func)

    def deleting_role_func(self):
        role = self.rolesBox.currentText()

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute(f'DELETE FROM roles WHERE posit="{role}"')
        conn.commit()

        conn.close()

        QtWidgets.QMessageBox.about(self, 'Внимание!', f'Роль "{role}" успешно удалена')

        self.close()


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
            conn.commit()
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

                if posit == 'Кладовщик':
                    c.execute(f'INSERT INTO abilityToAddDetail (login) VALUES ("{login}")')
                    conn.commit()

                conn.commit()
                conn.close()

                QtWidgets.QMessageBox.about(self, 'Внимание!', f'Пользователь с логином "{login}" успешно добавлен!')

            self.close()


class RemovingUserByAdmin(QtWidgets.QWidget, RemovingUserSkeleton):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.deleteUser.setText('Удалить')

        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute('SELECT login FROM data;')

        for i in c.fetchall():
            self.userBox.addItem(i[0])

        conn.close()

        self.deleteUser.clicked.connect(self.removingUserFunc)

    def removingUserFunc(self):
        conn = sqlite3.connect('databases/data.db')
        c = conn.cursor()

        c.execute(f'DELETE FROM data WHERE login="{self.userBox.currentText()}"')
        conn.commit()

        c.execute(f'DELETE FROM abilityToAddDetail WHERE login="{self.userBox.currentText()}"')
        conn.commit()

        conn.close()

        QtWidgets.QMessageBox.about(self, 'Внимание!',
                                    f'Пользователь с логином {self.userBox.currentText()} успешно удалён')

        self.close()


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
        self.removeRoleButton.clicked.connect(self.removing_role)

        self.action.triggered.connect(self.leaving)

    def removing_role(self):
        self.remove_role_func = RemoveRoleWindow()
        self.remove_role_func.show()

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


class MainWindowKladov(QtWidgets.QMainWindow, Mw_kladov):
    def __init__(self, login, posit):
        super().__init__()
        self.setupUi(self)

        self.login = login
        self.posit = posit

        self.setWindowTitle('Профиль - ' + login)

        if posit == "Кладовщик":
            self.giveAccessButton.setEnabled(1)
            self.depriveAccessButton.setEnabled(1)

        self.your_login.setText('Ваш логин: ' + login)
        self.your_posit.setText('Ваша должность: ' + posit)

        self.addDetail.clicked.connect(self.addingDetailFunc)
        self.giveAccessButton.clicked.connect(self.givingAccess)
        self.depriveAccessButton.clicked.connect(self.deprivingAccess)
        self.chooseDirButton.clicked.connect(self.choosingDir)
        self.chooseDirButtonWrong.clicked.connect()

        self.action.triggered.connect(self.leavingThis)

    def choosingDirWrong(self):
        fileway = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if fileway == "":
            return
        rb = xlrd.open_workbook('WrongDetails.xls')
        wb = copy(rb)
        wb.save('//'.join((fileway + '/WrongDetails.xls').split('/')))
        QtWidgets.QMessageBox.about(self, 'Внимание!', 'Данные успешно сохранены')

    def choosingDir(self):
        fileway = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if fileway == "":
            return
        rb = xlrd.open_workbook('Details.xls')
        wb = copy(rb)
        wb.save('//'.join((fileway + '/Details.xls').split('/')))
        QtWidgets.QMessageBox.about(self, 'Внимание!', 'Данные о деталях успешно сохранены')

    def deprivingAccess(self):
        self.depr = DepriveAccessWindow()
        self.depr.show()

    def givingAccess(self):
        self.giveAccessWind = GiveAccessWindow()
        self.giveAccessWind.show()

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

    def addingDetailFunc(self):
        self.addingDetail = AddDetailWindow()
        self.addingDetail.show()


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

            conn = sqlite3.connect('databases/data.db')
            c = conn.cursor()

            c.execute(f'SELECT login FROM abilityToAddDetail WHERE login="{login}"')

            if len(c.fetchall()):
                self.kladov_window = MainWindowKladov(login, posit)
                self.kladov_window.show()
            else:
                if posit == "Администратор/разработчик системы":
                    self.windadm = MainWindowAdmin(login)
                    self.windadm.show()
                else:
                    self.wind = MainWindowUser(login, posit)
                    self.wind.show()

            conn.close()
            self.close()


def main():
    app = QtWidgets.QApplication(argv)
    application = AuthorizationWindow()
    application.show()

    exit(app.exec_())


if __name__ == "__main__":
    main()
