from PySide6 import QtCore, QtGui, QtWidgets
from ui_select_style_dlg import Ui_SelectStyleDlg
from styleDef import StyleDef
from style_dlg import StyleDlg

from style_manager import StyleManager, kUserStyleStartIndex

class SelectStyleDialog(QtWidgets.QDialog):
  def __init__(self, parent, styleManager: StyleManager):
    super(SelectStyleDialog, self).__init__(parent)

    self.ui = Ui_SelectStyleDlg()
    self.ui.setupUi(self)

    self.styleManager = styleManager
    self.loadStyles()

    self.ui.styleList.setCurrentRow(0)

  def loadStyles(self):
    styleIds = self.styleManager.getStyleIds()

    for styleId in styleIds:
      styleDefOrNone = self.styleManager.getStyle(styleId)
      if styleDefOrNone is not None:
        self.addStyle(styleDefOrNone.strName, styleId)

  def addStyle(self, styleName: str, styleId: int) -> None:
    item = QtWidgets.QListWidgetItem(styleName)
    item.setData(QtCore.Qt.ItemDataRole.UserRole, styleId)
    self.ui.styleList.addItem(item)

  def getStyleIdForRow(self, row: int) -> int:
    item = self.ui.styleList.item(row)
    itemVar = item.data(QtCore.Qt.ItemDataRole.UserRole)

    return int(itemVar)

  def getSelectedStyle(self) -> int | None:
    curRow = self.ui.styleList.currentRow()
    if curRow > -1:
      return self.getStyleIdForRow(curRow)
    else:
      return None


  # ************* SLOTS *************

  @QtCore.Slot(int)
  def on_styleList_currentRowChanged(self, currentRow) -> None:
    styleDef = self.styleManager.getStyle(self.getStyleIdForRow(currentRow))

    if styleDef is not None:
      self.ui.descriptionEdit.setText(styleDef.strDescription)

      # Disable Edit and Delete buttons for the first two (built-in) styles
      self.ui.editButton.setEnabled(currentRow >= kUserStyleStartIndex)
      self.ui.deleteButton.setEnabled(currentRow >= kUserStyleStartIndex)

  @QtCore.Slot()
  def on_newButton_clicked(self) -> None:
    styleDef = StyleDef()
    styleDef.setAllFormatFlags()
    styleDef.strFontFamily = QtGui.QGuiApplication.font().family()

    dlg = StyleDlg(self, styleDef)

    if dlg.exec() == QtWidgets.QDialog.Accepted:
      styleDef = dlg.getStyle()
      styleId = self.styleManager.addStyle(styleDef)

      self.addStyle(styleDef.strName, styleId)

  @QtCore.Slot()
  def on_deleteButton_clicked(self) -> None:
    curRow = self.ui.styleList.currentRow()

    if curRow != -1:
      styleId = self.getStyleIdForRow(curRow)

      response = QtWidgets.QMessageBox.question(self, \
                                                'Delete Style',\
                                                f'Delete style {self.getStyleNameForRow(curRow)}')

      if response == QtWidgets.QMessageBox.StandardButton.Yes:
        # Delete the style
        self.styleManager.deleteStyle(styleId)
        self.styleList.takeItem(curRow)

  @QtCore.Slot()
  def on_editButton_clicked(self) -> None:
    curRow = self.ui.styleList.currentRow()

    if curRow != -1:
      styleId = self.getStyleIdForRow(curRow)
      styleDef = self.styleManager.getStyle(styleId)

      if styleDef is not None:
        dlg = StyleDlg(self, styleDef)

        if dlg.exec() == QtWidgets.QDialog.Accepted:
          styleDef = dlg.getStyle()

          self.styleManager.setStyle(styleDef, styleId)
