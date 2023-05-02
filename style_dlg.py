from PyQt5 import uic, QtCore, QtGui, QtWidgets

from styleDef import FormatFlag, FormatFlags, StyleDef

class StyleDlg(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget, styleDef: StyleDef) -> None:
    super(StyleDlg, self).__init__(parent)
    uic.loadUi('style_dlg.ui', self)

    self.styleDef = styleDef
    self.currentFont = QtGui.QFont()

    self.populateDialog(styleDef)
    self.updateFontLabel()
    self.updateResultLabel()
    self.updateOkButton()

    self.styleNameEdit.textChanged.connect(self.updateOkButton)
    self.bgColorToolButton.colorChangedSignal.connect(self.onColorChanged)
    self.fgColorToolButton.colorChangedSignal.connect(self.onColorChanged)
    self.bgColorToolButton.noColorSignal.connect(self.onColorChanged)
    self.fgColorToolButton.noColorSignal.connect(self.onColorChanged)

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

    if self.fgColorToolButton.hasColor():
      formatFlags.addFlag(FormatFlag.FGColor)
      fgColor = self.fgColorToolButton.getColor()
    else:
      formatFlags.addFlag(FormatFlag.FGColorNone)

    if self.bgColorToolButton.hasColor():
      formatFlags.addFlag(FormatFlag.BGColor)
      bgColor = self.bgColorToolButton.getColor()
    else:
      formatFlags.addFlag(FormatFlag.BGColorNone)

    theStyle = StyleDef()

    theStyle.strName = self.styleNameEdit.text()
    theStyle.strDescription = self.descriptionEdit.text()
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
    self.styleNameEdit.setText(styleDef.strName)
    self.descriptionEdit.setText(styleDef.strDescription)

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
        self.fgColorToolButton.setNoColor()

      if styleDef.formatFlags.hasFlag(FormatFlag.FGColor):
        self.fgColorToolButton.setColor(styleDef.textColor)

      if styleDef.formatFlags.hasFlag(FormatFlag.BGColorNone):
        self.bgColorToolButton.setNoColor()

      if styleDef.formatFlags.hasFlag(FormatFlag.BGColor):
        self.bgColorToolButton.setColor(styleDef.backgroundColor)

  @QtCore.pyqtSlot()
  def on_fontButton_clicked(self):
    font, okClicked = QtWidgets.QFontDialog.getFont(self.currentFont, self, 'Select Font')

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

    self.fontLabel.setText(styleDescription)

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

    if self.bgColorToolButton.hasColor():
      styleElementList.append(f'background-color: {self.bgColorToolButton.getColor().name()}')

    if self.fgColorToolButton.hasColor():
      styleElementList.append(f'color: {self.fgColorToolButton.getColor().name()}')

    styleElementList.append(f'font {fontStr} "{self.currentFont.family()}"')
    styleElementList.append(f'font-size: {self.currentFont.pointSize()}px')

    styleSheetStr = '; '.join(styleElementList)
    styleSheetStr += ';'

    self.sampleLabel.setStyleSheet(styleSheetStr)
    self.sampleLabel.setText('Style looks like this')

  def onColorChanged(self):
    self.updateResultLabel()

  def updateOkButton(self):
    self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setEnabled(len(self.styleNameEdit.text()) > 0)
