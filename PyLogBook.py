import sys
import os
import os.path
import platform
import datetime
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from PySide6 import QtCore, QtGui, QtWidgets

from ui_PyLogBookWindow import Ui_PyLogBookWindow

from SetPasswordDialog import SetPasswordDialog
from database import Database

from constants import kTempItemId, errNoDateFound, kPrefsFileName
from log_entry import LogEntry
from preferences import Preferences
from prefs_dialog import PrefsDialog
from utility import dateToJulianDay, formatDate, formatDateTime, julianDayToDate

from xml_file import XmlHandler

kLogFile = 'PyLogBook.log'
kAppName = 'PyLogBook'

kMaxLogileSize = 1024 * 1024

scriptPath = os.path.realpath(__file__)
scriptDir = os.path.dirname(scriptPath)

# ---------------------------------------------------------------
class PyLogBookWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(PyLogBookWindow, self).__init__()

    self.ui = Ui_PyLogBookWindow()
    self.ui.setupUi(self)

    prefsFilePath = self.getPrefsPath()
    print(f'Prefs file: {prefsFilePath}')
    self.prefs = Preferences(prefsFilePath)

    self.databaseFileName = ''
    self.logDir = scriptDir
    self.db = Database()

    self.currentDate = datetime.date.today()
    self.currentEntryId = dateToJulianDay(self.currentDate)
    self.tempNewLog = ''

    self.ui.logBrowser.setDb(self.db)

    self.ui.submitButton.clicked.connect(self.onSubmitButtonClicked)
    self.ui.curMonth.dateSelectedSignal.connect(self.onDisplayLogEntryScrollBrowser)
    self.ui.logEdit.logTextChangedSignal.connect(self.onLogTextChanged)
    self.ui.logEntryTree.logEntryClickedSignal.connect(self.onDisplayLogEntryScrollBrowser)

    QtCore.QTimer.singleShot(0, self.initialize)

  def initialize(self):
    logging.info("Starting application...")

    # Disallow deleting log entries.  In the future, might want to have a
    # preference that allows entries to be deleted.
    self.ui.deleteButton.hide()

    self.prefs.readPrefsFile()

    pos = self.prefs.getWindowPos()
    size = self.prefs.getWindowSize()

    if pos is not None:
      self.move(pos)

    if size is not None:
      self.resize(size)

    self.ui.logBrowser.setNumEntriesPerPage(self.prefs.getNumEntriesPerPage())

    if self.prefs.openPreviousLogOnStartup():
      logFileTuple = self.prefs.getPreviousLogFilePath()
      if logFileTuple is not None:
        logFileDir, logFileName = logFileTuple
        self.databaseFileName = logFileName
        self.logDir = logFileDir

        if not self.openLogFile():
          self.enableLogEntry(False)
      return

    # Just show an empty workspace
    # Disable log entry until a log file is either loaded or created.
    self.enableLogEntry(False)

  def openLogFile(self) -> bool:
    if len(self.getDatabasePath()) > 0:
      if self.db.openDatabase(self.getDatabasePath()):
        if self.db.isPasswordProtected():
          password = ''

          for x in range(3):
            passwordTuple = QtWidgets.QInputDialog.getText(self, 'PyLogBook - Enter Password',
                                                      'Enter log password:', QtWidgets.QLineEdit.EchoMode.Password)

            if passwordTuple[1]:
              password = passwordTuple[0]

              if self.db.passwordMatch(password):
                # Password correct
                self.db.setPasswordInMemory(password)
                break
              else:
                # Wrong password.  Has the user used up all 3 attempts?
                if x == 2:
                  # Yup
                  QtWidgets.QMessageBox.critical(self, kAppName, 'The password you entered was incorrect.')
                  self.db.closeDatabase()
                  return False
            else:
              # User clicked cancel
              self.db.closeDatabase()
              return False

        # These 3 calls are done in on_actionOpen_triggered
        self.setInitialBrowserEntries()

        self.setAppTitle()
        self.prefs.setLogFilePath(self.getDatabasePath())
        return True
      else:
        return False
    else:
      return False

  def closeLogFile(self):
    if self.db.isDatabaseOpen():
      successful = self.checkSaveLog()

      # TODO: May want to loop here, to give the user another chance to save

      self.db.closeDatabase()
      self.databaseFileName = ''

      self.clearAllControls()
      self.enableLogEntry(False)
      self.setAppTitle()

  def getDatabasePath(self) -> str:
    return os.path.normpath(os.path.join(self.getDatabaseDirectory(), self.databaseFileName))

  def getDatabaseDirectory(self):
    return self.logDir

  def getPrefsPath(self) -> str:
    """ Returns the full path to the prefs file. """
    if platform.system() == 'Windows':
      appDataDir = os.getenv('APPDATA', scriptPath)
      return os.path.normpath(os.path.join(appDataDir, kAppName, kPrefsFileName))
    elif platform.system() == 'Linux':
      homeDirObj = Path.home()
      prefsFileObj = homeDirObj / '.pylogbook' / kPrefsFileName
      print(f'Prefs path: {prefsFileObj}')
      return os.fspath(prefsFileObj)
    else:
      print('[getPrefsPath] Only Windows and Linux are currently supported')
      return ''

  def setAppTitle(self):
    if len(self.databaseFileName) > 0:
      self.setWindowTitle(f'PyLogBook - {self.getDatabasePath()}')
    else:
      self.setWindowTitle('PyLogBook')

  def clearAllControls(self):
    self.ui.logEntryTree.clear()
    self.ui.curMonth.clear()
    self.ui.logBrowser.clear()
    self.ui.logEdit.clear()
    self.ui.tagsEdit.clear()

  def enableLogEntry(self, enable):
    self.ui.submitButton.setEnabled(enable)
    self.ui.addendumButton.setEnabled(enable)
    self.ui.logEdit.setEnabled(enable)
    self.ui.tagsEdit.setEnabled(enable)
    self.ui.deleteButton.setEnabled(enable)

  def initControls(self):
    dateList = self.db.getEntryDates()
    self.ui.curMonth.setLogDates(dateList)
    self.ui.logEntryTree.setLogDates(dateList)

  def displayLog(self, entryId: int):
    if entryId != kTempItemId:
      if self.db.entryExists(entryId):
        logEntry = self.db.getLogEntry(entryId)

        if logEntry is not None:
          self.ui.logEdit.setDocumentText(logEntry.content)
          self.ui.tagsEdit.setText(logEntry.tagsAsString())
          self.ui.logDateLabel.setText(logEntry.entryDateAsString())
          self.ui.lastModificationDateLabel.setText(logEntry.lastModifiedDateAsFormattedString())
          self.ui.numChangesLabel.setText(logEntry.numModificationsAsString())

          self.currentEntryId = entryId

          self.ui.deleteButton.setEnabled(True)
          self.ui.submitButton.setEnabled(False)
        else:
          logging.error(f'[PyLogBookWindow.displayLog] Entry {entryId} not found in database')
          QtWidgets.QMessageBox.critical(self, kAppName, "Entry was not found in the database")
      else:
        # The entry does not exist.  The user is allowed to create entries for any day.
        entryDate = julianDayToDate(entryId)

        self.tempNewLog = ''

        fontSize = self.prefs.getEditorDefaultFontSize()

        if fontSize < 0:
          fontSize = 10

        fontFamily = self.prefs.getEditorDefaultFontFamily()
        self.ui.logEdit.newDocument(fontFamily, fontSize)

        self.ui.tagsEdit.setText('')
        self.ui.logDateLabel.setText(formatDate(entryDate))
        self.ui.lastModificationDateLabel.setText(formatDateTime(datetime.datetime.now(datetime.timezone.utc)))
        self.ui.numChangesLabel.setText('0')

        self.currentEntryId = entryId

        self.ui.deleteButton.setEnabled(False)
        self.ui.submitButton.setEnabled(True)

  def removeTemporaryDay(self):
    if self.currentEntryId == kTempItemId:
      self.ui.logEntryTree.removeTemporaryDay(self.currentEntryId)

  def setInitialEntryToDisplay(self):
    # Display today's date to start with.  If there is no entry for
    # today, create the new log, and set the display tab to the edit tab

    entryId = kTempItemId
    self.currentDate = datetime.date.today()

    if self.db.entryExistsForDate(self.currentDate):
      entryId = dateToJulianDay(self.currentDate)

    self.currentEntryId = entryId

    if self.currentEntryId == kTempItemId:
      # This is the first item entered - Connect database to log browser and log tree
      self.createNewLogEntry(self.currentDate)

      # TODO: Hide the "Add Addendum" button (need a function that shows/hides appropriate buttons)
    else:
      # Fetch the entry
      self.setDateCurrent(julianDayToDate(entryId), True)

  def setInitialBrowserEntries(self):
    dateList = self.db.getEntryDates()
    self.ui.logBrowser.setDateList(dateList)
    self.ui.logBrowser.displayCurrentBrowserPage()

  def createNewLogEntry(self, date: datetime.date):
    self.ui.logEdit.clear()
    self.ui.tagsEdit.clear()

    # Create the log entry
    self.tempNewLog = ''

    self.currentDate = date
    self.currentEntryId = dateToJulianDay(date)

    fontSize = self.prefs.getEditorDefaultFontSize()

    if fontSize <= 0:
      fontSize = 10

    fontFamily = self.prefs.getEditorDefaultFontFamily()
    self.ui.logEdit.newDocument(fontFamily, fontSize)

    self.ui.logDateLabel.setText(formatDate(date))
    self.ui.lastModificationDateLabel.setText(formatDateTime(datetime.datetime.now(datetime.timezone.utc)))
    self.ui.numChangesLabel.setText("0")

    self.ui.logEntryTree.addTemporaryDay(self.currentDate)

  def saveLogEntry(self) -> tuple[bool, bool, int]:
    """ Saves the log entry as self.currentEntryId.
        Returns a tuple:
        (success, newLog?, logId)
    """
    if self.db.entryExists(self.currentEntryId):
      success = self.db.updateLog(self.currentEntryId, self.ui.logEdit.toHtml(), self.ui.tagsEdit.text())
      if success:
        return (True, False, self.currentEntryId)
      else:
        logging.error('[saveLogEntry] Log update unsuccessful')
        QtWidgets.QMessageBox.critical(self, kAppName, "Log update unsuccessful")
        return (False, False, kTempItemId)
    else:
      # New entry - create it
      logEntry = LogEntry.fromData(0, self.ui.logEdit.toHtml(), self.ui.tagsEdit.text(), datetime.datetime.now(datetime.timezone.utc))
      entryId = self.db.addNewLog(self.currentDate, logEntry)

      if entryId is None:
        return (False, True, kTempItemId)
      else:
        return (True, True, entryId)

  def addNewLogEntryToWidgets(self, entryId):
    """ Adds a new log entry to the calendar, log entry tree, and log browser. """
    # Add entry to the calendar widget
    self.ui.curMonth.addLogDate(self.currentDate)

    # Add entry to the log browser
    self.ui.logBrowser.addDate(self.currentDate)

    # Add entry to the log entry tree
    self.ui.logEntryTree.addLogDate(self.currentDate)

  def setDateCurrent(self, inDate: datetime.date, scrollLogBrowser: bool):
    self.removeTemporaryDay()

    # Scroll to this date in the log tree
    self.ui.logEntryTree.setCurrentDate(inDate)

    # Scroll to this date in the log browser, if requested
    if scrollLogBrowser:
      self.ui.logBrowser.scrollToItem(inDate)

    self.ui.curMonth.setCurrentDate(inDate)

    entryId = dateToJulianDay(inDate)

    if entryId != errNoDateFound and entryId != kTempItemId:
      self.currentEntryId = entryId
      self.currentDate = inDate

      self.displayLog(entryId)

  @QtCore.Slot()
  def on_addendumButton_clicked(self):
    self.ui.logEdit.addAddendum()

  @QtCore.Slot()
  def on_actionNew_Log_File_triggered(self):
    filepathTuple = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          "LogBook - New Log File",
                                                          self.logDir,
                                                          'Log files (*.db)')

    if len(filepathTuple[0]) > 0:
      filepath = filepathTuple[0]
      self.databaseFileName = os.path.basename(filepath)
      self.logDir = os.path.dirname(filepath)

      password = ''
      dlg = SetPasswordDialog(self)
      if dlg.exec() == QtWidgets.QDialog.Accepted:
        password = dlg.getPassword()

      self.db.open(filepath)

      if len(password) > 0:
        self.db.storePassword(password)

      # Create new entry for today
      self.clearAllControls()
      self.enableLogEntry(True)
      self.initControls()
      self.setInitialEntryToDisplay()

      self.setAppTitle()

  @QtCore.Slot()
  def on_actionOpen_triggered(self):
    filepathTuple = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "LogBook - Open Log File",
                                                          self.logDir,
                                                          'Log files (*.db)')

    if len(filepathTuple[0]) > 0:
      if self.db.isDatabaseOpen():
        self.db.closeDatabase()
        self.clearAllControls()

      dbFilePath = filepathTuple[0]

      self.logDir = os.path.dirname(dbFilePath)
      self.databaseFileName = os.path.basename(dbFilePath)

      if self.openLogFile():

        self.enableLogEntry(True)
        self.initControls()
        self.setInitialEntryToDisplay()

  @QtCore.Slot()
  def on_actionClose_triggered(self):
    self.closeLogFile()

  @QtCore.Slot()
  def on_actionImport_XML_triggered(self):
    filepathTuple = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "LogBook - Import Log File XML",
                                                          self.logDir,
                                                          'Log XML files (*.xml)')

    if len(filepathTuple[0]) > 0:
      xmlHandler = XmlHandler(self.db)
      success, entryIds, earliestDate, latestDate = xmlHandler.importLogFile(filepathTuple[0])
      if success:
        entryDates = [ julianDayToDate(d) for d in entryIds ]
        self.ui.logEntryTree.addLogDates(entryDates)
        self.ui.curMonth.addLogDates(entryDates)
        self.ui.logBrowser.addDates(entryDates)

        msg = f'{len(entryDates)} log imported.\nDate range {formatDate(earliestDate)} to {formatDate(latestDate)}'
        QtWidgets.QMessageBox.information(self, 'Logs imported', msg)
      else:
        print('Error importing file')

  @QtCore.Slot()
  def on_actionExport_XML_triggered(self):
    filepathTuple = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          "LogBook - Export Log File XML",
                                                          self.logDir,
                                                          'Log XML files (*.xml)')

    if len(filepathTuple[0]) > 0:
      filepath = filepathTuple[0]
      xmlHandler = XmlHandler(self.db)
      success = xmlHandler.exportLogFile(filepath)

      if success:
        QtWidgets.QMessageBox.information(self, 'Log Export', 'Exported to XML successfully.')
      else:
        QtWidgets.QMessageBox.information(self, 'Log Export', 'An error occurred exporting to XML.')

  @QtCore.Slot()
  def on_actionExit_triggered(self):
    self.close()

  @QtCore.Slot()
  def on_actionPreferences_triggered(self):
    prefsDialog = PrefsDialog(self, self.prefs)
    if prefsDialog.exec() == QtWidgets.QDialog.Accepted:
      self.prefs.writePrefsFile()
      self.ui.logBrowser.setNumEntriesPerPage(self.prefs.getNumEntriesPerPage())

  @QtCore.Slot()
  def on_actionAbout_Qt_triggered(self):
    QtWidgets.QMessageBox.aboutQt(self, 'About Qt')

  @QtCore.Slot()
  def on_actionAbout_PyLogBook_triggered(self):
    QtWidgets.QMessageBox.about(self, "About PyLogBook", "PyLogBook by Jeff Geraci")

  @QtCore.Slot()
  def onLogTextChanged(self):
    self.ui.submitButton.setEnabled(True)

  @QtCore.Slot()
  def onSubmitButtonClicked(self):
    success, newLog, entryId = self.saveLogEntry()

    if not success:
      logging.error('[onSubmitButtonClicked] Log update unsuccessful')
      QtWidgets.QMessageBox.critical(self, kAppName, "There was a problem when saving the log.  The log was not saved.")
      return

    if newLog:
      if entryId != kTempItemId:
        # Update the UI
        self.addNewLogEntryToWidgets(entryId)

        # Set current entry
        self.currentEntryId = entryId

    else:
      # Existing log
      self.ui.logBrowser.displayCurrentBrowserPage()

    # Update the UI
    self.ui.logEdit.setDocumentModified(False)
    self.ui.submitButton.setEnabled(False)


  def onDisplayLogEntryScrollBrowser(self, date: datetime.date) -> None:
    entryId = dateToJulianDay(date)
    self.onDisplayLogEntry(entryId, False)

  def checkSaveLog(self) -> bool:
    """ If the current log entry is modified but not saved, asks the user whether he wants to save, and
        saves it if he answers Yes.  Returns an error code.  False indicates there was an error saving,
        True indicates no error.
    """
    if self.ui.logEdit.isModified():
      message = 'The current log entry has not been saved.  Would you like to save it?'
      button = QtWidgets.QMessageBox.question(self, kAppName, message)

      if button == QtWidgets.QMessageBox.StandardButton.Yes:
        success, newLog, savedEntryId = self.saveLogEntry()

        if not success:
          logging.error('[onDisplayLogEntry] Log update unsuccessful')
          QtWidgets.QMessageBox.critical(self, kAppName, "There was a problem when saving the log.  The log was not saved.")
          return False

    return True

  def onDisplayLogEntry(self, entryId: int, scrollBrowser: bool) -> None:
    if entryId != kTempItemId:
      self.checkSaveLog()
      date = julianDayToDate(entryId)
      self.setDateCurrent(date, scrollBrowser)

  def closeEvent(self, event):
    self.closeAppWindow()

  def closeAppWindow(self):
    logging.info('Closing app window...')
    self.closeLogFile()
    self.prefs.setWindowPos(self.pos())
    self.prefs.setWindowSize(self.size())
    self.prefs.writePrefsFile()

def shutdownApp():
  logging.info("Shutting down...")
  logging.shutdown()

def getLogfilePath():
  return os.path.join(scriptDir, kLogFile)

def main():
  console = logging.StreamHandler()
  rotatingFileHandler = RotatingFileHandler(getLogfilePath(), maxBytes=kMaxLogileSize, backupCount=9)
  logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                          handlers=[ rotatingFileHandler, console ])

  try:
    app = QtWidgets.QApplication(sys.argv)
    wind = PyLogBookWindow()
    wind.show()

  except Exception as inst:
    print(f'Shutdown exception: {inst}')
    logging.error(f'[main] Exception: type: {type(inst)}')
    logging.error(f'Exception args: {inst.args}')
    logging.error(f'Exception object: {inst}')
    sys.exit(1)

  returnVal = app.exec()
  shutdownApp()

  sys.exit(returnVal)

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
