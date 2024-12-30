# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RichTextEdit.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFontComboBox, QHBoxLayout,
    QSizePolicy, QSpacerItem, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

from ColorButton import CColorButton
import PyLogBook_rc

class Ui_RichTextEditWidget(object):
    def setupUi(self, RichTextEditWidget):
        if not RichTextEditWidget.objectName():
            RichTextEditWidget.setObjectName(u"RichTextEditWidget")
        RichTextEditWidget.resize(474, 628)
        self.verticalLayout = QVBoxLayout(RichTextEditWidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fontCombo = QFontComboBox(RichTextEditWidget)
        self.fontCombo.setObjectName(u"fontCombo")
        self.fontCombo.setEditable(False)

        self.horizontalLayout_2.addWidget(self.fontCombo)

        self.sizeCombo = QComboBox(RichTextEditWidget)
        self.sizeCombo.setObjectName(u"sizeCombo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizeCombo.sizePolicy().hasHeightForWidth())
        self.sizeCombo.setSizePolicy(sizePolicy)
        self.sizeCombo.setMinimumSize(QSize(50, 0))
        self.sizeCombo.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_2.addWidget(self.sizeCombo)

        self.leftAlignButton = QToolButton(RichTextEditWidget)
        self.leftAlignButton.setObjectName(u"leftAlignButton")
        icon = QIcon()
        icon.addFile(u":/PyLogBook/Resources/Left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.leftAlignButton.setIcon(icon)
        self.leftAlignButton.setIconSize(QSize(16, 16))
        self.leftAlignButton.setCheckable(True)
        self.leftAlignButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.leftAlignButton)

        self.centerAlignButton = QToolButton(RichTextEditWidget)
        self.centerAlignButton.setObjectName(u"centerAlignButton")
        icon1 = QIcon()
        icon1.addFile(u":/PyLogBook/Resources/Center.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.centerAlignButton.setIcon(icon1)
        self.centerAlignButton.setIconSize(QSize(16, 16))
        self.centerAlignButton.setCheckable(True)
        self.centerAlignButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.centerAlignButton)

        self.rightAlignButton = QToolButton(RichTextEditWidget)
        self.rightAlignButton.setObjectName(u"rightAlignButton")
        icon2 = QIcon()
        icon2.addFile(u":/PyLogBook/Resources/Right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.rightAlignButton.setIcon(icon2)
        self.rightAlignButton.setIconSize(QSize(16, 16))
        self.rightAlignButton.setCheckable(True)
        self.rightAlignButton.setAutoExclusive(True)

        self.horizontalLayout_2.addWidget(self.rightAlignButton)

        self.boldButton = QToolButton(RichTextEditWidget)
        self.boldButton.setObjectName(u"boldButton")
        font = QFont()
        font.setBold(True)
        self.boldButton.setFont(font)
        icon3 = QIcon()
        icon3.addFile(u":/PyLogBook/Resources/Bold.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.boldButton.setIcon(icon3)
        self.boldButton.setIconSize(QSize(16, 16))
        self.boldButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.boldButton)

        self.italicButton = QToolButton(RichTextEditWidget)
        self.italicButton.setObjectName(u"italicButton")
        font1 = QFont()
        font1.setItalic(True)
        self.italicButton.setFont(font1)
        icon4 = QIcon()
        icon4.addFile(u":/PyLogBook/Resources/Italic.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.italicButton.setIcon(icon4)
        self.italicButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.italicButton)

        self.underlineButton = QToolButton(RichTextEditWidget)
        self.underlineButton.setObjectName(u"underlineButton")
        font2 = QFont()
        font2.setUnderline(True)
        self.underlineButton.setFont(font2)
        icon5 = QIcon()
        icon5.addFile(u":/PyLogBook/Resources/Underline.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.underlineButton.setIcon(icon5)
        self.underlineButton.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.underlineButton)

        self.bulletTableInsertButton = QToolButton(RichTextEditWidget)
        self.bulletTableInsertButton.setObjectName(u"bulletTableInsertButton")
        icon6 = QIcon()
        icon6.addFile(u":/PyLogBook/Resources/Bullet Table.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bulletTableInsertButton.setIcon(icon6)

        self.horizontalLayout_2.addWidget(self.bulletTableInsertButton)

        self.numberTableInsertButton = QToolButton(RichTextEditWidget)
        self.numberTableInsertButton.setObjectName(u"numberTableInsertButton")
        icon7 = QIcon()
        icon7.addFile(u":/PyLogBook/Resources/Number Table.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.numberTableInsertButton.setIcon(icon7)

        self.horizontalLayout_2.addWidget(self.numberTableInsertButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.styleButton = QToolButton(RichTextEditWidget)
        self.styleButton.setObjectName(u"styleButton")
        self.styleButton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.styleButton)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.textColorButton = CColorButton(RichTextEditWidget)
        self.textColorButton.setObjectName(u"textColorButton")
        icon8 = QIcon()
        icon8.addFile(u":/PyLogBook/Resources/Text Foreground.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.textColorButton.setIcon(icon8)
        self.textColorButton.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.textColorButton)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.textBackgroundButton = CColorButton(RichTextEditWidget)
        self.textBackgroundButton.setObjectName(u"textBackgroundButton")
        icon9 = QIcon()
        icon9.addFile(u":/PyLogBook/Resources/Text Background.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.textBackgroundButton.setIcon(icon9)
        self.textBackgroundButton.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.textBackgroundButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textEdit = QTextEdit(RichTextEditWidget)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)


        self.retranslateUi(RichTextEditWidget)

        QMetaObject.connectSlotsByName(RichTextEditWidget)
    # setupUi

    def retranslateUi(self, RichTextEditWidget):
        RichTextEditWidget.setWindowTitle(QCoreApplication.translate("RichTextEditWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.fontCombo.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Font", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sizeCombo.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Font Size", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.leftAlignButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Left Alignment", None))
#endif // QT_CONFIG(tooltip)
        self.leftAlignButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Left", None))
#if QT_CONFIG(tooltip)
        self.centerAlignButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Center Alignment", None))
#endif // QT_CONFIG(tooltip)
        self.centerAlignButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Center", None))
#if QT_CONFIG(tooltip)
        self.rightAlignButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Right Alignment", None))
#endif // QT_CONFIG(tooltip)
        self.rightAlignButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Right", None))
#if QT_CONFIG(tooltip)
        self.boldButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Bold", None))
#endif // QT_CONFIG(tooltip)
        self.boldButton.setText(QCoreApplication.translate("RichTextEditWidget", u"B", None))
#if QT_CONFIG(tooltip)
        self.italicButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Italic", None))
#endif // QT_CONFIG(tooltip)
        self.italicButton.setText(QCoreApplication.translate("RichTextEditWidget", u"I", None))
#if QT_CONFIG(tooltip)
        self.underlineButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Underline", None))
#endif // QT_CONFIG(tooltip)
        self.underlineButton.setText(QCoreApplication.translate("RichTextEditWidget", u"u", None))
#if QT_CONFIG(tooltip)
        self.bulletTableInsertButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Bulleted Table", None))
#endif // QT_CONFIG(tooltip)
        self.bulletTableInsertButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Table", None))
#if QT_CONFIG(tooltip)
        self.numberTableInsertButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Numbered Table", None))
#endif // QT_CONFIG(tooltip)
        self.numberTableInsertButton.setText(QCoreApplication.translate("RichTextEditWidget", u".", None))
#if QT_CONFIG(tooltip)
        self.styleButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Style", None))
#endif // QT_CONFIG(tooltip)
        self.styleButton.setText(QCoreApplication.translate("RichTextEditWidget", u"Apply Style...", None))
#if QT_CONFIG(tooltip)
        self.textColorButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Text (Foreground) Color", None))
#endif // QT_CONFIG(tooltip)
        self.textColorButton.setText("")
#if QT_CONFIG(tooltip)
        self.textBackgroundButton.setToolTip(QCoreApplication.translate("RichTextEditWidget", u"Background Color", None))
#endif // QT_CONFIG(tooltip)
        self.textBackgroundButton.setText("")
    # retranslateUi

