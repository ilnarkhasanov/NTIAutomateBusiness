# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'incorrect_password.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(701, 121)
        self.Hey = QtWidgets.QLabel(Form)
        self.Hey.setGeometry(QtCore.QRect(10, 30, 681, 51))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Hey.setFont(font)
        self.Hey.setAlignment(QtCore.Qt.AlignCenter)
        self.Hey.setObjectName("Hey")
        self.OK = QtWidgets.QPushButton(Form)
        self.OK.setGeometry(QtCore.QRect(20, 80, 661, 28))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.OK.setFont(font)
        self.OK.setObjectName("OK")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Hey.setText(_translate("Form", "Пароль введен неправильно! Количество оставшихся попыток: "))
        self.OK.setText(_translate("Form", "ОК"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
