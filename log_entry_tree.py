from PyQt5 import uic, QtCore, QtGui, QtWidgets
import typing
import logging
import datetime
import calendar
from date_widget_item import CDateWidgetItem
from month_widget_item import CMonthWidgetItem

from utility import dateToJulianDay, formatDate

class CLogEntryTree(QtWidgets.QTreeWidget):
  def __init__(self, parent):
    super(CLogEntryTree, self).__init__(parent)
    self.clear()
    self.logDates: list[datetime.date] = []

  def setLogDates(self, dateList: list[datetime.date]):
    self.logDates = dateList

    # Turn off sorting while items are inserted, to speed up insertion.
    self.setSortingEnabled(False)

    for logEntryDate in self.logDates:
      entryId = dateToJulianDay(logEntryDate)

      self.addDayToLogTree(logEntryDate, entryId)

    # Turn sorting back on
    self.setSortingEnabled(True)

  def setCurrentDate(self, date: datetime.date):
    item = self.findEntryByDate(date)

    if item is not None:
      self.setCurrentItem(item)

  def addDayToLogTree(self, logEntryDate: datetime.date, entryId: int) -> QtWidgets.QTreeWidgetItem | None:
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
      itemFont = item.font(0)
      itemFont.setItalic(False)
      item.setFont(0, itemFont)

  def addTemporaryDay(self, date: datetime.date, entryId: int) -> None:
    item = self.addDayToLogTree(date, entryId)

    if item is not None:
      itemFont = item.font(0)
      itemFont.setItalic(True)
      item.setFont(0, itemFont)
