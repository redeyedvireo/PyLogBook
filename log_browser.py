from PySide6 import QtCore, QtGui, QtWidgets
import datetime
from database import Database
from ui_log_browser import Ui_LogBrowserWidgetSimple
from utility import dateToJulianDay, formatDate

class LogBrowser(QtWidgets.QWidget):
  def __init__(self, parent):
    super(LogBrowser, self).__init__(parent)

    self.ui = Ui_LogBrowserWidgetSimple()
    self.ui.setupUi(self)

    self.logDates: list[datetime.date] = []
    self.numEntriesPerPage = 5
    self.currentPageNum = 0
    self.db = None

    self.ui.pageSpin.setEnabled(False)

    self.ui.beginButton.clicked.connect(self.onBeginButtonClicked)
    self.ui.endButton.clicked.connect(self.onEndButtonClicked)
    self.ui.previousButton.clicked.connect(self.onPreviousButtonClicked)
    self.ui.nextButton.clicked.connect(self.onNextButtonClicked)
    self.ui.pageSpin.valueChanged.connect(self.onPageSpinValueChanged)

  def setDb(self, db: Database):
    self.db = db

  def clear(self):
    self.logDates = []
    self.displayCurrentBrowserPage()

  def setNumEntriesPerPage(self, numEntriesPerPage):
    if numEntriesPerPage != self.numEntriesPerPage:
      self.numEntriesPerPage = numEntriesPerPage

      # Go back to page 0
      self.currentPageNum = 0
      self.displayCurrentBrowserPage()

  def displayCurrentBrowserPage(self):
    if self.db is None:
      return

    self.ui.textBrowser.clear()

    # Loop and display several log entries
    startEntry = self.numEntriesPerPage * self.currentPageNum
    lastEntry = min(startEntry + self.numEntriesPerPage, len(self.logDates))

    for i in range(startEntry, lastEntry):
      entryDate = self.logDates[i]
      entryId = dateToJulianDay(entryDate)
      logEntry = self.db.getLogEntry(entryId)

      if logEntry is not None:
        insertHLineBefore = (i > startEntry)
        self.addLogEntryToPage(logEntry.content, entryDate, insertHLineBefore)

  def addLogEntryToPage(self, content: str, date: datetime.date, insertHLineBefore: bool) -> None:
    if insertHLineBefore:
      self.ui.textBrowser.insertHtml('<br><hr><br>')

    headerText = f'<h3>{formatDate(date)}</h3><br>'
    self.ui.textBrowser.insertHtml(headerText)
    self.ui.textBrowser.insertHtml(content)

  def addDate(self, date: datetime.date):
    if date not in self.logDates:
      self.logDates.append(date)

      self.logDates.sort()

      self.ui.pageSpin.setMaximum(self.getNumPages())

      self.displayCurrentBrowserPage()
      self.updateNumberOfPagesLabel()

  def addDates(self, dates: list[datetime.date]):
    for date in dates:
      if date not in self.logDates:
        self.logDates.append(date)

    self.logDates.sort()

    self.ui.pageSpin.setMaximum(self.getNumPages())

    self.displayCurrentBrowserPage()
    self.updateNumberOfPagesLabel()

  def setDateList(self, dateList: list[datetime.date]) -> None:
    self.logDates = dateList

    self.logDates.sort()

    if len(self.logDates) > 0:
      self.ui.pageSpin.setEnabled(True)
      self.ui.pageSpin.setMinimum(1)
      self.ui.pageSpin.setMaximum(self.getNumPages())

    self.updateNumberOfPagesLabel()

  def getNumPages(self):
    numPages = len(self.logDates) / self.numEntriesPerPage

    if len(self.logDates) % self.numEntriesPerPage != 0:
      numPages += 1

    return int(numPages)

  def updateNumberOfPagesLabel(self):
    self.ui.numPagesLabel.setText(f'/ {self.getNumPages()} pages')

  def scrollToItem(self, inDate: datetime.date) -> None:
    if inDate in self.logDates:
      index = self.logDates.index(inDate)

      pageNum = index / self.numEntriesPerPage
      self.gotoPage(pageNum)

      entryId = dateToJulianDay(inDate)

      if entryId is not None:
        # TODO: Scroll to the given date
        pass

  def gotoPage(self, pageNum: int) -> None:
    if pageNum <= self.getNumPages() and pageNum > 0:
      # See if this page is already current
      zeroBasedPageNum = pageNum - 1

      if self.currentPageNum != zeroBasedPageNum:
        self.currentPageNum = zeroBasedPageNum
        self.displayCurrentBrowserPage()

        # Update horizontal scroll bar
        self.ui.pageSpin.setValue(pageNum)

        self.ui.nextButton.setEnabled(pageNum < self.getNumPages())
        self.ui.previousButton.setEnabled(pageNum > 1)

  def getCurrentPageAsOneBasedNumber(self) -> int:
    return self.currentPageNum + 1

  @QtCore.Slot()
  def onBeginButtonClicked(self):
    self.gotoPage(1)

  @QtCore.Slot()
  def onEndButtonClicked(self):
    self.gotoPage(self.getNumPages())

  @QtCore.Slot()
  def onPreviousButtonClicked(self):
    curPage = self.getCurrentPageAsOneBasedNumber()

    if curPage > 1:
      self.gotoPage(curPage - 1)

  @QtCore.Slot()
  def onNextButtonClicked(self):
    curPage = self.getCurrentPageAsOneBasedNumber()

    if curPage < self.getNumPages():
      self.gotoPage(curPage + 1)

  @QtCore.Slot(int)
  def onPageSpinValueChanged(self, value: int):
    self.gotoPage(value)
