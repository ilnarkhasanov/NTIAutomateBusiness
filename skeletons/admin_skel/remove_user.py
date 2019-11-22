# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remove_user.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(471, 102)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 30, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(200, 30, 261, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.registerNewUser = QtWidgets.QPushButton(Form)
        self.registerNewUser.setGeometry(QtCore.QRect(10, 60, 451, 28))
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
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Логин пользователя: "))
        self.registerNewUser.setText(_translate("Form", "Регистрация"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
