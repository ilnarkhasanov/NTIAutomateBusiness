# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'authorization.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 381, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labemkmkl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labemkmkl.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.labemkmkl.setFont(font)
        self.labemkmkl.setAlignment(QtCore.Qt.AlignCenter)
        self.labemkmkl.setObjectName("labemkmkl")
        self.verticalLayout.addWidget(self.labemkmkl)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.login = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.login.setObjectName("login")
        self.verticalLayout.addWidget(self.login)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.password = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        self.Authorization = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Authorization.setObjectName("Authorization")
        self.verticalLayout.addWidget(self.Authorization)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Авторизация"))
        self.labemkmkl.setText(_translate("Form", "Пользовательская система организации"))
        self.label_3.setText(_translate("Form", "Логин"))
        self.label.setText(_translate("Form", "Пароль"))
        self.Authorization.setText(_translate("Form", "Войти"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
