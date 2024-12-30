from PySide6 import QtCore, QtGui, QtWidgets
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

class FormatFlags:
  def __init__(self, initialFlags: set[FormatFlag]) -> None:
    self.formatFlags: set[FormatFlag] = initialFlags

  def hasFlag(self, flagToTest: FormatFlag) -> bool:
    return flagToTest in self.formatFlags

  def addFlag(self, flagToAdd: FormatFlag):
    self.formatFlags.add(flagToAdd)

class StyleDef:
  def __init__(self) -> None:
    self.strName = ''
    self.strDescription = ''
    self.strFontFamily = 'Helvetica'
    self.fontPointSize = 10
    self.textColor = QtGui.QColor('black')
    self.backgroundColor = QtGui.QColor('white')
    self.bIsBold = False
    self.bIsItalic = False
    self.bIsUnderline = False
    self.bIsStrikeout = False

    self.formatFlags = FormatFlags({ FormatFlag.NoFormat }) 						# Don't set format

  def setAllFormatFlags(self):
    self.formatFlags = FormatFlags({ FormatFlag.FontFamily, \
                                    FormatFlag.FontSize, \
                                    FormatFlag.Bold, \
                                    FormatFlag.Italic, \
                                    FormatFlag.Underline, \
                                    FormatFlag.Strikeout, \
                                    FormatFlag.FGColorNone, \
                                    FormatFlag.BGColorNone })