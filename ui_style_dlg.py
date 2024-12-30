# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'style_dlg.ui'
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
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ColorButton import CColorButton
import PyLogBook_rc

class Ui_CStyleDlg(object):
    def setupUi(self, CStyleDlg):
        if not CStyleDlg.objectName():
            CStyleDlg.setObjectName(u"CStyleDlg")
        CStyleDlg.resize(369, 418)
        self.verticalLayout = QVBoxLayout(CStyleDlg)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(CStyleDlg)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_2)

        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(CStyleDlg)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.styleNameEdit = QLineEdit(CStyleDlg)
        self.styleNameEdit.setObjectName(u"styleNameEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.styleNameEdit)

        self.label_5 = QLabel(CStyleDlg)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.descriptionEdit = QLineEdit(CStyleDlg)
        self.descriptionEdit.setObjectName(u"descriptionEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.descriptionEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fontButton = QPushButton(CStyleDlg)
        self.fontButton.setObjectName(u"fontButton")

        self.horizontalLayout.addWidget(self.fontButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(CStyleDlg)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.fontLabel = QLabel(CStyleDlg)
        self.fontLabel.setObjectName(u"fontLabel")

        self.verticalLayout.addWidget(self.fontLabel)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_3 = QLabel(CStyleDlg)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.line = QFrame(CStyleDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(CStyleDlg)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.fgColorToolButton = CColorButton(CStyleDlg)
        self.fgColorToolButton.setObjectName(u"fgColorToolButton")
        self.fgColorToolButton.setEnabled(True)
        icon = QIcon()
        icon.addFile(u":/PyLogBook/Resources/Text Foreground.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fgColorToolButton.setIcon(icon)

        self.gridLayout.addWidget(self.fgColorToolButton, 0, 1, 1, 1)

        self.label_7 = QLabel(CStyleDlg)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)

        self.bgColorToolButton = CColorButton(CStyleDlg)
        self.bgColorToolButton.setObjectName(u"bgColorToolButton")
        self.bgColorToolButton.setEnabled(True)
        icon1 = QIcon()
        icon1.addFile(u":/PyLogBook/Resources/Text Background.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bgColorToolButton.setIcon(icon1)

        self.gridLayout.addWidget(self.bgColorToolButton, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.sampleLabel = QLabel(CStyleDlg)
        self.sampleLabel.setObjectName(u"sampleLabel")
        self.sampleLabel.setMinimumSize(QSize(0, 25))
        self.sampleLabel.setFrameShape(QFrame.Box)
        self.sampleLabel.setTextFormat(Qt.RichText)

        self.verticalLayout.addWidget(self.sampleLabel)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.buttonBox = QDialogButtonBox(CStyleDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CStyleDlg)
        self.buttonBox.rejected.connect(CStyleDlg.reject)
        self.buttonBox.accepted.connect(CStyleDlg.accept)

        QMetaObject.connectSlotsByName(CStyleDlg)
    # setupUi

    def retranslateUi(self, CStyleDlg):
        CStyleDlg.setWindowTitle(QCoreApplication.translate("CStyleDlg", u"Style Editor", None))
        self.label_2.setText(QCoreApplication.translate("CStyleDlg", u"Specify which font elements will be selected by the style.  Items that are not checked will not be a part of the style.", None))
        self.label_4.setText(QCoreApplication.translate("CStyleDlg", u"Style Name:", None))
        self.label_5.setText(QCoreApplication.translate("CStyleDlg", u"Description:", None))
        self.fontButton.setText(QCoreApplication.translate("CStyleDlg", u"Choose Font...", None))
        self.label.setText(QCoreApplication.translate("CStyleDlg", u"Font:", None))
        self.fontLabel.setText(QCoreApplication.translate("CStyleDlg", u"font", None))
        self.label_3.setText(QCoreApplication.translate("CStyleDlg", u"Text Color", None))
        self.label_6.setText(QCoreApplication.translate("CStyleDlg", u"Text Color", None))
        self.fgColorToolButton.setText("")
        self.label_7.setText(QCoreApplication.translate("CStyleDlg", u"Background Color", None))
        self.bgColorToolButton.setText("")
        self.sampleLabel.setText(QCoreApplication.translate("CStyleDlg", u"Style looks like this", None))
    # retranslateUi

