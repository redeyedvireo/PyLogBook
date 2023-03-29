from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

from utility import dateFromFormattedString

class CDateWidgetItem(QtWidgets.QTreeWidgetItem):
  def __init__(self, parent):
    super(CDateWidgetItem, self).__init__(parent)

  def __lt__(self, other: QtWidgets.QTreeWidgetItem) -> bool:
    thisDate = self.data(0, QtCore.Qt.ItemDataRole.UserRole)
    otherDate = other.data(0, QtCore.Qt.ItemDataRole.UserRole)

    return thisDate < otherDate
