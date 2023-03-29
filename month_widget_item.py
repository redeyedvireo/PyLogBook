from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

class CMonthWidgetItem(QtWidgets.QTreeWidgetItem):
  def __init__(self, parent):
    super(CMonthWidgetItem, self).__init__(parent)

  def __lt__(self, other: QtWidgets.QTreeWidgetItem) -> bool:
    thisMonth = self.data(0, QtCore.Qt.ItemDataRole.UserRole)
    otherMonth = other.data(0, QtCore.Qt.ItemDataRole.UserRole)

    return thisMonth < otherMonth
