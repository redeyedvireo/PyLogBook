from PyQt5 import uic, QtCore, QtGui, QtWidgets
import datetime
from database import Database
from utility import dateToJulianDay, formatDate

class LogBrowser(QtWidgets.QWidget):
  def __init__(self, parent):
    super(LogBrowser, self).__init__(parent)
    uic.loadUi('log_browser.ui', self)

    self.logDates: list[datetime.date] = []
    self.numEntriesPerPage = 5
    self.currentPageNum = 0
    self.db = None

    self.pageSpin.setEnabled(False)

  def setDb(self, db: Database):
    self.db = db

  def clear(self):
    self.logDates = []
    self.displayCurrentBrowserPage()

  def displayCurrentBrowserPage(self):
    if self.db is None:
      return

    self.textBrowser.clear()

    # Loop and display several log entries
    startEntry = self.numEntriesPerPage * self.currentPageNum
    lastEntry = min(startEntry + self.numEntriesPerPage, len(self.dateList))

    for i in range(startEntry, lastEntry + 1):
      entryDate = self.dateList[i]
      entryId = dateToJulianDay(entryDate)
      logEntry = self.db.getLogEntry(entryId)

      if logEntry is not None:
        insertHLineBefore = (i > startEntry)
        self.addLogEntryToPage(logEntry.content, entryDate, insertHLineBefore)

  def addLogEntryToPage(self, content: str, date: datetime.date, insertHLineBefore: bool) -> None:
    if insertHLineBefore:
      self.textBrowser.insertHtml('<br><hr><br>')

    headerText = f'<h3>{formatDate(date)}</h3><br>'
    self.textBrowser.insertHtml(headerText)
    self.textBrowser.insertHtml(content)

  def addDate(self, date: datetime.date):
    if date not in self.dateList:
      self.dateList.append(date)

      self.dateList.sort()

      self.pageSpin.setMaximum(self.getNumPages())

      self.displayCurrentBrowserPage()
      self.updateNumberOfPagesLabel()

  def setDateList(self, dateList: list[datetime.date]) -> None:
    self.dateList = dateList

    self.dateList.sort()

    if len(self.dateList) > 0:
      self.pageSpin.setEnabled(True)
      self.pageSpin.setMinimum(1)
      self.pageSpin.setMaximum(self.getNumPages())

  def getNumPages(self):
    numPages = len(self.dateList) / self.numEntriesPerPage

    if len(self.dateList) % self.numEntriesPerPage != 0:
      numPages += 1

    return int(numPages)

  def updateNumberOfPagesLabel(self):
    self.numPagesLabel(f'/ {self.getNumPages()} pages')

  def scrollToItem(self, inDate: datetime.date) -> None:
    # TODO: Implement
    pass
