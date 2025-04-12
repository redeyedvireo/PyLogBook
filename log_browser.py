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
    self.currentPageNum = 0       # Zero-based page number
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

      self.ui.pageSpin.setMaximum(self.getNumPages())

      # Go back to page 0
      self.gotoPage(0)

      self.updateNumberOfPagesLabel()
      self.updatePageButtons(self.getCurrentPageAsOneBasedNumber())

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

    entryId = dateToJulianDay(date)
    headerText = f'<a name="{entryId}"><h3>{formatDate(date)}</h3></a><br>'
    self.ui.textBrowser.insertHtml(headerText)
    self.ui.textBrowser.insertHtml(content)

  def addDate(self, date: datetime.date):
    if date not in self.logDates:
      self.logDates.append(date)

      self.logDates.sort()

      self.ui.pageSpin.setMaximum(self.getNumPages())

      self.updateNumberOfPagesLabel()
      self.onEndButtonClicked()       # Go to the last page (we're assuming that the date being added is the latest date)
      self.displayCurrentBrowserPage()
      self.updatePageButtons(self.getCurrentPageAsOneBasedNumber())

  def addDates(self, dates: list[datetime.date]):
    for date in dates:
      if date not in self.logDates:
        self.logDates.append(date)

    self.logDates.sort()

    self.ui.pageSpin.setMaximum(self.getNumPages())

    self.displayCurrentBrowserPage()
    self.updateNumberOfPagesLabel()
    self.updatePageButtons(self.getCurrentPageAsOneBasedNumber())

  def setDateList(self, dateList: list[datetime.date]) -> None:
    self.logDates = dateList

    self.logDates.sort()

    if len(self.logDates) > 0:
      self.ui.pageSpin.setEnabled(True)
      self.ui.pageSpin.setMinimum(1)
      self.ui.pageSpin.setMaximum(self.getNumPages())

    self.updateNumberOfPagesLabel()

    self.updatePageButtons(self.getCurrentPageAsOneBasedNumber())

  def getNumPages(self):
    numPages = len(self.logDates) / self.numEntriesPerPage

    if len(self.logDates) % self.numEntriesPerPage != 0:
      numPages += 1

    return int(numPages)

  def getLastPage(self):
    numPages = self.getNumPages()
    return numPages - 1 if numPages > 0 else 0

  def updateNumberOfPagesLabel(self):
    self.ui.numPagesLabel.setText(f'/ {self.getNumPages()} pages')

  def scrollToItem(self, inDate: datetime.date) -> None:
    if inDate in self.logDates:
      index = self.logDates.index(inDate)
      pageNum = index // self.numEntriesPerPage   # Integer division
    elif inDate == datetime.date.today():
      # This might be the "temporary day"
      pageNum = self.getLastPage()
    else:
      # Date not found - do nothing
      return

    self.gotoPage(pageNum)

    entryId = dateToJulianDay(inDate)

    if entryId is not None:
      # Scroll to the given date
      self.ui.textBrowser.scrollToAnchor(f'{entryId}')

  def gotoPage(self, pageNum: int) -> None:
    """Displays the given page in the browser.  The page number is zero-based.

    Args:
        pageNum (int): Zero-based page number
    """
    if pageNum <= self.getNumPages() and pageNum >= 0:
      # See if this page is already current

      if self.currentPageNum != pageNum:
        self.currentPageNum = pageNum
        self.displayCurrentBrowserPage()

        # Update page spinner
        oneBasedPageNum = pageNum + 1
        self.ui.pageSpin.setValue(oneBasedPageNum)

        self.updatePageButtons(oneBasedPageNum)

  def updatePageButtons(self, oneBasedPageNumber: int):
    self.ui.nextButton.setEnabled(oneBasedPageNumber < self.getNumPages() and self.getNumPages() > 1)
    self.ui.endButton.setEnabled(oneBasedPageNumber < self.getNumPages() and self.getNumPages() > 1)
    self.ui.previousButton.setEnabled(oneBasedPageNumber > 1 and self.getNumPages() > 1)
    self.ui.beginButton.setEnabled(oneBasedPageNumber > 1 and self.getNumPages() > 1)

  def getCurrentPageAsOneBasedNumber(self) -> int:
    return self.currentPageNum + 1

  @QtCore.Slot()
  def onBeginButtonClicked(self):
    self.gotoPage(0)

  @QtCore.Slot()
  def onEndButtonClicked(self):
    self.gotoPage(self.getLastPage())

  @QtCore.Slot()
  def onPreviousButtonClicked(self):
    if self.currentPageNum > 0:
      self.gotoPage(self.currentPageNum - 1)

  @QtCore.Slot()
  def onNextButtonClicked(self):
    if self.currentPageNum < self.getNumPages() - 1:
      self.gotoPage(self.currentPageNum + 1)

  @QtCore.Slot(int)
  def onPageSpinValueChanged(self, value: int):
    zeroBasedPageNumber = value - 1
    destinationPageNum = min(max(zeroBasedPageNumber, 0), self.getNumPages() - 1)

    self.gotoPage(destinationPageNum)
