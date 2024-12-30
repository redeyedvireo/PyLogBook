from PySide6 import QtCore
import configparser
import logging
import os.path
from pathlib import Path

from constants import kStartupLoadPreviousLog, \
                      kStartupEmptyWorkspace, \
                      kGeneralStartupLoad, \
                      kEditorDefaultTextSize, \
                      kBrowserLogsPerPage, \
                      kEditorDefaultFontFamily, \
                      kFilesLastLogDirectory, \
                      kFilesLastLogFile, \
                      kWindowSize, \
                      kWindowPos

class Preferences():
  def __init__(self, prefsFilePath) -> None:
    self.prefsFilePath = prefsFilePath

    # Default prefs
    self.prefsMap = {
      kGeneralStartupLoad: kStartupLoadPreviousLog,
      kEditorDefaultTextSize: 10,
      kEditorDefaultFontFamily: 'Arial',
      kBrowserLogsPerPage: 5,
      kFilesLastLogDirectory: '',
      kFilesLastLogFile: '',
      kWindowSize: '',
      kWindowPos: ''
    }

  def setLogFilePath(self, logFilePath):
    self.prefsMap[kFilesLastLogDirectory] = os.path.dirname(logFilePath)
    self.prefsMap[kFilesLastLogFile] = os.path.basename(logFilePath)

  def getPreviousLogFilePath(self) -> tuple[str, str] | None:
    if len(self.prefsMap[kFilesLastLogDirectory]) > 0 and len(self.prefsMap[kFilesLastLogFile]) > 0:
      return (self.prefsMap[kFilesLastLogDirectory], self.prefsMap[kFilesLastLogFile])
    else:
      return None

  def readPrefsFile(self):
    """ Reads the prefs from the prefs INI file. """
    configObj = configparser.ConfigParser()

    if not os.path.exists(self.prefsFilePath):
      # The prefs file does not exist.  Create it with app defaults
      self.writePrefsFile()
    else:
      try:
        configObj.read(self.prefsFilePath)

        self.prefsMap[kGeneralStartupLoad] = configObj.get('general', 'startupload', fallback=kStartupEmptyWorkspace)
        self.prefsMap[kEditorDefaultTextSize] = configObj.getint('editor', 'defaulttextsize', fallback=10)
        self.prefsMap[kBrowserLogsPerPage] = configObj.getint('browser', 'logsperpage', fallback=5)
        self.prefsMap[kEditorDefaultFontFamily] = configObj.get('browser', 'defaultfontfamily', fallback='Arial')
        self.prefsMap[kFilesLastLogDirectory] = configObj.get('files', 'lastlogdirectory', fallback='')
        self.prefsMap[kFilesLastLogFile] = configObj.get('files', 'lastlogfile', fallback='')
        self.prefsMap[kWindowPos] = configObj.get('window', 'pos', fallback='')
        self.prefsMap[kWindowSize] = configObj.get('window', 'size', fallback='')

      except Exception as inst:
        errMsg = "Exception: {}".format(inst)
        print(errMsg)
        logging.error(f'[readPrefsFile] {errMsg}')

  def writePrefsFile(self):
    configObj = configparser.ConfigParser()

    # Set prefs in in-memory prefs object
    for prefKey in self.prefsMap:
      items = prefKey.split('-')
      section = items[0]
      pref = items[1]

      if not configObj.has_section(section):
        # The section must be created before data can be stored in it
        configObj[section] = {}

      configObj[section][pref] = str(self.prefsMap[prefKey])

    # Write prefs to disk
    try:
      # Make sure the directory exists
      directory = os.path.dirname(self.prefsFilePath)
      path = Path(directory)
      if not path.exists():
        try:
          path.mkdir(parents=True)
        except Exception as inst:
          errMsg = "Creating prefs directory: {}".format(inst)
          print(errMsg)
          logging.error(f'[writePrefsFile] {errMsg}')
          return

      with open(self.prefsFilePath, 'w') as configFile:
        configObj.write(configFile)
    except Exception as inst:
      errMsg = "Writing prefs file: {}".format(inst)
      print(errMsg)
      logging.error(f'[writePrefsFile] {errMsg}')

  def getStartupAction(self) -> str:
    return self.prefsMap[kGeneralStartupLoad]

  def openPreviousLogOnStartup(self) -> bool:
    """ A convenience function for determining if the previous log file should be
        opened upon startup.
    """
    return self.prefsMap[kGeneralStartupLoad] == kStartupLoadPreviousLog

  def setStartupAction(self, action: str):
    if action == kStartupEmptyWorkspace:
      self.prefsMap[kGeneralStartupLoad] = kStartupEmptyWorkspace
    else:
      self.prefsMap[kGeneralStartupLoad] = kStartupLoadPreviousLog

  @property
  def editorDefaultFontSize(self) -> int:
    return self.prefsMap[kEditorDefaultTextSize]

  @editorDefaultFontSize.setter
  def editorDefaultFontSize(self, fontSize: int):
    self.prefsMap[kEditorDefaultTextSize] = fontSize

  @property
  def editorDefaultFontFamily(self) -> str:
    return self.prefsMap[kEditorDefaultFontFamily]

  @editorDefaultFontFamily.setter
  def editorDefaultFontFamily(self, fontFamily: str):
    self.prefsMap[kEditorDefaultFontFamily] = fontFamily

  def getNumEntriesPerPage(self) -> int:
    return self.prefsMap[kBrowserLogsPerPage]

  def setNumEntriesPerPage(self, numEntriesPerPage: int):
    self.prefsMap[kBrowserLogsPerPage] = numEntriesPerPage

  def getWindowSize(self) -> QtCore.QSize | None:
    if kWindowSize in self.prefsMap and len(self.prefsMap[kWindowSize]):
      width, height = self.prefsMap[kWindowSize].split(',')
      return QtCore.QSize(int(width), int(height))

    return None

  def setWindowSize(self, size: QtCore.QSize):
    self.prefsMap[kWindowSize] = f'{size.width()},{size.height()}'

  def getWindowPos(self) -> QtCore.QPoint | None:
    if kWindowPos in self.prefsMap and len(self.prefsMap[kWindowPos]):
      x, y = self.prefsMap[kWindowPos].split(',')
      return QtCore.QPoint(int(x), int(y))

    return None

  def setWindowPos(self, pos: QtCore.QPoint):
    self.prefsMap[kWindowPos] = f'{pos.x()},{pos.y()}'
