from PyQt5 import uic, QtCore, QtGui, QtWidgets

class RichTextEditWidget(QtWidgets.QWidget):
  def __init__(self, parent):
    super(RichTextEditWidget, self).__init__(parent)
    uic.loadUi('RichTextEdit.ui', self)

    # Load icons explicityly, as they don't want to load automatically
    self.leftAlignButton.setIcon(QtGui.QIcon('Resources/Left.png'))
    self.centerAlignButton.setIcon(QtGui.QIcon('Resources/Center.png'))
    self.rightAlignButton.setIcon(QtGui.QIcon('Resources/Right.png'))
    self.boldButton.setIcon(QtGui.QIcon('Resources/Bold.png'))
    self.italicButton.setIcon(QtGui.QIcon('Resources/Italic.png'))
    self.underlineButton.setIcon(QtGui.QIcon('Resources/Underline.png'))
    self.bulletTableInsertButton.setIcon(QtGui.QIcon('Resources/Bullet Table.png'))
    self.numberTableInsertButton.setIcon(QtGui.QIcon('Resources/Number Table.png'))
    self.textColorButton.setIcon(QtGui.QIcon('Resources/Text Foreground.png'))
    self.textBackgroundButton.setIcon(QtGui.QIcon('Resources/Text Background.png'))

    self.populatePointSizesCombo()
    self.textColorButton.setColor(QtGui.QColor('Black'))

    # Disable style button at first.  It will be enabled whenever there is a selection.
    self.styleButton.setEnabled(False)

    self.styleMenu = QtWidgets.QMenu()

    self.initStyleButton()

    # Connect signals
    self.textColorButton.colorChangedSignal.connect(self.onTextColorChanged)
    self.textColorButton.noColorSignal.connect(self.onTextColorNoColor)
    self.textBackgroundButton.colorChangedSignal.connect(self.onTextBackgroundChanged)
    self.textBackgroundButton.noColorSignal.connect(self.onBackgroundNoColor)
    self.textEdit.selectionChanged.connect(self.onSelectionChanged)
    self.styleButton.triggered.connect(self.onStyleButtonTriggered)

  def populatePointSizesCombo(self):
    fontDatabase = QtGui.QFontDatabase()
    curFontFamily = self.fontCombo.currentText()

    self.sizeCombo.clear()
    fontSizeList = fontDatabase.pointSizes(curFontFamily)
    for curFontSize in fontSizeList:
      fontSizeString = f'{curFontSize}'
      self.sizeCombo.addItem(fontSizeString)

  def initStyleButton(self):
    # TODO: Need to get the settings from the user's prefs file.  This will
    # probably be read at startup.

    # TODO: Should add a way for the user to import/export the style settings.
    self.styleMenu.clear()

    # Add some hard-coded styles for debugging, but eventually, all styles will come from the styles.xml file.
    # NEW! The action will have the style ID stored as its data item.  (In the C++ version, a signal mapper was used,
    #      but the Qt docs say that signal mapper is obsolete.)

    debugStyles = [ ('Style #1', 11),
                    ('Style Two', 23),
                    ('Style The Third', 88)
                  ]

    for styleTuple in debugStyles:
      styleName = styleTuple[0]
      styleId = styleTuple[1]

      action = self.styleMenu.addAction(styleName)
      action.setData(styleId)

    self.styleButton.setMenu(self.styleMenu)

  def clear(self):
    self.textEdit.clear()

  def newDocument(self, fontFamily, fontSize):
    self.textEdit.clear()
    self.setDocumentModified(False)

    # Set global font size
    self.setGlobalFont(fontFamily, fontSize)

  def setDocumentModified(self, modified):
    doc = self.textEdit.document()
    doc.setModified(modified)

  def isModified(self):
    doc = self.textEdit.document()
    return doc.isModified()

  def setGlobalFont(self, fontFamily, fontSize):
    selectionCursor = self.textEdit.textCursor()

    if fontSize > 3 or len(fontFamily) > 0:
      tempCharFormat = QtGui.QTextCharFormat()

      # Select entire document
      selectionCursor.select(QtGui.QTextCursor.Document)
      selectionFormat = selectionCursor.charFormat()

      fontSizeToUse = self.findClosestSize(fontSize)

      tempCharFormat.setFontPointSize(fontSizeToUse)
      tempCharFormat.setFontFamily(fontFamily)
      selectionCursor.mergeCharFormat(tempCharFormat)

      self.textEdit.setTextCursor(selectionCursor)

      tempFont = QtGui.QFont(fontFamily, fontSize)
      doc = self.textEdit.document()

      doc.setDefaultFont(tempFont)

      self.updateControls()

  def findClosestSize(self, fontSize):
    index = self.sizeCombo.findText(f'{fontSize}')
    maxFontSize = 0

    if index < 0:
      return fontSize

    for i in range(self.fontCombo.count()):
      fontSizeStr = self.sizeCombo.itemText(i)

      if len(fontSizeStr) > 0:
        curFontSize = int(fontSizeStr)
        maxFontSize = max(maxFontSize, curFontSize)

        if curFontSize > fontSize:
          return curFontSize

    # fontSize is larger than any font in the combo box.  In this
    # case, return the largest font in the combo box
    return maxFontSize

  def updateControls(self):
    selectionCursor = self.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()

    fontFamily = selectionFormat.fontFamily()
    index = self.fontCombo.findText(fontFamily)
    if index != -1:
      self.fontCombo.setCurrentIndex(index)

    fontSize = selectionFormat.fontPointSize()
    fontSizeStr = f'{fontSize}'
    index = self.sizeCombo.findText(fontSizeStr)
    if index != -1:
      self.sizeCombo.setCurrentIndex(index)

    self.boldButton.setChecked(selectionFormat.fontWeight() == QtGui.QFont.Bold)
    self.italicButton.setChecked(selectionFormat.fontItalic())
    self.underlineButton.setChecked(selectionFormat.fontUnderline())

    curBlockFormat = selectionCursor.blockFormat()
    alignmentVal = curBlockFormat.alignment()

    alignmentVal &= 0x0000000f    # Mask off other flags

    if alignmentVal == QtCore.Qt.AlignmentFlag.AlignLeft:
      self.leftAlignButton.setChecked(True)
    elif alignmentVal == QtCore.Qt.AlignmentFlag.AlignHCenter:
      self.centerAlignButton.setChecked(True)
    elif alignmentVal == QtCore.Qt.AlignmentFlag.AlignRight:
      self.rightAlignButton.setChecked(True)
    else:
      self.leftAlignButton.setChecked(True)

    textBrush = selectionFormat.foreground()
    if textBrush.isOpaque():
      self.textColorButton.setColor(textBrush.color())
    else:
      self.textColorButton.setNoColor()

    bgBrush = selectionFormat.background()
    if bgBrush.isOpaque():
      self.textBackgroundButton.setColor(bgBrush.color())
    else:
      self.textBackgroundButton.setNoColor()

  # Slots

  @QtCore.pyqtSlot(QtGui.QColor)
  def onTextColorChanged(self, color):
    selectionCursor = self.textEdit.textCursor()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setForeground(QtGui.QBrush(color))
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.textEdit.setTextCursor(selectionCursor)

  def onTextColorNoColor(self):
    selectionCursor = self.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()

    # NOTE: This approach will cause all text in the selection to take on
    # all characteristics of the selectionFormat.  It has the effect of
    # removing formatting changes within the block.  Unfortunately,
    # mergeCharFormat does not work when clearing a property.
    selectionFormat.clearForeground()
    selectionCursor.setCharFormat(selectionFormat)

    self.textEdit.setTextCursor(selectionCursor)

  @QtCore.pyqtSlot(QtGui.QColor)
  def onTextBackgroundChanged(self, color):
    selectionCursor = self.textEdit.textCursor()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setBackground(QtGui.QBrush(color))
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.textEdit.setTextCursor(selectionCursor)

  @QtCore.pyqtSlot()
  def onBackgroundNoColor(self):
    selectionCursor = self.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()

    # NOTE: This approach will cause all text in the selection to take on
    # all characteristics of the selectionFormat.  It has the effect of
    # removing formatting changes within the block.  Unfortunately,
    # mergeCharFormat does not work when clearing a property.
    selectionFormat.clearBackground()
    selectionCursor.setCharFormat(selectionFormat)

    self.textEdit.setTextCursor(selectionCursor)

  @QtCore.pyqtSlot()
  def onSelectionChanged(self):
    selectionCursor = self.textEdit.textCursor()
    self.styleButton.setEnabled(selectionCursor.hasSelection())

  @QtCore.pyqtSlot(QtWidgets.QAction)
  def onStyleButtonTriggered(self, action):
    """ A 'triggered' event happens when the user changes
        the current item in the style button. """
    styleId = action.data()
    print(f'Style button triggered.  Style: {styleId}')