import sys
import os
import os.path
import platform
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from SetPasswordDialog import SetPasswordDialog
from database import Database

from constants import kTempItemId, errNoDateFound

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

    self.databaseFileName = ''
    self.logDir = scriptDir
    self.db = Database()

    self.currentDate = QtCore.QDate.currentDate()
    self.currentEntryId = kTempItemId
    self.tempNewLog = ''

    QtCore.QTimer.singleShot(0, self.initialize)

  def initialize(self):
    logging.info("Starting application...")

  def getDatabasePath(self):
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

  def initControls(self):
    dateList = self.db.getEntryDates()
    self.curMonth.setLogDates(dateList)
    self.logEntryTree.setLogDates(dateList)

  def setInitialEntryToDisplay(self):
    # Display today's date to start with.  If there is no entry for
    # today, create the new log, and set the display tab to the edit tab

    entryId = kTempItemId
    self.currentDate = QtCore.QDate.currentDate()

    if self.db.entryExists(self.currentDate):
      entryId = self.db.getLogIdForDate(self.currentDate)

    self.currentEntryId = entryId

    if self.currentEntryId == kTempItemId:
      # This is the first item entered - Connect database to log browser and log tree
      # TODO: This should probably be done in the constructor
      # self.logBrowser.setDb(self.db)
      # self.logEntryTree.setDb(self.db)
      self.createNewLogEntry(self.currentDate)

      # TODO: Hide the "Add Addendum" button (need a function that shows/hides appropriate buttons)
    else:
      # Fetch the entry
      self.setDateCurrent(self.db.getLogEntryDate(entryId), True)

  def createNewLogEntry(self, date):
    self.logEdit.clear()
    self.tagsEdit.clear()

    # Create the log entry
    self.tempNewLog = ''

    self.currentEntryId = kTempItemId
    self.currentDate = date

    # TODO: Implement this
    fontSize = 10  # TODO: m_prefs.GetIntPref("editor-defaulttextsize");

    if fontSize <= 0:
      fontSize = 10

    fontFamily = 'Arial'    # TODO: m_prefs.GetStringPref("editor-defaultfontfamily")
    self.logEdit.newDocument(fontFamily, fontSize)

    # TODO: Implement this
    # self.logDateLabel.setText(date.toString(Qt::SystemLocaleLongDate))
    # self.lastModificationDateLabel.setText(QDate::currentDate().toString(Qt::SystemLocaleLongDate))
    # self.numChangesLabel.setText("0")

    # self.logEntryTree.AddTemporaryDay(m_currentDate, m_currentEntryId)

  def setDateCurrent(self, inDate, scrollLogBrowser):
    # TODO: self.removeTemporaryDay()

    # Scroll to this date in the log tree
    self.logEntryTree.setCurrentDate(inDate)

    # Scroll to this date in the log browser, if requested
    if scrollLogBrowser:
      self.logBrowser.scrollToItem(inDate)

    self.curMonth.setCurrentDate(inDate)

    entryId = self.db.getLogIdForDate(inDate)

    if entryId != errNoDateFound and entryId != kTempItemId:
      self.currentEntryId = entryId
      self.currentDate = inDate

      self.DisplayLog(entryId)

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
    QtWidgets.QMessageBox.about(self, "Open Log File", "Open log file triggered")

  @QtCore.pyqtSlot()
  def on_actionClose_triggered(self):
    QtWidgets.QMessageBox.about(self, "Close Log File", "Close log file triggered")

  @QtCore.pyqtSlot()
  def on_actionExit_triggered(self):
    self.close()

  @QtCore.pyqtSlot()
  def on_actionAbout_Qt_triggered(self):
    QtWidgets.QMessageBox.aboutQt(self, 'About Qt')

  @QtCore.pyqtSlot()
  def on_actionAbout_PyLogBook_triggered(self):
    QtWidgets.QMessageBox.about(self, "About PyLogBook", "PyLogBook by Jeff Geraci")

  def closeEvent(self, event):
    self.closeAppWindow()

  def closeAppWindow(self):
    logging.info('Closing app window...')
    self.db.close()
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
