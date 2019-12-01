# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_user.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(471, 123)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.loginOfNewUser = QtWidgets.QLineEdit(Form)
        self.loginOfNewUser.setGeometry(QtCore.QRect(200, 20, 261, 22))
        self.loginOfNewUser.setObjectName("loginOfNewUser")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 231, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.positionOfNewUser = QtWidgets.QComboBox(Form)
        self.positionOfNewUser.setGeometry(QtCore.QRect(240, 50, 221, 22))
        self.positionOfNewUser.setObjectName("positionOfNewUser")
        self.registerNewUser = QtWidgets.QPushButton(Form)
        self.registerNewUser.setGeometry(QtCore.QRect(10, 80, 451, 28))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.registerNewUser.setFont(font)
        self.registerNewUser.setObjectName("registerNewUser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить нового пользователя"))
        self.label.setText(_translate("Form", "Логин пользователя: "))
        self.label_2.setText(_translate("Form", "Дожлность пользователя: "))
        self.registerNewUser.setText(_translate("Form", "Регистрация"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
