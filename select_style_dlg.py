from PyQt5 import uic, QtCore, QtGui, QtWidgets
from styleDef import StyleDef
from style_dlg import StyleDlg

from style_manager import StyleManager, kUserStyleStartIndex

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
      styleDefOrNone = self.styleManager.getStyle(styleId)
      if styleDefOrNone is not None:
        self.addStyle(styleDefOrNone.strName, styleId)

  def addStyle(self, styleName: str, styleId: int) -> None:
    item = QtWidgets.QListWidgetItem(styleName)
    item.setData(QtCore.Qt.ItemDataRole.UserRole, styleId)
    self.styleList.addItem(item)

  def getStyleIdForRow(self, row: int) -> int:
    item = self.styleList.item(row)
    itemVar = item.data(QtCore.Qt.ItemDataRole.UserRole)

    return int(itemVar)

  def getSelectedStyle(self) -> int | None:
    curRow = self.styleList.currentRow()
    if curRow > -1:
      return self.getStyleIdForRow(curRow)
    else:
      return None


  # ************* SLOTS *************

  @QtCore.pyqtSlot(int)
  def on_styleList_currentRowChanged(self, currentRow) -> None:
    styleDef = self.styleManager.getStyle(self.getStyleIdForRow(currentRow))

    if styleDef is not None:
      self.descriptionEdit.setText(styleDef.strDescription)

      # Disable Edit and Delete buttons for the first two (built-in) styles
      self.editButton.setEnabled(currentRow >= kUserStyleStartIndex)
      self.deleteButton.setEnabled(currentRow >= kUserStyleStartIndex)

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
    curRow = self.styleList.currentRow()

    if curRow != -1:
      styleId = self.getStyleIdForRow(curRow)

      response = QtWidgets.QMessageBox.question(self, \
                                                'Delete Style',\
                                                f'Delete style {self.getStyleNameForRow(curRow)}')

      if response == QtWidgets.QMessageBox.Yes:
        # Delete the style
        self.styleManager.deleteStyle(styleId)
        self.styleList.takeItem(curRow)

  @QtCore.pyqtSlot()
  def on_editButton_clicked(self) -> None:
    curRow = self.styleList.currentRow()

    if curRow != -1:
      styleId = self.getStyleIdForRow(curRow)
      styleDef = self.styleManager.getStyle(styleId)

      if styleDef is not None:
        dlg = StyleDlg(self, styleDef)

        if dlg.exec() == QtWidgets.QDialog.Accepted:
          styleDef = dlg.getStyle()

          self.styleManager.setStyle(styleDef, styleId)
