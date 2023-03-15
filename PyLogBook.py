import sys
import os
import os.path
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
from PyQt5 import QtCore, QtGui, QtWidgets, uic

kLogFile = 'PyLogBook.log'
kAppName = 'PyLogBook'
kDatabaseName = 'PyLogBook.db'

kMaxLogileSize = 1024 * 1024

scriptPath = os.path.realpath(__file__)
scriptDir = os.path.dirname(scriptPath)

# ---------------------------------------------------------------
class PyLogBookWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super(PyLogBookWindow, self).__init__()
    uic.loadUi('PyLogBookWindow.ui', self)

    console = logging.StreamHandler()
    rotatingFileHandler = RotatingFileHandler(self.getLogfilePath(), maxBytes=kMaxLogileSize, backupCount=9)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            handlers=[ rotatingFileHandler, console ])

    QtCore.QTimer.singleShot(0, self.initialize)

  def initialize(self):
    logging.info("Starting application...")

  def getLogfilePath(self):
    return os.path.join(self.getDatabaseDirectory(), kLogFile)

  def getDatabasePath(self):
      return "{}\\{}".format(self.getDatabaseDirectory(), kDatabaseName)

  def getDatabaseDirectory(self):
    procEnv = QtCore.QProcessEnvironment.systemEnvironment()

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

  def OpenLogFile(self):
    pass

  def closeEvent(self, event):
      self.shutdownApp()

  def shutdownApp(self):
      # self.db.close()
      # self.saveSettings()
      logging.info("Shutting down...")
      logging.shutdown()

def main():
  try:
    app = QtWidgets.QApplication(sys.argv)
    wind = PyLogBookWindow()
    wind.show()

  except Exception as inst:
    logging.error(f'[main] Exception: type: {type(inst)}')
    logging.error(f'Exception args: {inst.args}')
    logging.error(f'Exception object: {inst}')
    wind.shutdownApp()

  sys.exit(app.exec_())

# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
