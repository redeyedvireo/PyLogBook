from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

from utility import dateFromFormattedString

class CDateWidgetItem(QtWidgets.QTreeWidgetItem):
  def __init__(self, parent):
    super(CDateWidgetItem, self).__init__(parent)

  def __lt__(self, other: QtWidgets.QTreeWidgetItem) -> bool:
    thisDateStr = self.text(0)
    otherDateStr = other.text(0)

    thisDate = dateFromFormattedString(thisDateStr)
    otherDate = dateFromFormattedString(otherDateStr)

    return thisDate < otherDate
