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

    self.beginButton.clicked.connect(self.onBeginButtonClicked)
    self.endButton.clicked.connect(self.onEndButtonClicked)
    self.previousButton.clicked.connect(self.onPreviousButtonClicked)
    self.nextButton.clicked.connect(self.onNextButtonClicked)
    self.pageSpin.valueChanged.connect(self.onPageSpinValueChanged)

  def setDb(self, db: Database):
    self.db = db

  def clear(self):
    self.logDates = []
    self.displayCurrentBrowserPage()

  def setNumEntriesPerPage(self, numEntriesPerPage):
    if numEntriesPerPage != self.numEntriesPerPage:
      self.numEntriesPerPage = numEntriesPerPage
      self.pageScrollBar.setMaximum(self.getNumPages() - 1)

      # Go back to page 0
      self.currentPageNum = 0
      self.pageScrollBar.setValue(self.currentPageNum)
      self.displayCurrentBrowserPage()

  def displayCurrentBrowserPage(self):
    if self.db is None:
      return

    self.textBrowser.clear()

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
      self.textBrowser.insertHtml('<br><hr><br>')

    headerText = f'<h3>{formatDate(date)}</h3><br>'
    self.textBrowser.insertHtml(headerText)
    self.textBrowser.insertHtml(content)

  def addDate(self, date: datetime.date):
    if date not in self.logDates:
      self.logDates.append(date)

      self.logDates.sort()

      self.pageSpin.setMaximum(self.getNumPages())

      self.displayCurrentBrowserPage()
      self.updateNumberOfPagesLabel()

  def setDateList(self, dateList: list[datetime.date]) -> None:
    self.logDates = dateList

    self.logDates.sort()

    if len(self.logDates) > 0:
      self.pageSpin.setEnabled(True)
      self.pageSpin.setMinimum(1)
      self.pageSpin.setMaximum(self.getNumPages())

    self.updateNumberOfPagesLabel()

  def getNumPages(self):
    numPages = len(self.logDates) / self.numEntriesPerPage

    if len(self.logDates) % self.numEntriesPerPage != 0:
      numPages += 1

    return int(numPages)

  def updateNumberOfPagesLabel(self):
    self.numPagesLabel.setText(f'/ {self.getNumPages()} pages')

  def scrollToItem(self, inDate: datetime.date) -> None:
    # TODO: Implement
    pass

  def gotoPage(self, pageNum: int) -> None:
    if pageNum <= self.getNumPages() and pageNum > 0:
      # See if this page is already current
      zeroBasedPageNum = pageNum - 1

      if self.currentPageNum != zeroBasedPageNum:
        self.currentPageNum = zeroBasedPageNum
        self.displayCurrentBrowserPage()

        # Update horizontal scroll bar
        self.pageSpin.setValue(pageNum)

        self.nextButton.setEnabled(pageNum < self.getNumPages())
        self.previousButton.setEnabled(pageNum > 1)

  def getCurrentPageAsOneBasedNumber(self) -> int:
    return self.currentPageNum + 1

  @QtCore.pyqtSlot()
  def onBeginButtonClicked(self):
    self.gotoPage(1)

  @QtCore.pyqtSlot()
  def onEndButtonClicked(self):
    self.gotoPage(self.getNumPages())

  @QtCore.pyqtSlot()
  def onPreviousButtonClicked(self):
    curPage = self.getCurrentPageAsOneBasedNumber()

    if curPage > 1:
      self.gotoPage(curPage - 1)

  @QtCore.pyqtSlot()
  def onNextButtonClicked(self):
    curPage = self.getCurrentPageAsOneBasedNumber()

    if curPage < self.getNumPages():
      self.gotoPage(curPage + 1)

  @QtCore.pyqtSlot(int)
  def onPageSpinValueChanged(self, value: int):
    self.gotoPage(value)
