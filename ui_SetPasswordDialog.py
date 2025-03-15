# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetPasswordDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SetPasswordDlg(object):
    def setupUi(self, SetPasswordDlg):
        if not SetPasswordDlg.objectName():
            SetPasswordDlg.setObjectName(u"SetPasswordDlg")
        SetPasswordDlg.resize(371, 367)
        self.verticalLayout = QVBoxLayout(SetPasswordDlg)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SetPasswordDlg)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_2 = QLabel(SetPasswordDlg)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.passwordEdit = QLineEdit(SetPasswordDlg)
        self.passwordEdit.setObjectName(u"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.passwordEdit)

        self.label_3 = QLabel(SetPasswordDlg)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.reEnterPasswordEdit = QLineEdit(SetPasswordDlg)
        self.reEnterPasswordEdit.setObjectName(u"reEnterPasswordEdit")
        self.reEnterPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.reEnterPasswordEdit)

        self.passwordsNotMatchLabel = QLabel(SetPasswordDlg)
        self.passwordsNotMatchLabel.setObjectName(u"passwordsNotMatchLabel")
        font = QFont()
        font.setPointSize(11)
        self.passwordsNotMatchLabel.setFont(font)
        self.passwordsNotMatchLabel.setStyleSheet(u"color: red")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.passwordsNotMatchLabel)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 21, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.noPasswordButton = QPushButton(SetPasswordDlg)
        self.noPasswordButton.setObjectName(u"noPasswordButton")
        self.noPasswordButton.setMinimumSize(QSize(95, 0))

        self.horizontalLayout.addWidget(self.noPasswordButton)

        self.buttonBox = QDialogButtonBox(SetPasswordDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(SetPasswordDlg)
        self.buttonBox.rejected.connect(SetPasswordDlg.reject)

        QMetaObject.connectSlotsByName(SetPasswordDlg)
    # setupUi

    def retranslateUi(self, SetPasswordDlg):
        SetPasswordDlg.setWindowTitle(QCoreApplication.translate("SetPasswordDlg", u"Set Log Password", None))
        self.label.setText(QCoreApplication.translate("SetPasswordDlg", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Here you can set the password for your log file. A password is not required, but without a password, anyone can view your log entries.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">To create a log file without a password, either leave t"
                        "he password field blank, or click the &quot;No Password&quot; button.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">If you do decide to use a password, write it down and keep it in a safe place, or use a password management program to remember it.  The password </span><span style=\" font-size:8pt; font-weight:600;\">is required</span><span style=\" font-size:8pt;\"> to access the log file.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font"
                        "-weight:600;\">Without the password, it will be impossible to access, export, print or otherwise view the log file.  If the password is lost, the contents of the log file cannot be retrieved.  Take care to ensure the safety of the password.</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("SetPasswordDlg", u"Password", None))
        self.label_3.setText(QCoreApplication.translate("SetPasswordDlg", u"Re-enter Password", None))
        self.passwordsNotMatchLabel.setText(QCoreApplication.translate("SetPasswordDlg", u"Passwords do not match", None))
        self.noPasswordButton.setText(QCoreApplication.translate("SetPasswordDlg", u"No Password", None))
    # retranslateUi

