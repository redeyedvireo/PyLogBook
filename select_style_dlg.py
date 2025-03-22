from PySide6 import QtCore, QtGui, QtWidgets
from ui_select_style_dlg import Ui_SelectStyleDlg
from styleDef import StyleDef
from style_dlg import StyleDlg

from style_manager import StyleManager, kUserStyleStartIndex

class SelectStyleDialog(QtWidgets.QDialog):
  def __init__(self, parent, styleManager: StyleManager, defaultFontFamily: str, defaultFontSize: int):
    super(SelectStyleDialog, self).__init__(parent)

    self.ui = Ui_SelectStyleDlg()
    self.ui.setupUi(self)

    self.defaultFontFamily = defaultFontFamily
    self.defaultFontSize = defaultFontSize
    self.styleManager = styleManager
    self.loadStyles()

    self.ui.styleList.setCurrentRow(0)

  def loadStyles(self):
    styleIds = self.styleManager.getStyleIds()

    for styleId in styleIds:
      styleDefOrNone = self.styleManager.getStyle(styleId)
      if styleDefOrNone is not None:
        self.addStyle(styleDefOrNone.strName, styleId)

  def addStyle(self, styleName: str, styleId: int):
    """Adds a style to the list.  Returns the row number of the added style.

    Args:
        styleName (str): Name of style
        styleId (int): Style ID

    Returns:
        int: Row number of the added style
    """
    item = QtWidgets.QListWidgetItem(styleName)
    item.setData(QtCore.Qt.ItemDataRole.UserRole, styleId)
    self.ui.styleList.addItem(item)
    numRows = self.ui.styleList.count()
    return numRows - 1

  def getStyleIdForRow(self, row: int) -> int:
    item = self.ui.styleList.item(row)
    itemVar = item.data(QtCore.Qt.ItemDataRole.UserRole)

    return int(itemVar)

  def getStyleNameForRow(self, row: int) -> str:
    item = self.ui.styleList.item(row)
    return item.text()

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
    styleDef.strFontFamily = self.defaultFontFamily
    styleDef.fontPointSize = self.defaultFontSize

    dlg = StyleDlg(self, styleDef)

    if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
      styleDef = dlg.getStyle()
      styleId = self.styleManager.addStyle(styleDef)

      styleRowNum = self.addStyle(styleDef.strName, styleId)
      self.ui.styleList.setCurrentRow(styleRowNum)

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
        self.ui.styleList.takeItem(curRow)

  @QtCore.Slot()
  def on_editButton_clicked(self) -> None:
    curRow = self.ui.styleList.currentRow()

    if curRow != -1:
      styleId = self.getStyleIdForRow(curRow)
      styleDef = self.styleManager.getStyle(styleId)

      if styleDef is not None:
        dlg = StyleDlg(self, styleDef)

        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
          styleDef = dlg.getStyle()

          self.styleManager.setStyle(styleDef, styleId)
