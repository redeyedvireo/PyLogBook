import configparser
import logging
import os.path
from pathlib import Path

from constants import kStartupLoadPreviousLog, \
                      kStartupEmptyWorkspace, \
                      kGeneralStartupLoad, \
                      kEditorDefaultTextSize, \
                      kBrowserLogsPerPage, \
                      kEditorDefaultFontFamily

class Preferences():
  def __init__(self, prefsFilePath) -> None:
    self.prefsFilePath = prefsFilePath

    # Default prefs
    self.prefsMap = {
      kGeneralStartupLoad: kStartupLoadPreviousLog,
      kEditorDefaultTextSize: 10,
      kEditorDefaultFontFamily: 'Arial',
      kBrowserLogsPerPage: 5
    }

  def readPrefsFile(self):
    """ Reads the prefs from the prefs INI file. """
    configObj = configparser.ConfigParser()

    if not os.path.exists(self.prefsFilePath):
      # The prefs file does not exist.  Create it with app defaults
      self.writePrefsFile()
    else:
      try:
        configObj.read(self.prefsFilePath)

        self.prefsMap[kGeneralStartupLoad] = configObj['general']['startupload']
        self.prefsMap[kEditorDefaultTextSize] = int(configObj['editor']['defaulttextsize'])
        self.prefsMap[kBrowserLogsPerPage] = int(configObj['browser']['logsperpage'])
        self.prefsMap[kEditorDefaultFontFamily] = configObj['browser']['defaultfontfamily']

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

  def setStartupAction(self, action: str):
    if action == kStartupEmptyWorkspace:
      self.prefsMap[kGeneralStartupLoad] = kStartupEmptyWorkspace
    else:
      self.prefsMap[kGeneralStartupLoad] = kStartupLoadPreviousLog

  def getEditorDefaultFontSize(self) -> int:
    return self.prefsMap[kEditorDefaultTextSize]

  def setEditorDefaultFontSize(self, fontSize: int):
    self.prefsMap[kEditorDefaultTextSize] = fontSize

  def getEditorDefaultFontFamily(self) -> str:
    return self.prefsMap[kEditorDefaultFontFamily]

  def setEditorDefaultFontFamily(self, fontFamily: str):
    self.prefsMap[kEditorDefaultFontFamily] = fontFamily

  def getNumEntriesPerPage(self) -> int:
    return self.prefsMap[kBrowserLogsPerPage]

  def setNumEntriesPerPage(self, numEntriesPerPage: int):
    self.prefsMap[kBrowserLogsPerPage] = numEntriesPerPage