import logging
import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from database import Database

from ui_search_dialog import Ui_searchDialog
from utility import dateToJulianDay, julianDayToDate


class SearchDialog(QtWidgets.QDialog):
  dateSelectedSignal = QtCore.Signal(datetime.date)

  def __init__(self, db: Database, parent):
    super(SearchDialog, self).__init__(parent)

    self.ui = Ui_searchDialog()
    self.ui.setupUi(self)

    self.db = db

    self.setConnections()

  def setConnections(self):
    self.ui.searchEdit.returnPressed.connect(self.search)

  @QtCore.Slot()
  def on_closeButton_clicked(self):
    self.done(True)

  @QtCore.Slot()
  def on_searchButton_clicked(self):
    self.search()

  @QtCore.Slot(str)
  def on_searchEdit_textChanged(self, newText):
    searchTerm = self.ui.searchEdit.text()

    self.ui.searchButton.setEnabled(len(searchTerm) > 0)

  @QtCore.Slot(QtWidgets.QListWidgetItem)
  def on_resultsListWidget_itemClicked(self, item):
    pageId = item.data(QtCore.Qt.ItemDataRole.UserRole)
    entryDate = julianDayToDate(pageId)
    if entryDate is not None:
      self.dateSelectedSignal.emit(entryDate)

  def search(self):
    searchTerm = self.ui.searchEdit.text()
    self.doSearch(searchTerm)

  def doSearch(self, searchText):
    self.setWaitCursor()
    self.ui.resultsListWidget.clear()

    dateList = self.db.getEntryDates()

    # Scan each page, and check its title and contents for the search term
    for curDate in dateList:

      entryId = dateToJulianDay(curDate)

      logEntry = self.db.getLogEntry(entryId)

      if logEntry is None:
        logging.error(f"[SearchDialog.doSearch] No log entry found for date {curDate}.  Skipping.")
        continue

      if logEntry.containsString(searchText):
        self.addItem(logEntry.entryId)

    self.restoreCursor()

  def addItem(self, logIEntryId: int):
    entryDate = julianDayToDate(logIEntryId)
    if entryDate is not None:
      newItem = QtWidgets.QListWidgetItem(entryDate.strftime('%B %d, %Y'))
      newItem.setData(QtCore.Qt.ItemDataRole.UserRole, logIEntryId)
      self.ui.resultsListWidget.addItem(newItem)


  # TODO: These cursor methods should be moved to a utility class
  def setWaitCursor(self):
    app = self.getApp()
    if app is not None:
      app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))

  def restoreCursor(self):
    app = self.getApp()
    if app is not None:
      app.restoreOverrideCursor()

  def getApp(self) -> QtWidgets.QApplication | None:
    app = QtWidgets.QApplication.instance()
    if type(app) is QtWidgets.QApplication:
      return app
    return None
