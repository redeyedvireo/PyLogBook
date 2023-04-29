from PyQt5 import uic, QtCore, QtGui, QtWidgets
from styleDef import StyleDef
from style_dlg import StyleDlg

from style_manager import StyleManager

class SelectStyleDialog(QtWidgets.QDialog):
  def __init__(self, parent, styleManager: StyleManager):
    super(SelectStyleDialog, self).__init__(parent)
    uic.loadUi('select_style_dlg.ui', self)

    # Load icons explicityly, as they don't load automatically (PyQt bug?)
    self.newButton.setIcon(QtGui.QIcon('Resources/plus.png'))
    self.deleteButton.setIcon(QtGui.QIcon('Resources/minus.png'))
    self.editButton.setIcon(QtGui.QIcon('Resources/pencil.png'))

    self.styleManager = styleManager
    self.loadStyles()

    self.styleList.setCurrentRow(0)

  def loadStyles(self):
    styleIds = self.styleManager.getStyleIds()

    for styleId in styleIds:
      self.addStyle(self.styleManager.getStyle(styleId).strName, styleId)

  def addStyle(self, styleName: str, styleId: int) -> None:
    item = QtWidgets.QListWidgetItem(styleName)
    item.setData(QtCore.Qt.ItemDataRole.UserRole, styleId)
    self.styleList.addItem(item)


  # ************* SLOTS *************

  @QtCore.pyqtSlot(int)
  def on_styleList_currentRowChanged(self, currentRow) -> None:
    # TODO: Implement
    print('on_styleList_currentRowChanged')

  @QtCore.pyqtSlot()
  def on_newButton_clicked(self) -> None:
    styleDef = StyleDef()
    styleDef.setAllFormatFlags()
    styleDef.strFontFamily = QtGui.QGuiApplication.font().family()

    dlg = StyleDlg(self, styleDef)

    if dlg.exec() == QtWidgets.QDialog.Accepted:
      styleDef = dlg.getStyle()
      styleId = self.styleManager.addStyle(styleDef)

      self.addStyle(styleDef.strName, styleId)

  @QtCore.pyqtSlot()
  def on_deleteButton_clicked(self) -> None:
    # TODO: Implement
    print('on_deleteButton_clicked')

  @QtCore.pyqtSlot()
  def on_editButton_clicked(self) -> None:
    # TODO: Implement
    print('on_editButton_clicked')
