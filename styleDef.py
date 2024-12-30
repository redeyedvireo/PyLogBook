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


	 #	The formatFlags indicate which elments are specified by the style.
	 #	For example, if the Bold flag is set, that indicates that this
	 #	style dictates how bold is to be set (either on or off).  The
	 #	actual setting of whether bold is on or off is determined by
	 #	the bIsBold member.
class FormatFlags:
  def __init__(self, initialFlags: set[FormatFlag]) -> None:
    self.formatFlags: set[FormatFlag] = initialFlags

  def hasFlag(self, flagToTest: FormatFlag) -> bool:
    return flagToTest in self.formatFlags

  def addFlag(self, flagToAdd: FormatFlag):
    self.formatFlags.add(flagToAdd)

  def removeFlag(self, flagToRemove: FormatFlag):
    if self.hasFlag(flagToRemove):
      self.formatFlags.remove(flagToRemove)

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

  # For the properties, a property will return None if the corresponding format flag for that property does not exist.
  # This means that the property is not affected by this style.
  # If the format flag for that property DOES exist, it means that this style is affected by the property, and in this
  # case the value of the property will be returned.
  # When setting a property, if the value is set to None, the corresponding format flag will be removed; in this case,
  # this property no longer is affected by this style.
  #
  # Addendum: It occurred to me that instead of this complicated system, all that really needs to be done is to store
  # None in any property that is not affected by the style.

  @property
  def fontFamily(self) -> str | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.FontFamily) else self.strFontFamily

  @fontFamily.setter
  def fontFamily(self, value: str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.FontFamily)
      self.strFontFamily = ''
    else:
      self.strFontFamily = value
      self.formatFlags.addFlag(FormatFlag.FontFamily)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)

  @property
  def pointSize(self) -> int | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.FontSize) else self.fontPointSize

  @pointSize.setter
  def pointSize(self, value: str | int | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.FontSize)
      self.fontPointSize = 0
    else:
      self.formatFlags.addFlag(FormatFlag.FontSize)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.fontPointSize = int(value)

  @property
  def noForegroundColor(self) -> bool:
    return self.formatFlags.hasFlag(FormatFlag.FGColorNone)

  @noForegroundColor.setter
  def noForegroundColor(self, value: bool | str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.FGColorNone)
    elif type(value) is str:
      if value == 'yes':
        self.formatFlags.addFlag(FormatFlag.FGColorNone)
        self.formatFlags.removeFlag(FormatFlag.NoFormat)
      else:
        self.formatFlags.removeFlag(FormatFlag.FGColorNone)
    elif type(value) is bool:
      if value:
        self.formatFlags.addFlag(FormatFlag.FGColorNone)
        self.formatFlags.removeFlag(FormatFlag.NoFormat)
      else:
        self.formatFlags.removeFlag(FormatFlag.FGColorNone)
    else:
      # Unknown type - do nothing
      pass

  @property
  def fgColor(self) -> QtGui.QColor | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.FGColor) else self.textColor

  @fgColor.setter
  def fgColor(self, value: str | QtGui.QColor | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.FGColor)
    elif type(value) is QtGui.QColor:
      self.formatFlags.addFlag(FormatFlag.FGColor)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.textColor = value
    elif type(value) is str:
      self.formatFlags.addFlag(FormatFlag.FGColor)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.textColor.setNamedColor(value)
    else:
      # Unknown type - do nothing
      pass

  @property
  def noBackgroundColor(self) -> bool:
    return self.formatFlags.hasFlag(FormatFlag.BGColorNone)

  @noBackgroundColor.setter
  def noBackgroundColor(self, value: bool | str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.BGColorNone)
    elif type(value) is str:
      if value == 'yes':
        self.formatFlags.addFlag(FormatFlag.BGColorNone)
        self.formatFlags.removeFlag(FormatFlag.NoFormat)
      else:
        self.formatFlags.removeFlag(FormatFlag.BGColorNone)
    elif type(value) is bool:
      if value:
        self.formatFlags.addFlag(FormatFlag.BGColorNone)
        self.formatFlags.removeFlag(FormatFlag.NoFormat)
      else:
        self.formatFlags.removeFlag(FormatFlag.BGColorNone)
    else:
      # Unknown type - do nothing
      pass

  @property
  def bgColor(self) -> QtGui.QColor | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.BGColor) else self.backgroundColor

  @bgColor.setter
  def bgColor(self, value: str | QtGui.QColor | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.BGColor)
    elif type(value) is QtGui.QColor:
      self.formatFlags.addFlag(FormatFlag.BGColor)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.backgroundColor = value
    elif type(value) is str:
      self.formatFlags.addFlag(FormatFlag.BGColor)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.backgroundColor.setNamedColor(value)
    else:
      # Unknown type - do nothing
      pass

  @property
  def isBold(self) -> bool | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.Bold) else self.bIsBold

  @isBold.setter
  def isBold(self, value: bool | str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.Bold)
    elif type(value) is str:
      self.formatFlags.addFlag(FormatFlag.Bold)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsBold = (value == 'yes')
    elif type(value) is bool:
      self.formatFlags.addFlag(FormatFlag.Bold)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsBold = value
    else:
      # Unknown type - do nothing
      pass

  @property
  def isItalic(self) -> bool | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.Italic) else self.bIsItalic

  @isItalic.setter
  def isItalic(self, value: bool | str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.Italic)
    elif type(value) is str:
      self.formatFlags.addFlag(FormatFlag.Italic)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsItalic = (value == 'yes')
    elif type(value) is bool:
      self.formatFlags.addFlag(FormatFlag.Italic)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsItalic = value
    else:
      # Unknown type - do nothing
      pass

  @property
  def isUnderline(self) -> bool | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.Underline) else self.bIsUnderline

  @isUnderline.setter
  def isUnderline(self, value: bool | str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.Underline)
    elif type(value) is str:
      self.formatFlags.addFlag(FormatFlag.Underline)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsUnderline = (value == 'yes')
    elif type(value) is bool:
      self.formatFlags.addFlag(FormatFlag.Underline)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsUnderline = value
    else:
      # Unknown type - do nothing
      pass

  @property
  def isStrikeout(self) -> bool | None:
    return None if not self.formatFlags.hasFlag(FormatFlag.Strikeout) else self.bIsStrikeout

  @isStrikeout.setter
  def isStrikeout(self, value: bool | str | None):
    if value is None:
      self.formatFlags.removeFlag(FormatFlag.Strikeout)
    elif type(value) is str:
      self.formatFlags.addFlag(FormatFlag.Strikeout)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsStrikeout = (value == 'yes')
    elif type(value) is bool:
      self.formatFlags.addFlag(FormatFlag.Strikeout)
      self.formatFlags.removeFlag(FormatFlag.NoFormat)
      self.bIsStrikeout = value
    else:
      # Unknown type - do nothing
      pass
