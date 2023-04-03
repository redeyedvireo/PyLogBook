import configparser
import logging
import os.path
from pathlib import Path

from constants import kStartupLoadPreviousLog

class Preferences():
  def __init__(self, prefsFilePath) -> None:
    self.prefsFilePath = prefsFilePath

    # Default prefs
    self.prefsMap = {
      'general-startupload': kStartupLoadPreviousLog,
      'editor-defaulttextsize': 10,
      'browser-logsperpage': 5
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

        self.prefsMap['general-startupload'] = configObj['general']['startupload']
        self.prefsMap['editor-defaulttextsize'] = configObj['editor']['defaulttextsize']
        self.prefsMap['browser-logsperpage'] = configObj['browser']['logsperpage']

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
