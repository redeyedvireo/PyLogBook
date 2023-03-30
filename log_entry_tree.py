from PyQt5 import uic, QtCore, QtGui, QtWidgets
import typing
import logging
import datetime
import calendar
from date_widget_item import CDateWidgetItem
from month_widget_item import CMonthWidgetItem

from utility import dateToJulianDay, formatDate, julianDayToDate

class CLogEntryTree(QtWidgets.QTreeWidget):
  logEntryClickedSignal = QtCore.pyqtSignal(datetime.date)

  def __init__(self, parent):
    super(CLogEntryTree, self).__init__(parent)
    self.clear()
    self.logDates: list[datetime.date] = []

    self.itemClicked.connect(self.onItemClicked)

  def onItemClicked(self, item: QtWidgets.QTreeWidgetItem, column: int) -> None:
    entryId = item.data(0, QtCore.Qt.ItemDataRole.UserRole)

    if entryId > 0:
      date = julianDayToDate(entryId)
      self.logEntryClickedSignal.emit(date)

  def setLogDates(self, dateList: list[datetime.date]):
    self.logDates = dateList

    # Turn off sorting while items are inserted, to speed up insertion.
    self.setSortingEnabled(False)

    for logEntryDate in self.logDates:
      self.addDayToLogTree(logEntryDate)

    # Turn sorting back on
    self.setSortingEnabled(True)
    self.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)

  def addLogDate(self, date: datetime.date):
    """ Adds a new date to the tree. """
    item = self.findEntryByDate(date)

    if item is None:
      # New item
      self.addDayToLogTree(date)
    else:
      # If the item already exists, it might be a temporary day, which uses the italic font.
      # In this case, turn off the italic
      self.setItemItalic(item, False)

  def setCurrentDate(self, date: datetime.date):
    item = self.findEntryByDate(date)

    if item is not None:
      self.setCurrentItem(item)

  def addDayToLogTree(self, logEntryDate: datetime.date) -> QtWidgets.QTreeWidgetItem | None:
    entryId = dateToJulianDay(logEntryDate)
    yearItem = self.addYearToLogTree(logEntryDate.year)

    if yearItem is not None:
      monthItem = self.addMonthToLogTree(yearItem, logEntryDate.month)

      if monthItem is not None:
        dayStr = formatDate(logEntryDate)

        dayItem = self.findChildItem(monthItem, dayStr)

        if dayItem is None:
          # Day not found - add it
          dayItem = CDateWidgetItem(monthItem)

          if dayItem is not None:
            dayItem.setText(0, dayStr)
            dayItem.setData(0, QtCore.Qt.ItemDataRole.UserRole, entryId)
            return dayItem
          else:
            logging.error('[addDayToLogTree] Failed to create a CDateWidgetItem')
            return None
        else:
          return dayItem

  def addYearToLogTree(self, year: int) -> QtWidgets.QTreeWidgetItem | None:
    yearStr = str(year)

    yearList = self.findItems(yearStr, QtCore.Qt.MatchFlag.MatchFixedString, 0)

    if len(yearList) == 0:
      # This year does not exist - create it
      yearItem = QtWidgets.QTreeWidgetItem(self)

      if yearItem is not None:
        yearItem.setText(0, yearStr)
        return yearItem
      else:
        logging.error(f'[addDayToLogTree] Error creating a year item')
        return None
    else:
      return yearList[0]

  def addMonthToLogTree(self, yearItem: QtWidgets.QTreeWidgetItem, month: int) -> CMonthWidgetItem | None:
    monthName = calendar.month_name[month]    # Note: This assumes 1 = January

    monthItem = self.findChildItem(yearItem, monthName)

    if monthItem is None:
      monthItem = CMonthWidgetItem(yearItem)

      if monthItem is not None:
        monthItem.setText(0, monthName)
        monthItem.setData(0, QtCore.Qt.ItemDataRole.UserRole, month)
        return monthItem
      else:
        logging.error(f'[addMonthToLogTree] Error creating a month item')
        return None
    else:
      return typing.cast(CMonthWidgetItem, monthItem)

  def findChildItem(self, parent: QtWidgets.QTreeWidgetItem, itemName: str) -> QtWidgets.QTreeWidgetItem | None:

    itemList = self.findItems(itemName, typing.cast(QtCore.Qt.MatchFlags, QtCore.Qt.MatchFlag.MatchFixedString | QtCore.Qt.MatchFlag.MatchRecursive), 0)

    if len(itemList) > 0:
      for item in itemList:
        if item.parent() == parent:
          return item

    return None

  def findEntryByDate(self, date: datetime.date) -> QtWidgets.QTreeWidgetItem | None:
    itemString = formatDate(date)

    itemList = self.findItems(itemString, typing.cast(QtCore.Qt.MatchFlags, QtCore.Qt.MatchFlag.MatchFixedString | QtCore.Qt.MatchFlag.MatchRecursive), 0)

    if len(itemList) > 0:
      return itemList[0]
    else:
      return None

  def makeTemporaryEntryPermanent(self, date: datetime.date, entryId: int):
    item = self.findEntryByDate(date)

    if item is not None:
      item.setData(0, QtCore.Qt.ItemDataRole.UserRole, entryId)
      self.setItemItalic(item, False)

  def addTemporaryDay(self, date: datetime.date) -> None:
    item = self.addDayToLogTree(date)

    if item is not None:
      self.setItemItalic(item, True)

  def removeTemporaryDay(self, dateOrLogId: datetime.date | int):
    if isinstance(dateOrLogId, datetime.date):
      date = dateOrLogId
    else:
      date = julianDayToDate(dateOrLogId)

    dateItem = self.findEntryByDate(date)

    if dateItem is not None:
      parent = dateItem.parent()
      parent.removeChild(dateItem)

      # If a parent (a month node) has no children, remove it
      while parent.childCount() == 0 and parent.parent() is not None:
        grandParent = parent.parent()

        grandParent.removeChild(parent)
        parent = grandParent

  def setItemItalic(self, item, italicFlag):
    itemFont = item.font(0)
    itemFont.setItalic(italicFlag)
    item.setFont(0, itemFont)
