import sys
import os
import os.path
import platform
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from PyQt5 import QtCore, QtGui, QtWidgets, uic

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

    self.databaseName = ''
    self.logDir = scriptDir

    QtCore.QTimer.singleShot(0, self.initialize)

  def initialize(self):
    logging.info("Starting application...")

  def getDatabasePath(self):
    return os.path.join(self.getDatabaseDirectory(), self.databaseName)

  def getDatabaseDirectory(self):
    procEnv = QtCore.QProcessEnvironment.systemEnvironment()

    if platform.system() == 'Windows':
      if procEnv.contains("APPDATA"):
        # Indicates Windows platform
        appDataPath = procEnv.value("APPDATA")

        databasePath = "{}\\{}".format(appDataPath, kAppName)

        #  Create directory if non - existent
        dbDir = Path(databasePath)

        if not dbDir.exists():
          # Directory doesn't exist - create it.
          if not dbDir.mkdir():
            errMsg = "Could not create the data directory: {}".format(databasePath)
            logging.error(f'[PyLogBookWindow.getDatabaseDirectory]: {errMsg}')
            QtWidgets.QMessageBox.critical(self, kAppName, errMsg)
            return ""

        return databasePath
      else:
        logging.error('[PyLogBookWindow.getDatabasePath] Environment does not contain APPDATA')
        return ''
    else:
      logging.error('[PyLogBookWindow.getDatabasePath] Only Windows supported at the moment.')
      return ''

  @QtCore.pyqtSlot()
  def on_actionNew_Log_File_triggered(self):
    filepathTuple = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          "LogBook - New Log File",
                                                          self.logDir,
                                                          'Log files (*.db)')

    if len(filepathTuple[0]) > 0:
      filepath = filepathTuple[0]
      print(f'filepath: {filepath}')
      self.databaseName = filepath
      self.logDir = os.path.dirname(filepath)
      print(f'log dir is now: {self.logDir}')

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
      self.shutdownApp()

  def shutdownApp(self):
      # self.db.close()
      # self.saveSettings()
    pass

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
    logging.error(f'[main] Exception: type: {type(inst)}')
    logging.error(f'Exception args: {inst.args}')
    logging.error(f'Exception object: {inst}')
    sys.exit(1)

  shutdownApp()
  sys.exit(app.exec_())

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
