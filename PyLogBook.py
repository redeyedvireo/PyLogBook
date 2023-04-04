import sys
import os
import os.path
import platform
import datetime
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from SetPasswordDialog import SetPasswordDialog
from database import Database

from constants import kTempItemId, errNoDateFound, kPrefsFileName
from log_entry import LogEntry
from preferences import Preferences
from prefs_dialog import PrefsDialog
from utility import dateToJulianDay, formatDate, formatDateTime, julianDayToDate

kLogFile = 'PyLogBook.log'
kAppName = 'PyLogBook'

kMaxLogileSize = 1024 * 1024

scriptPath = os.path.realpath(__file__)
scriptDir = os.path.dirname(scriptPath)

# ---------------------------------------------------------------
class PyLogBookWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(PyLogBookWindow, self).__init__()
    uic.loadUi('PyLogBookWindow.ui', self)

    prefsFilePath = self.getPrefsPath()
    print(f'Prefs file: {prefsFilePath}')
    self.prefs = Preferences(prefsFilePath)

    self.databaseFileName = ''
    self.logDir = scriptDir
    self.db = Database()

    self.currentDate = datetime.date.today()
    self.currentEntryId = dateToJulianDay(self.currentDate)
    self.tempNewLog = ''

    self.logBrowser.setDb(self.db)

    self.submitButton.clicked.connect(self.onSubmitButtonClicked)
    self.curMonth.dateSelectedSignal.connect(self.onDisplayLogEntryScrollBrowser)
    self.logEdit.logTextChangedSignal.connect(self.onLogTextChanged)
    self.logEntryTree.logEntryClickedSignal.connect(self.onDisplayLogEntryScrollBrowser)

    QtCore.QTimer.singleShot(0, self.initialize)

  def initialize(self):
    logging.info("Starting application...")

    self.prefs.readPrefsFile()

    self.logBrowser.setNumEntriesPerPage(self.prefs.getNumEntriesPerPage())

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

        self.initControls()
        self.setInitialEntryToDisplay()
        self.setInitialBrowserEntries()
        self.setAppTitle()
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

  # This code was taken from another app, and doesn't apply to PyLogBook.  But
  # I'm keeping this here because this might be used for setting the location
  # of the preferences (INI) file.
  # def getDatabaseDirectory(self):
  #   procEnv = QtCore.QProcessEnvironment.systemEnvironment()

  #   if platform.system() == 'Windows':
  #     if procEnv.contains("APPDATA"):
  #       # Indicates Windows platform
  #       appDataPath = procEnv.value("APPDATA")

  #       databasePath = "{}\\{}".format(appDataPath, kAppName)

  #       #  Create directory if non - existent
  #       dbDir = Path(databasePath)

  #       if not dbDir.exists():
  #         # Directory doesn't exist - create it.
  #         if not dbDir.mkdir():
  #           errMsg = "Could not create the data directory: {}".format(databasePath)
  #           logging.error(f'[PyLogBookWindow.getDatabaseDirectory]: {errMsg}')
  #           QtWidgets.QMessageBox.critical(self, kAppName, errMsg)
  #           return ""

  #       return databasePath
  #     else:
  #       logging.error('[PyLogBookWindow.getDatabasePath] Environment does not contain APPDATA')
  #       return ''
  #   else:
  #     logging.error('[PyLogBookWindow.getDatabasePath] Only Windows supported at the moment.')
  #     return ''

  def getDatabaseDirectory(self):
    return self.logDir

  def getPrefsPath(self) -> str:
    """ Returns the full path to the prefs file. """
    if platform.system() == 'Windows':
      appDataDir = os.getenv('APPDATA', scriptPath)
      return os.path.normpath(os.path.join(appDataDir, kAppName, kPrefsFileName))
    else:
      print('Prefs file not yet supported on non-Windows systems.')
      return ''

  def setAppTitle(self):
    if len(self.databaseFileName) > 0:
      self.setWindowTitle(f'PyLogBook - {self.getDatabasePath()}')
    else:
      self.setWindowTitle('PyLogBook')

  def clearAllControls(self):
    self.logEntryTree.clear()
    self.curMonth.clear()
    self.logBrowser.clear()
    self.logEdit.clear()
    self.tagsEdit.clear()

  def enableLogEntry(self, enable):
    self.submitButton.setEnabled(enable)
    self.addendumButton.setEnabled(enable)
    self.logEdit.setEnabled(enable)
    self.tagsEdit.setEnabled(enable)
    self.deleteButton.setEnabled(enable)

  def initControls(self):
    dateList = self.db.getEntryDates()
    self.curMonth.setLogDates(dateList)
    self.logEntryTree.setLogDates(dateList)

  def displayLog(self, entryId: int):
    if entryId != kTempItemId:
      if self.db.entryExists(entryId):
        logEntry = self.db.getLogEntry(entryId)

        if logEntry is not None:
          self.logEdit.setDocumentText(logEntry.content)
          self.tagsEdit.setText(logEntry.tagsAsString())
          self.logDateLabel.setText(logEntry.entryDateAsString())
          self.lastModificationDateLabel.setText(logEntry.lastModifiedDateAsFormattedString())
          self.numChangesLabel.setText(logEntry.numModificationsAsString())

          self.currentEntryId = entryId

          self.deleteButton.setEnabled(True)
          self.submitButton.setEnabled(False)
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
        self.logEdit.newDocument(fontFamily, fontSize)

        self.tagsEdit.setText('')
        self.logDateLabel.setText(formatDate(entryDate))
        self.lastModificationDateLabel.setText(formatDateTime(datetime.datetime.now(datetime.timezone.utc)))
        self.numChangesLabel.setText('0')

        self.currentEntryId = entryId

        self.deleteButton.setEnabled(False)
        self.submitButton.setEnabled(True)

  def removeTemporaryDay(self):
    if self.currentEntryId == kTempItemId:
      self.logEntryTree.removeTemporaryDay(self.currentEntryId)

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
    self.logBrowser.setDateList(dateList)
    self.logBrowser.displayCurrentBrowserPage()

  def createNewLogEntry(self, date: datetime.date):
    self.logEdit.clear()
    self.tagsEdit.clear()

    # Create the log entry
    self.tempNewLog = ''

    self.currentDate = date
    self.currentEntryId = dateToJulianDay(date)

    fontSize = self.prefs.getEditorDefaultFontSize()

    if fontSize <= 0:
      fontSize = 10

    fontFamily = self.prefs.getEditorDefaultFontFamily()
    self.logEdit.newDocument(fontFamily, fontSize)

    self.logDateLabel.setText(formatDate(date))
    self.lastModificationDateLabel.setText(formatDateTime(datetime.datetime.now(datetime.timezone.utc)))
    self.numChangesLabel.setText("0")

    self.logEntryTree.addTemporaryDay(self.currentDate)

  def saveLogEntry(self) -> tuple[bool, bool, int]:
    """ Saves the log entry as self.currentEntryId.
        Returns a tuple:
        (success, newLog?, logId)
    """
    if self.db.entryExists(self.currentEntryId):
      success = self.db.updateLog(self.currentEntryId, self.logEdit.toHtml(), self.tagsEdit.text())
      if success:
        return (True, False, self.currentEntryId)
      else:
        logging.error('[saveLogEntry] Log update unsuccessful')
        QtWidgets.QMessageBox.critical(self, kAppName, "Log update unsuccessful")
        return (False, False, kTempItemId)
    else:
      # New entry - create it
      logEntry = LogEntry.fromData(0, self.logEdit.toHtml(), self.tagsEdit.text(), datetime.datetime.now(datetime.timezone.utc))
      entryId = self.db.addNewLog(self.currentDate, logEntry)

      if entryId is None:
        return (False, True, kTempItemId)
      else:
        return (True, True, entryId)

  def addNewLogEntryToWidgets(self, entryId):
    """ Adds a new log entry to the calendar, log entry tree, and log browser. """
    # Add entry to the calendar widget
    self.curMonth.addLogDate(self.currentDate)

    # Add entry to the log browser
    self.logBrowser.addDate(self.currentDate)

    # Add entry to the log entry tree
    self.logEntryTree.addLogDate(self.currentDate)

  def setDateCurrent(self, inDate: datetime.date, scrollLogBrowser: bool):
    self.removeTemporaryDay()

    # Scroll to this date in the log tree
    self.logEntryTree.setCurrentDate(inDate)

    # Scroll to this date in the log browser, if requested
    if scrollLogBrowser:
      self.logBrowser.scrollToItem(inDate)

    self.curMonth.setCurrentDate(inDate)

    entryId = dateToJulianDay(inDate)

    if entryId != errNoDateFound and entryId != kTempItemId:
      self.currentEntryId = entryId
      self.currentDate = inDate

      self.displayLog(entryId)

  @QtCore.pyqtSlot()
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

  @QtCore.pyqtSlot()
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

  @QtCore.pyqtSlot()
  def on_actionClose_triggered(self):
    self.closeLogFile()

  @QtCore.pyqtSlot()
  def on_actionExit_triggered(self):
    self.close()

  @QtCore.pyqtSlot()
  def on_actionPreferences_triggered(self):
    prefsDialog = PrefsDialog(self)
    if prefsDialog.exec() == QtWidgets.QDialog.Accepted:
      print('OK selected')

  @QtCore.pyqtSlot()
  def on_actionAbout_Qt_triggered(self):
    QtWidgets.QMessageBox.aboutQt(self, 'About Qt')

  @QtCore.pyqtSlot()
  def on_actionAbout_PyLogBook_triggered(self):
    QtWidgets.QMessageBox.about(self, "About PyLogBook", "PyLogBook by Jeff Geraci")

  @QtCore.pyqtSlot()
  def onLogTextChanged(self):
    self.submitButton.setEnabled(True)

  @QtCore.pyqtSlot()
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
      self.logBrowser.displayCurrentBrowserPage()

    # Update the UI
    self.logEdit.setDocumentModified(False)
    self.submitButton.setEnabled(False)


  def onDisplayLogEntryScrollBrowser(self, date: datetime.date) -> None:
    entryId = dateToJulianDay(date)
    self.onDisplayLogEntry(entryId, False)

  def checkSaveLog(self) -> bool:
    """ If the current log entry is modified but not saved, asks the user whether he wants to save, and
        saves it if he answers Yes.  Returns an error code.  False indicates there was an error saving,
        True indicates no error.
    """
    if self.logEdit.isModified():
      message = 'The current log entry has not been saved.  Would you like to save it?'
      button = QtWidgets.QMessageBox.question(self, kAppName, message)

      if button == QtWidgets.QMessageBox.Yes:
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
    # self.saveSettings()

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

  returnVal = app.exec_()
  shutdownApp()

  sys.exit(returnVal)

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
