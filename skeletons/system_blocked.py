# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'system_blocked.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(352, 300)
        self.minutes_render = QtWidgets.QLCDNumber(Form)
        self.minutes_render.setGeometry(QtCore.QRect(20, 130, 151, 141))
        self.minutes_render.setObjectName("minutes_render")
        self.seconds_render = QtWidgets.QLCDNumber(Form)
        self.seconds_render.setGeometry(QtCore.QRect(180, 130, 151, 141))
        self.seconds_render.setObjectName("seconds_render")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 311, 111))
        font = QtGui.QFont()
        font.setFamily("Open Sans SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Система заблокирована"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Open Sans SemiBold\'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400;\">Система заблокирована, так как вы 3 раза ввели неправильный пароль.</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
