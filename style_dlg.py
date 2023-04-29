from PyQt5 import uic, QtCore, QtGui, QtWidgets

from styleDef import FormatFlag, StyleDef

class StyleDlg(QtWidgets.QDialog):
  def __init__(self, parent: QtWidgets.QWidget, styleDef: StyleDef) -> None:
    super(StyleDlg, self).__init__(parent)
    uic.loadUi('style_dlg.ui', self)

    self.styleDef = styleDef
    self.currentFont = QtGui.QFont()

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

    formatFlags = FormatFlag.FontFamily | \
                  FormatFlag.FontSize | \
                  FormatFlag.Bold | \
                  FormatFlag.Italic | \
                  FormatFlag.Underline | \
                  FormatFlag.Strikeout

    if self.fgColorToolButton.hasColor():
      formatFlags |= FormatFlag.FGColor
      fgColor = self.fgColorToolButton.getColor()
    else:
      formatFlags |= FormatFlag.FGColorNone

    if self.bgColorToolButton.hasColor():
      formatFlags |= FormatFlag.BGColor
      bgColor = self.bgColorToolButton.getColor()
    else:
      formatFlags |= FormatFlag.BGColorNone

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
