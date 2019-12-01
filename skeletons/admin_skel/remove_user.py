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
        Form.resize(471, 81)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.deleteUser = QtWidgets.QPushButton(Form)
        self.deleteUser.setGeometry(QtCore.QRect(10, 40, 451, 28))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.deleteUser.setFont(font)
        self.deleteUser.setObjectName("deleteUser")
        self.userBox = QtWidgets.QComboBox(Form)
        self.userBox.setGeometry(QtCore.QRect(200, 10, 261, 22))
        self.userBox.setObjectName("userBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Удалить пользователя"))
        self.label.setText(_translate("Form", "Логин пользователя: "))
        self.deleteUser.setText(_translate("Form", "Удалить пользователя"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
