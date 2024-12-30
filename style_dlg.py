from PySide6 import QtCore, QtGui, QtWidgets
from ui_style_dlg import Ui_CStyleDlg

from styleDef import FormatFlag, FormatFlags, StyleDef

class StyleDlg(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget, styleDef: StyleDef) -> None:
    super(StyleDlg, self).__init__(parent)

    self.ui = Ui_CStyleDlg()
    self.ui.setupUi(self)

    self.styleDef = styleDef
    self.currentFont = QtGui.QFont()

    self.populateDialog(styleDef)
    self.updateFontLabel()
    self.updateResultLabel()
    self.updateOkButton()

    self.ui.styleNameEdit.textChanged.connect(self.updateOkButton)
    self.ui.bgColorToolButton.colorChangedSignal.connect(self.onColorChanged)
    self.ui.fgColorToolButton.colorChangedSignal.connect(self.onColorChanged)
    self.ui.bgColorToolButton.noColorSignal.connect(self.onColorChanged)
    self.ui.fgColorToolButton.noColorSignal.connect(self.onColorChanged)

  def getStyle(self) -> StyleDef:
    fgColor = QtGui.QColor()
    bgColor = QtGui.QColor()

    #	For now, the style dialog is a simplified dialog, where every style item
    #	will be specified.  Later on, an "Advanced" button will be added that will
    #	(probably through a stacked widget) reveal additional (or a new set of)
    #	controls that will allow the user to specify which style items are set
    #	by this style.  (For example, a style could be created that only specifies
    #	a font family and size.  In this case other font items would be left alone
    #	when applying the style.)

    formatFlags = FormatFlags({ FormatFlag.FontFamily, \
                    FormatFlag.FontSize, \
                    FormatFlag.Bold, \
                    FormatFlag.Italic, \
                    FormatFlag.Underline,\
                    FormatFlag.Strikeout })

    if self.ui.fgColorToolButton.hasColor():
      formatFlags.addFlag(FormatFlag.FGColor)
      fgColor = self.ui.fgColorToolButton.getColor()
    else:
      formatFlags.addFlag(FormatFlag.FGColorNone)

    if self.ui.bgColorToolButton.hasColor():
      formatFlags.addFlag(FormatFlag.BGColor)
      bgColor = self.ui.bgColorToolButton.getColor()
    else:
      formatFlags.addFlag(FormatFlag.BGColorNone)

    theStyle = StyleDef()

    theStyle.strName = self.ui.styleNameEdit.text()
    theStyle.strDescription = self.ui.descriptionEdit.text()
    theStyle.formatFlags = formatFlags
    theStyle.strFontFamily = self.currentFont.family()
    theStyle.fontPointSize = self.currentFont.pointSize()
    theStyle.textColor = fgColor
    theStyle.backgroundColor = bgColor
    theStyle.bIsBold = self.currentFont.bold()
    theStyle.bIsItalic = self.currentFont.italic()
    theStyle.bIsUnderline = self.currentFont.underline()
    theStyle.bIsStrikeout = self.currentFont.strikeOut()

    return theStyle

  def populateDialog(self, styleDef: StyleDef):
    self.ui.styleNameEdit.setText(styleDef.strName)
    self.ui.descriptionEdit.setText(styleDef.strDescription)

    if styleDef.formatFlags != FormatFlag.NoFormat:
      if styleDef.formatFlags.hasFlag(FormatFlag.FontFamily):
        self.currentFont.setFamily(styleDef.strFontFamily)

      if styleDef.formatFlags.hasFlag(FormatFlag.FontSize):
        self.currentFont.setPointSize(styleDef.fontPointSize)

      if styleDef.formatFlags.hasFlag(FormatFlag.Bold):
        self.currentFont.setBold(styleDef.bIsBold)

      if styleDef.formatFlags.hasFlag(FormatFlag.Italic):
        self.currentFont.setItalic(styleDef.bIsItalic)

      if styleDef.formatFlags.hasFlag(FormatFlag.Underline):
        self.currentFont.setUnderline(styleDef.bIsUnderline)

      if styleDef.formatFlags.hasFlag(FormatFlag.Strikeout):
        self.currentFont.setStrikeOut(styleDef.bIsStrikeout)

      if styleDef.formatFlags.hasFlag(FormatFlag.FGColorNone):
        self.ui.fgColorToolButton.setNoColor()

      if styleDef.formatFlags.hasFlag(FormatFlag.FGColor):
        self.ui.fgColorToolButton.setColor(styleDef.textColor)

      if styleDef.formatFlags.hasFlag(FormatFlag.BGColorNone):
        self.ui.bgColorToolButton.setNoColor()

      if styleDef.formatFlags.hasFlag(FormatFlag.BGColor):
        self.ui.bgColorToolButton.setColor(styleDef.backgroundColor)

  @QtCore.Slot()
  def on_fontButton_clicked(self):
    okClicked, font = QtWidgets.QFontDialog.getFont(self.currentFont, self, 'Select Font')

    if okClicked:
      self.currentFont = font

      self.updateFontLabel()
      self.updateResultLabel()

  def onOrOffToString(self, styleItem: str, isOn: bool) -> str:
    return  styleItem if isOn else f'no {styleItem}'

  def updateFontLabel(self):
    styleItemList: list[str] = []

    styleItemList.append(self.currentFont.family())
    styleItemList.append(f'{self.currentFont.pointSize()} pt.')

    if self.currentFont.bold():
      styleItemList.append('bold')

    if self.currentFont.italic():
      styleItemList.append('italic')

    if self.currentFont.underline():
      styleItemList.append('underline')

    if self.currentFont.strikeOut():
      styleItemList.append('strikeout')

    styleDescription = ', '.join(styleItemList)

    self.ui.fontLabel.setText(styleDescription)

  def updateResultLabel(self):
    styleElementList: list[str] = []
    fontStr = ''

    if self.currentFont.bold():
      fontStr += ' bold'

    if self.currentFont.italic():
      fontStr += ' italic'

    if self.currentFont.underline():
      fontStr += ' underline'

    if self.currentFont.strikeOut():
      fontStr += ' strikeout'

    if self.ui.bgColorToolButton.hasColor():
      styleElementList.append(f'background-color: {self.ui.bgColorToolButton.getColor().name()}')

    if self.ui.fgColorToolButton.hasColor():
      styleElementList.append(f'color: {self.ui.fgColorToolButton.getColor().name()}')

    styleElementList.append(f'font {fontStr} "{self.currentFont.family()}"')
    styleElementList.append(f'font-size: {self.currentFont.pointSize()}px')

    styleSheetStr = '; '.join(styleElementList)
    styleSheetStr += ';'

    self.ui.sampleLabel.setStyleSheet(styleSheetStr)
    self.ui.sampleLabel.setText('Style looks like this')

  def onColorChanged(self):
    self.updateResultLabel()

  def updateOkButton(self):
    self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setEnabled(len(self.ui.styleNameEdit.text()) > 0)
