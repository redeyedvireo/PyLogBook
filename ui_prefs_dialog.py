# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prefs_dialog.ui'
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
    QFontComboBox, QFormLayout, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        if not PrefsDialog.objectName():
            PrefsDialog.setObjectName(u"PrefsDialog")
        PrefsDialog.resize(526, 385)
        self.verticalLayout = QVBoxLayout(PrefsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = QListWidget(PrefsDialog)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout.addWidget(self.listWidget)

        self.stackedWidget = QStackedWidget(PrefsDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setSizeIncrement(QSize(0, 0))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.emptyWorkspaceRadio = QRadioButton(self.groupBox)
        self.emptyWorkspaceRadio.setObjectName(u"emptyWorkspaceRadio")

        self.verticalLayout_3.addWidget(self.emptyWorkspaceRadio)

        self.loadPreviousLogRadio = QRadioButton(self.groupBox)
        self.loadPreviousLogRadio.setObjectName(u"loadPreviousLogRadio")
        self.loadPreviousLogRadio.setChecked(True)

        self.verticalLayout_3.addWidget(self.loadPreviousLogRadio)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 204, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.defaultTextSizeSpin = QSpinBox(self.page_2)
        self.defaultTextSizeSpin.setObjectName(u"defaultTextSizeSpin")
        self.defaultTextSizeSpin.setMinimum(1)
        self.defaultTextSizeSpin.setValue(8)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.defaultTextSizeSpin)

        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.defaultFontCombo = QFontComboBox(self.page_2)
        self.defaultFontCombo.setObjectName(u"defaultFontCombo")
        font = QFont()
        font.setFamilies([u"Verdana"])
        font.setPointSize(10)
        self.defaultFontCombo.setCurrentFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.defaultFontCombo)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_5 = QVBoxLayout(self.page_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.page_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.logsPerPageSpin = QSpinBox(self.page_3)
        self.logsPerPageSpin.setObjectName(u"logsPerPageSpin")
        self.logsPerPageSpin.setMinimum(1)
        self.logsPerPageSpin.setMaximum(50)
        self.logsPerPageSpin.setValue(5)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.logsPerPageSpin)


        self.verticalLayout_5.addLayout(self.formLayout_2)

        self.stackedWidget.addWidget(self.page_3)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line = QFrame(PrefsDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(PrefsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PrefsDialog)
        self.buttonBox.accepted.connect(PrefsDialog.accept)
        self.buttonBox.rejected.connect(PrefsDialog.reject)
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(PrefsDialog)
    # setupUi

    def retranslateUi(self, PrefsDialog):
        PrefsDialog.setWindowTitle(QCoreApplication.translate("PrefsDialog", u"Preferences", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("PrefsDialog", u"General", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("PrefsDialog", u"Editor", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("PrefsDialog", u"Browser", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("PrefsDialog", u"On Startup", None))
        self.emptyWorkspaceRadio.setText(QCoreApplication.translate("PrefsDialog", u"Empty Workspace", None))
        self.loadPreviousLogRadio.setText(QCoreApplication.translate("PrefsDialog", u"Load Previous Log", None))
        self.label.setText(QCoreApplication.translate("PrefsDialog", u"Default text size", None))
        self.label_3.setText(QCoreApplication.translate("PrefsDialog", u"Default font family", None))
        self.label_2.setText(QCoreApplication.translate("PrefsDialog", u"Logs Per Page", None))
    # retranslateUi

