# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyLogBookWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from RichTextEdit import RichTextEditWidget
from ccalendar import CCalendar
from log_browser import LogBrowser
from log_entry_tree import CLogEntryTree
import PyLogBook_rc

class Ui_PyLogBookWindow(object):
    def setupUi(self, PyLogBookWindow):
        if not PyLogBookWindow.objectName():
            PyLogBookWindow.setObjectName(u"PyLogBookWindow")
        PyLogBookWindow.resize(1264, 793)
        self.actionOpen = QAction(PyLogBookWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExit = QAction(PyLogBookWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout_PyLogBook = QAction(PyLogBookWindow)
        self.actionAbout_PyLogBook.setObjectName(u"actionAbout_PyLogBook")
        self.actionAbout_Qt = QAction(PyLogBookWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        self.actionNew_Log_File = QAction(PyLogBookWindow)
        self.actionNew_Log_File.setObjectName(u"actionNew_Log_File")
        self.actionClose = QAction(PyLogBookWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionPreferences = QAction(PyLogBookWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionExport_XML = QAction(PyLogBookWindow)
        self.actionExport_XML.setObjectName(u"actionExport_XML")
        self.actionImport_XML = QAction(PyLogBookWindow)
        self.actionImport_XML.setObjectName(u"actionImport_XML")
        self.actionSearch = QAction(PyLogBookWindow)
        self.actionSearch.setObjectName(u"actionSearch")
        icon = QIcon()
        icon.addFile(u":/PyLogBook/Resources/Search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSearch.setIcon(icon)
        self.actionSearch.setMenuRole(QAction.MenuRole.NoRole)
        self.centralWidget = QWidget(PyLogBookWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.logEntryTree = CLogEntryTree(self.centralWidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Log Entries");
        self.logEntryTree.setHeaderItem(__qtreewidgetitem)
        self.logEntryTree.setObjectName(u"logEntryTree")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logEntryTree.sizePolicy().hasHeightForWidth())
        self.logEntryTree.setSizePolicy(sizePolicy)
        self.logEntryTree.setHeaderHidden(False)

        self.verticalLayout_3.addWidget(self.logEntryTree)

        self.curMonth = CCalendar(self.centralWidget)
        self.curMonth.setObjectName(u"curMonth")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.curMonth.sizePolicy().hasHeightForWidth())
        self.curMonth.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.curMonth)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.centralWidget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.logBrowser = LogBrowser(self.centralWidget)
        self.logBrowser.setObjectName(u"logBrowser")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy2)
        self.verticalLayout_4 = QVBoxLayout(self.logBrowser)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout.addWidget(self.logBrowser)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.centralWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(2)
        self.logDateLabel_2 = QLabel(self.centralWidget)
        self.logDateLabel_2.setObjectName(u"logDateLabel_2")
        font1 = QFont()
        font1.setBold(True)
        self.logDateLabel_2.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.logDateLabel_2)

        self.logDateLabel = QLabel(self.centralWidget)
        self.logDateLabel.setObjectName(u"logDateLabel")
        self.logDateLabel.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.logDateLabel)

        self.lastModificationDateLabel_2 = QLabel(self.centralWidget)
        self.lastModificationDateLabel_2.setObjectName(u"lastModificationDateLabel_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lastModificationDateLabel_2)

        self.lastModificationDateLabel = QLabel(self.centralWidget)
        self.lastModificationDateLabel.setObjectName(u"lastModificationDateLabel")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lastModificationDateLabel)

        self.numChangesLabel_2 = QLabel(self.centralWidget)
        self.numChangesLabel_2.setObjectName(u"numChangesLabel_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.numChangesLabel_2)

        self.numChangesLabel = QLabel(self.centralWidget)
        self.numChangesLabel.setObjectName(u"numChangesLabel")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.numChangesLabel)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.logEdit = RichTextEditWidget(self.centralWidget)
        self.logEdit.setObjectName(u"logEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(1)
        sizePolicy3.setHeightForWidth(self.logEdit.sizePolicy().hasHeightForWidth())
        self.logEdit.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.logEdit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.centralWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.tagsEdit = QLineEdit(self.centralWidget)
        self.tagsEdit.setObjectName(u"tagsEdit")

        self.horizontalLayout_2.addWidget(self.tagsEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addendumButton = QPushButton(self.centralWidget)
        self.addendumButton.setObjectName(u"addendumButton")

        self.horizontalLayout.addWidget(self.addendumButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.deleteButton = QPushButton(self.centralWidget)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout.addWidget(self.deleteButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.submitButton = QPushButton(self.centralWidget)
        self.submitButton.setObjectName(u"submitButton")

        self.horizontalLayout.addWidget(self.submitButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        PyLogBookWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(PyLogBookWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1264, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuSearch = QMenu(self.menuBar)
        self.menuSearch.setObjectName(u"menuSearch")
        PyLogBookWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSearch.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew_Log_File)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_XML)
        self.menuFile.addAction(self.actionExport_XML)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout_PyLogBook)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuSettings.addAction(self.actionPreferences)
        self.menuSearch.addAction(self.actionSearch)

        self.retranslateUi(PyLogBookWindow)

        QMetaObject.connectSlotsByName(PyLogBookWindow)
    # setupUi

    def retranslateUi(self, PyLogBookWindow):
        PyLogBookWindow.setWindowTitle(QCoreApplication.translate("PyLogBookWindow", u"PyLogBook", None))
        self.actionOpen.setText(QCoreApplication.translate("PyLogBookWindow", u"Open Log File...", None))
        self.actionExit.setText(QCoreApplication.translate("PyLogBookWindow", u"Exit", None))
        self.actionAbout_PyLogBook.setText(QCoreApplication.translate("PyLogBookWindow", u"About PyLogBook", None))
        self.actionAbout_Qt.setText(QCoreApplication.translate("PyLogBookWindow", u"About Qt", None))
        self.actionNew_Log_File.setText(QCoreApplication.translate("PyLogBookWindow", u"New Log File...", None))
        self.actionClose.setText(QCoreApplication.translate("PyLogBookWindow", u"Close", None))
        self.actionPreferences.setText(QCoreApplication.translate("PyLogBookWindow", u"Preferences...", None))
        self.actionExport_XML.setText(QCoreApplication.translate("PyLogBookWindow", u"Export XML...", None))
        self.actionImport_XML.setText(QCoreApplication.translate("PyLogBookWindow", u"Import XML...", None))
        self.actionSearch.setText(QCoreApplication.translate("PyLogBookWindow", u"Search...", None))
        self.label_2.setText(QCoreApplication.translate("PyLogBookWindow", u"Log Browser", None))
        self.label_3.setText(QCoreApplication.translate("PyLogBookWindow", u"Log Editor", None))
        self.logDateLabel_2.setText(QCoreApplication.translate("PyLogBookWindow", u"Log Entry:", None))
        self.logDateLabel.setText(QCoreApplication.translate("PyLogBookWindow", u"-", None))
        self.lastModificationDateLabel_2.setText(QCoreApplication.translate("PyLogBookWindow", u"Last Modified:", None))
        self.lastModificationDateLabel.setText(QCoreApplication.translate("PyLogBookWindow", u"-", None))
        self.numChangesLabel_2.setText(QCoreApplication.translate("PyLogBookWindow", u"Number of Changes:", None))
        self.numChangesLabel.setText(QCoreApplication.translate("PyLogBookWindow", u"-", None))
        self.label.setText(QCoreApplication.translate("PyLogBookWindow", u"Tags", None))
        self.addendumButton.setText(QCoreApplication.translate("PyLogBookWindow", u"Add Addendum", None))
        self.deleteButton.setText(QCoreApplication.translate("PyLogBookWindow", u"Delete Entry", None))
        self.submitButton.setText(QCoreApplication.translate("PyLogBookWindow", u"Save Entry", None))
        self.menuFile.setTitle(QCoreApplication.translate("PyLogBookWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("PyLogBookWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("PyLogBookWindow", u"Settings", None))
        self.menuSearch.setTitle(QCoreApplication.translate("PyLogBookWindow", u"Search", None))
    # retranslateUi

