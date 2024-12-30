# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_style_dlg.ui'
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
    QGroupBox, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)
import PyLogBook_rc

class Ui_SelectStyleDlg(object):
    def setupUi(self, SelectStyleDlg):
        if not SelectStyleDlg.objectName():
            SelectStyleDlg.setObjectName(u"SelectStyleDlg")
        SelectStyleDlg.resize(321, 413)
        SelectStyleDlg.setMinimumSize(QSize(242, 0))
        SelectStyleDlg.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_3 = QVBoxLayout(SelectStyleDlg)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.styleList = QListWidget(SelectStyleDlg)
        self.styleList.setObjectName(u"styleList")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.styleList.sizePolicy().hasHeightForWidth())
        self.styleList.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.styleList)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.newButton = QPushButton(SelectStyleDlg)
        self.newButton.setObjectName(u"newButton")
        icon = QIcon()
        icon.addFile(u":/PyLogBook/Resources/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.newButton.setIcon(icon)

        self.verticalLayout_2.addWidget(self.newButton)

        self.deleteButton = QPushButton(SelectStyleDlg)
        self.deleteButton.setObjectName(u"deleteButton")
        icon1 = QIcon()
        icon1.addFile(u":/PyLogBook/Resources/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon1)

        self.verticalLayout_2.addWidget(self.deleteButton)

        self.editButton = QPushButton(SelectStyleDlg)
        self.editButton.setObjectName(u"editButton")
        icon2 = QIcon()
        icon2.addFile(u":/PyLogBook/Resources/pencil.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editButton.setIcon(icon2)

        self.verticalLayout_2.addWidget(self.editButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.groupBox = QGroupBox(SelectStyleDlg)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descriptionEdit = QTextEdit(self.groupBox)
        self.descriptionEdit.setObjectName(u"descriptionEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.descriptionEdit.sizePolicy().hasHeightForWidth())
        self.descriptionEdit.setSizePolicy(sizePolicy2)
        self.descriptionEdit.setMaximumSize(QSize(16777215, 100))
        self.descriptionEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.descriptionEdit)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(SelectStyleDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy2.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy2)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.retranslateUi(SelectStyleDlg)
        self.buttonBox.accepted.connect(SelectStyleDlg.accept)
        self.buttonBox.rejected.connect(SelectStyleDlg.reject)

        QMetaObject.connectSlotsByName(SelectStyleDlg)
    # setupUi

    def retranslateUi(self, SelectStyleDlg):
        SelectStyleDlg.setWindowTitle(QCoreApplication.translate("SelectStyleDlg", u"Styles", None))
        self.newButton.setText("")
        self.deleteButton.setText("")
        self.editButton.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("SelectStyleDlg", u"Description", None))
    # retranslateUi

