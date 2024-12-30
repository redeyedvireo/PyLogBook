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
    QTabWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from RichTextEdit import RichTextEditWidget
from ccalendar import CCalendar
from log_browser import LogBrowser
from log_entry_tree import CLogEntryTree
import PyLogBook_rc

class Ui_PyLogBookWindow(object):
    def setupUi(self, PyLogBookWindow):
        if not PyLogBookWindow.objectName():
            PyLogBookWindow.setObjectName(u"PyLogBookWindow")
        PyLogBookWindow.resize(824, 793)
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
        self.logEntryTree.setHeaderHidden(False)

        self.verticalLayout_3.addWidget(self.logEntryTree)

        self.curMonth = CCalendar(self.centralWidget)
        self.curMonth.setObjectName(u"curMonth")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.curMonth.sizePolicy().hasHeightForWidth())
        self.curMonth.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.curMonth)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.South)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(2)
        self.logDateLabel_2 = QLabel(self.tab)
        self.logDateLabel_2.setObjectName(u"logDateLabel_2")
        font1 = QFont()
        font1.setBold(True)
        self.logDateLabel_2.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.logDateLabel_2)

        self.logDateLabel = QLabel(self.tab)
        self.logDateLabel.setObjectName(u"logDateLabel")
        self.logDateLabel.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.logDateLabel)

        self.lastModificationDateLabel_2 = QLabel(self.tab)
        self.lastModificationDateLabel_2.setObjectName(u"lastModificationDateLabel_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lastModificationDateLabel_2)

        self.lastModificationDateLabel = QLabel(self.tab)
        self.lastModificationDateLabel.setObjectName(u"lastModificationDateLabel")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lastModificationDateLabel)

        self.numChangesLabel_2 = QLabel(self.tab)
        self.numChangesLabel_2.setObjectName(u"numChangesLabel_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.numChangesLabel_2)

        self.numChangesLabel = QLabel(self.tab)
        self.numChangesLabel.setObjectName(u"numChangesLabel")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.numChangesLabel)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.logEdit = RichTextEditWidget(self.tab)
        self.logEdit.setObjectName(u"logEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.logEdit.sizePolicy().hasHeightForWidth())
        self.logEdit.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.logEdit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.tagsEdit = QLineEdit(self.tab)
        self.tagsEdit.setObjectName(u"tagsEdit")

        self.horizontalLayout_2.addWidget(self.tagsEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addendumButton = QPushButton(self.tab)
        self.addendumButton.setObjectName(u"addendumButton")

        self.horizontalLayout.addWidget(self.addendumButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.deleteButton = QPushButton(self.tab)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout.addWidget(self.deleteButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.submitButton = QPushButton(self.tab)
        self.submitButton.setObjectName(u"submitButton")

        self.horizontalLayout.addWidget(self.submitButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_6.addWidget(self.label_2)

        self.logBrowser = LogBrowser(self.tab_2)
        self.logBrowser.setObjectName(u"logBrowser")
        sizePolicy1.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.logBrowser)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout_6.addWidget(self.logBrowser)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        PyLogBookWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(PyLogBookWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 824, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        PyLogBookWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
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

        self.retranslateUi(PyLogBookWindow)

        self.tabWidget.setCurrentIndex(0)


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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("PyLogBookWindow", u"Editor", None))
        self.label_2.setText(QCoreApplication.translate("PyLogBookWindow", u"Log Browser", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("PyLogBookWindow", u"Browser", None))
        self.menuFile.setTitle(QCoreApplication.translate("PyLogBookWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("PyLogBookWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("PyLogBookWindow", u"Settings", None))
    # retranslateUi

