from PyQt5 import uic, QtCore, QtGui, QtWidgets

class CColorButton(QtWidgets.QToolButton):
  # Emitted when the user changes to "No Color"
  noColorSignal = QtCore.pyqtSignal()

  # Emitted when the color has changed
  colorChangedSignal = QtCore.pyqtSignal(QtGui.QColor)

  def __init__(self, parent):
    super(CColorButton, self).__init__(parent)
    self.m_hasColor = False
    self.m_color = QtGui.QColor(128, 128, 128)

    self.m_noColorAction = QtWidgets.QAction()
    self.m_noColorAction.setText('No Color')

    self.m_menu = QtWidgets.QMenu()
    self.m_menu.clear()
    self.m_menu.addAction(self.m_noColorAction)

    self.setMenu(self.m_menu)

    self.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)

    self.clicked.connect(self.showColorDialog)
    self.m_noColorAction.triggered.connect(self.onNoColorActionTriggered)


  def getColor(self) -> QtGui.QColor:
    return self.m_color

  def setColor(self, color):
    self.m_color = color
    self.m_hasColor = True
    self.update()

  def setNoColor(self):
    self.m_hasColor = False
    self.update()

  def hasColor(self):
    return self.m_hasColor

  def paintEvent(self, event):
    super(CColorButton, self).paintEvent(event)

    painter = QtGui.QPainter(self)
    colorRect = QtCore.QRect(6, 15, 10, 4)

    if self.m_hasColor:
      painter.fillRect(colorRect, self.m_color)
    else:
      # Paint an outline
      painter.setPen(QtGui.QColor("black"))
      colorRect.setBottom(colorRect.bottom() - 1)
      colorRect.setRight(colorRect.right() - 1)
      painter.drawRect(colorRect)

  def showColorDialog(self):
    color = QtWidgets.QColorDialog.getColor()

    if color.isValid:
      self.setColor(color)
      self.colorChangedSignal.emit(color)

  def onNoColorActionTriggered(self):
    self.m_hasColor = False
    self.update()

    self.noColorSignal.emit()