from PyQt5 import uic, QtCore, QtGui, QtWidgets
from enum import IntFlag

class FormatFlag(IntFlag):
  NoFormat = 0
  FontFamily = 1
  FontSize = 2
  FGColorNone = 4
  FGColor = 8
  BGColorNone = 16
  BGColor = 32
  Bold = 64
  Italic = 128
  Underline = 256
  Strikeout = 512

class StyleDef:
  def __init__(self) -> None:
    self.strName = ''
    self.strDescription = ''
    self.strFontFamily = 'Helvetica'
    self.fontPointSize = -1
    self.textColor = QtGui.QColor('black')
    self.backgroundColor = QtGui.QColor('white')
    self.bIsBold = False
    self.bIsItalic = False
    self.bIsUnderline = False
    self.bIsStrikeout = False

    self.formatFlags = FormatFlag.NoFormat						# Don't set format

  def setAllFormatFlags(self):
    self.formatFlags = FormatFlag.FontFamily | \
                        FormatFlag.FontSize | \
                        FormatFlag.Bold | \
                        FormatFlag.Italic | \
                        FormatFlag.Underline | \
                        FormatFlag.Strikeout | \
                        FormatFlag.FGColorNone | \
                        FormatFlag.BGColorNone