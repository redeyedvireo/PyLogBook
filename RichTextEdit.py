from PySide6 import QtCore, QtGui, QtWidgets
import datetime

from ui_RichTextEdit import Ui_RichTextEditWidget

from select_style_dlg import SelectStyleDialog
from style_manager import StyleManager
from utility import formatDateTime

class RichTextEditWidget(QtWidgets.QWidget):
  logTextChangedSignal = QtCore.Signal()

  def __init__(self, parent):
    super(RichTextEditWidget, self).__init__(parent)

    self.ui = Ui_RichTextEditWidget()
    self.ui.setupUi(self)

    self.styleManager = StyleManager()

    self.populatePointSizesCombo()
    self.ui.textColorButton.setColor(QtGui.QColor('Black'))

    # Disable style button at first.  It will be enabled whenever there is a selection.
    self.ui.styleButton.setEnabled(False)

    self.styleMenu = QtWidgets.QMenu()

    self.initStyleButton()

    # Connect signals
    self.ui.textColorButton.colorChangedSignal.connect(self.onTextColorChanged)
    self.ui.textColorButton.noColorSignal.connect(self.onTextColorNoColor)
    self.ui.textBackgroundButton.colorChangedSignal.connect(self.onTextBackgroundChanged)
    self.ui.textBackgroundButton.noColorSignal.connect(self.onBackgroundNoColor)
    self.ui.textEdit.selectionChanged.connect(self.onSelectionChanged)
    self.ui.textEdit.textChanged.connect(self.onTextChanged)
    self.ui.textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)
    self.ui.styleButton.triggered.connect(self.onStyleButtonTriggered)
    self.ui.boldButton.clicked.connect(self.onBoldButtonClicked)
    self.ui.italicButton.clicked.connect(self.onItalicButtonClicked)
    self.ui.underlineButton.clicked.connect(self.onUnderlineButtonClicked)
    self.ui.leftAlignButton.clicked.connect(self.onLeftAlignButtonClicked)
    self.ui.centerAlignButton.clicked.connect(self.onCenterAlignButtonClicked)
    self.ui.rightAlignButton.clicked.connect(self.onRightAlignButtonClicked)
    self.ui.bulletTableInsertButton.clicked.connect(self.onBulletTableInsertButtonClicked)
    self.ui.numberTableInsertButton.clicked.connect(self.onNumberTableInsertButtonClicked)

  def populatePointSizesCombo(self):
    curFontFamily = self.ui.fontCombo.currentText()

    self.ui.sizeCombo.clear()
    fontSizeList = QtGui.QFontDatabase.pointSizes(curFontFamily)
    for curFontSize in fontSizeList:
      fontSizeString = f'{curFontSize}'
      self.ui.sizeCombo.addItem(fontSizeString)

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

    self.ui.styleButton.setMenu(self.styleMenu)

  def clear(self):
    self.ui.textEdit.clear()

  def newDocument(self, fontFamily, fontSize):
    self.clear()
    self.setDocumentModified(False)

    # Set global font size
    self.setGlobalFont(fontFamily, fontSize)

  def toHtml(self):
    return self.ui.textEdit.document().toHtml()

  def isModified(self):
    doc = self.ui.textEdit.document()
    return doc.isModified()

  def setDocumentModified(self, modified):
    doc = self.ui.textEdit.document()
    doc.setModified(modified)

  def setDocumentText(self, content: str) -> None:
    self.ui.textEdit.setHtml(content)

  def setGlobalFont(self, fontFamily, fontSize):
    selectionCursor = self.ui.textEdit.textCursor()

    if fontSize > 3 or len(fontFamily) > 0:
      tempCharFormat = QtGui.QTextCharFormat()

      # Select entire document
      selectionCursor.select(QtGui.QTextCursor.SelectionType.Document)
      selectionFormat = selectionCursor.charFormat()

      fontSizeToUse = self.findClosestSize(fontSize)

      tempCharFormat.setFontPointSize(fontSizeToUse)
      tempCharFormat.setFontFamily(fontFamily)
      selectionCursor.mergeCharFormat(tempCharFormat)

      self.ui.textEdit.setTextCursor(selectionCursor)

      tempFont = QtGui.QFont(fontFamily, fontSize)
      doc = self.ui.textEdit.document()

      doc.setDefaultFont(tempFont)

      self.updateControls()

  def findClosestSize(self, fontSize):
    index = self.ui.sizeCombo.findText(f'{fontSize}')
    maxFontSize = 0

    if index < 0:
      return fontSize

    for i in range(self.ui.fontCombo.count()):
      fontSizeStr = self.ui.sizeCombo.itemText(i)

      if len(fontSizeStr) > 0:
        curFontSize = int(fontSizeStr)
        maxFontSize = max(maxFontSize, curFontSize)

        if curFontSize > fontSize:
          return curFontSize

    # fontSize is larger than any font in the combo box.  In this
    # case, return the largest font in the combo box
    return maxFontSize

  def updateControls(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    # fontFamily = selectionFormat.fontFamily()
    fontFamilies = selectionFormat.fontFamilies()

    if fontFamilies is not None and len(fontFamilies) > 0:
      index = self.ui.fontCombo.findText(fontFamilies[0])
      if index != -1:
        self.ui.fontCombo.setCurrentIndex(index)

    fontSize = selectionFormat.fontPointSize()
    fontSizeStr = f'{int(fontSize)}'
    index = self.ui.sizeCombo.findText(fontSizeStr)
    if index != -1:
      self.ui.sizeCombo.setCurrentIndex(index)

    self.ui.boldButton.setChecked(selectionFormat.fontWeight() == QtGui.QFont.Weight.Bold)
    self.ui.italicButton.setChecked(selectionFormat.fontItalic())
    self.ui.underlineButton.setChecked(selectionFormat.fontUnderline())

    curBlockFormat = selectionCursor.blockFormat()
    alignmentVal = curBlockFormat.alignment()

    alignmentVal &= 0x0000000f    # Mask off other flags

    if alignmentVal == QtCore.Qt.AlignmentFlag.AlignLeft:
      self.ui.leftAlignButton.setChecked(True)
    elif alignmentVal == QtCore.Qt.AlignmentFlag.AlignHCenter:
      self.ui.centerAlignButton.setChecked(True)
    elif alignmentVal == QtCore.Qt.AlignmentFlag.AlignRight:
      self.ui.rightAlignButton.setChecked(True)
    else:
      self.ui.leftAlignButton.setChecked(True)

    textBrush = selectionFormat.foreground()
    if textBrush.isOpaque():
      self.ui.textColorButton.setColor(textBrush.color())
    else:
      self.ui.textColorButton.setNoColor()

    bgBrush = selectionFormat.background()
    if bgBrush.isOpaque():
      self.ui.textBackgroundButton.setColor(bgBrush.color())
    else:
      self.ui.textBackgroundButton.setNoColor()

  def getCursorAndSelectionFormat(self) -> tuple[QtGui.QTextCursor, QtGui.QTextCharFormat]:
    selectionCursor = self.ui.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()
    return (selectionCursor, selectionFormat)

  def getCursorAndBlockFormat(self) -> tuple[QtGui.QTextCursor, QtGui.QTextBlockFormat]:
    selectionCursor = self.ui.textEdit.textCursor()
    blockFormat = selectionCursor.blockFormat()
    return (selectionCursor, blockFormat)

  def addAddendum(self):
    textCursor = self.ui.textEdit.textCursor()

    textCursor.movePosition(QtGui.QTextCursor.MoveOperation.End, QtGui.QTextCursor.MoveMode.MoveAnchor)

    self.ui.textEdit.insertHtml(f'<br><hr />Addendum {formatDateTime(datetime.datetime.now())}<br>')


  # Slots

  @QtCore.Slot()
  def onTextChanged(self):
    self.logTextChangedSignal.emit()

  @QtCore.Slot()
  def onCursorPositionChanged(self):
    self.updateControls()

  @QtCore.Slot(QtGui.QColor)
  def onTextColorChanged(self, color):
    selectionCursor = self.ui.textEdit.textCursor()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setForeground(QtGui.QBrush(color))
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  def onTextColorNoColor(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    # NOTE: This approach will cause all text in the selection to take on
    # all characteristics of the selectionFormat.  It has the effect of
    # removing formatting changes within the block.  Unfortunately,
    # mergeCharFormat does not work when clearing a property.
    selectionFormat.clearForeground()
    selectionCursor.setCharFormat(selectionFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot(QtGui.QColor)
  def onTextBackgroundChanged(self, color):
    selectionCursor = self.ui.textEdit.textCursor()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setBackground(QtGui.QBrush(color))
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onBackgroundNoColor(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    # NOTE: This approach will cause all text in the selection to take on
    # all characteristics of the selectionFormat.  It has the effect of
    # removing formatting changes within the block.  Unfortunately,
    # mergeCharFormat does not work when clearing a property.
    selectionFormat.clearBackground()
    selectionCursor.setCharFormat(selectionFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onSelectionChanged(self):
    selectionCursor = self.ui.textEdit.textCursor()
    self.ui.styleButton.setEnabled(selectionCursor.hasSelection())

  @QtCore.Slot(QtGui.QAction)
  def onStyleButtonTriggered(self, action):
    """ A 'triggered' event happens when the user changes
        the current item in the style button. """
    styleId = action.data()
    print(f'Style button triggered.  Style: {styleId}')

  @QtCore.Slot()
  def onBoldButtonClicked(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    tempCharFormat = QtGui.QTextCharFormat()
    if selectionFormat.fontWeight() != QtGui.QFont.Weight.Bold:
      tempCharFormat.setFontWeight(QtGui.QFont.Weight.Bold)
    else:
      tempCharFormat.setFontWeight(QtGui.QFont.Weight.Normal)

    selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onItalicButtonClicked(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setFontItalic(not selectionFormat.fontItalic())
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onUnderlineButtonClicked(self):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setFontUnderline(not selectionFormat.fontUnderline())
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onLeftAlignButtonClicked(self):
    selectionCursor, blockFormat = self.getCursorAndBlockFormat()

    blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    selectionCursor.setBlockFormat(blockFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onCenterAlignButtonClicked(self):
    selectionCursor, blockFormat = self.getCursorAndBlockFormat()

    blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    selectionCursor.setBlockFormat(blockFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onRightAlignButtonClicked(self):
    selectionCursor, blockFormat = self.getCursorAndBlockFormat()

    blockFormat.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    selectionCursor.setBlockFormat(blockFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def onBulletTableInsertButtonClicked(self):
    selectionCursor = self.ui.textEdit.textCursor()

    newListFormat = QtGui.QTextListFormat()
    newListFormat.setIndent(1)
    newListFormat.setStyle(QtGui.QTextListFormat.Style.ListDisc)

    selectionCursor.createList(newListFormat)

  @QtCore.Slot()
  def onNumberTableInsertButtonClicked(self):
    selectionCursor = self.ui.textEdit.textCursor()

    newListFormat = QtGui.QTextListFormat()
    newListFormat.setIndent(1)
    newListFormat.setStyle(QtGui.QTextListFormat.Style.ListDecimal)

    selectionCursor.createList(newListFormat)

  @QtCore.Slot(int)
  def on_fontCombo_activated(self, index):
    self.populatePointSizesCombo()

    # selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()
    selectionCursor = self.ui.textEdit.textCursor()
    selectionFormat = selectionCursor.charFormat()

    fontFamily = self.ui.fontCombo.currentText()
    selectionFormat.setFontFamily(fontFamily)
    selectionCursor.setCharFormat(selectionFormat)

    # tempCharFormat = QtGui.QTextCharFormat()
    # tempCharFormat.setFontFamily(text)
    # selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot(int)
  def on_sizeCombo_activated(self, index):
    selectionCursor, selectionFormat = self.getCursorAndSelectionFormat()

    text = self.ui.sizeCombo.itemText(index)
    newFontSize = int(text)

    tempCharFormat = QtGui.QTextCharFormat()
    tempCharFormat.setFontPointSize(newFontSize)
    selectionCursor.mergeCharFormat(tempCharFormat)

    self.ui.textEdit.setTextCursor(selectionCursor)

  @QtCore.Slot()
  def on_styleButton_clicked(self):
    print('Style button clicked')
    styleDlg = SelectStyleDialog(self, self.styleManager)
    if styleDlg.exec() == QtWidgets.QDialog.Accepted:
      styleId = styleDlg.getSelectedStyle()

      if styleId is not None:
        self.styleManager.applyStyle(self.ui.textEdit, styleId)
        self.initStyleButton()
