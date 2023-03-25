import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path
import datetime

from encrypter import Encrypter
from log_entry import LogEntry
from utility import dateToJulianDay, julianDayToDate

from constants import kTempItemId


# Global value data type constants
kDataTypeInteger = 0
kDataTypeString = 1
kDataTypeBlob = 2

class Database:
  def __init__(self):
    super(Database, self).__init__()
    self.db = None
    self.dbPassword = ''
    self.encrypter = Encrypter()

  def openDatabase(self, pathName) -> bool:
    self.encrypter.clear()
    return self.open(pathName)

  def open(self, pathName) -> bool:
    self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    p = Path(pathName)
    dbExists = p.is_file()

    self.db.setDatabaseName(pathName)

    if self.db.open():
      if dbExists:
        logging.info("Database open")
        self.updateDatabase()
      else:
        # Create the database, and all tables
        self.createNewDatabase()
        logging.info(f'Created new database at: {pathName}')
      return True
    else:
      logging.error("Could not open database")
      return False

  def isDatabaseOpen(self):
    if self.db is not None:
      return self.db.isOpen()
    else:
      return False

  def closeDatabase(self):
    self.close()
    self.encrypter.clear()

  def close(self):
    if self.db is not None:
      self.db.close()

  def reportError(self, errorMessage):
    logging.error(errorMessage)

  def updateDatabase(self):
    """ Updates the database to the current version. """
    # Nothing to do at this point.
    pass

  def createNewDatabase(self):
    self.createGlobalsTable()
    self.createLogsTable()

  def createGlobalsTable(self):
    """ Creates the globals table. """
    queryObj = QtSql.QSqlQuery(self.db)

    createStr = "create table globals ("
    createStr += "key text UNIQUE, "
    createStr += "datatype int, "
    createStr += "intval int, "
    createStr += "stringval text, "
    createStr += "blobval blob"
    createStr += ")"

    queryObj.prepare(createStr)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError( "Error when attempting to the globals table: {}".format(sqlErr.text()))

  def createLogsTable(self):
    """ Creates the Logs table. """
    queryObj = QtSql.QSqlQuery(self.db)

    createStr = "create table logs ("
    createStr += "entryid integer UNIQUE, "       # Unique ID - this is the Julian Day (ie, date) for which this log entry was created
    createStr += "lastmodifieddate integer, "     # time entry was last modified (Linux timestamp)
    createStr += "nummodifications integer, "     # Number of modifications made to the log entry
    createStr += "contents blob, "                # Log entry (must be blob to hold encrypted data)
    createStr += "tags blob"                      # Tags (also encrypted, so must be blob)
    createStr += ")"

    queryObj.prepare(createStr)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError( "Error when attempting to the logs table: {}".format(sqlErr.text()))

  def getGlobalValue(self, key):
    """ Returns the value of a 'global value' for the given key. """
    queryObj = QtSql.QSqlQuery(self.db)
    queryObj.prepare("select datatype from globals where key = ?")
    queryObj.bindValue(0, key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to retrieve a global value key: {}".format(sqlErr.text()))
      return None

    if queryObj.next():
      typeField = queryObj.record().indexOf("datatype")

      dataType = queryObj.value(typeField)
    else:
      # key not found
      return None

    if dataType == kDataTypeInteger:
      createStr = "select intval from globals where key=?"
    elif dataType == kDataTypeString:
      createStr = "select stringval from globals where key=?"
    elif dataType == kDataTypeBlob:
      createStr = "select blobval from globals where key=?"
    else:
      # Unknown data type
      self.reportError("getGlobalValue: unknown data type: {}".format(dataType))
      return None

    # Now that the data type is known, retrieve the data itself.
    queryObj.prepare(createStr)
    queryObj.bindValue(0, key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to retrieve a page: {}".format(sqlErr.text()))
      return None

    if queryObj.next():
      if dataType == kDataTypeInteger:
        valueField = queryObj.record().indexOf("intval")
      elif dataType == kDataTypeString:
        valueField = queryObj.record().indexOf("stringval")
      elif dataType == kDataTypeBlob:
        valueField = queryObj.record().indexOf("blobval")
      else:
        return None

      value = queryObj.value(valueField)
      return value

  def setGlobalValue(self, key, value):
    """ Sets the value of the given key to the given value. """

    # See if the key exists
    queryObj = QtSql.QSqlQuery(self.db)
    queryObj.prepare("select datatype from globals where key = ?")
    queryObj.bindValue(0, key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to determine if a global value exists: {}".format(sqlErr.text()))
      return

    if queryObj.next():
      # Key exists; update its value
      if isinstance(value, int):
        createStr = "update globals set intval=? where key=?"
      elif isinstance(value, str):
        createStr = "update globals set stringval=? where key=?"
      elif isinstance(value, QtCore.QByteArray):
        createStr = "update globals set blobval=? where key=?"
      else:
        self.reportError("setGlobalValue: invalid data type")
        return

      queryObj.prepare(createStr)

      queryObj.addBindValue(value)
      queryObj.addBindValue(key)
    else:
      if isinstance(value, int):
        createStr = "insert into globals (key, datatype, intval) values (?, ?, ?)"
        dataType = kDataTypeInteger
      elif isinstance(value, str):
        createStr = "insert into globals (key, datatype, stringval) values (?, ?, ?)"
        dataType = kDataTypeString
      elif isinstance(value, QtCore.QByteArray):
        createStr = "insert into globals (key, datatype, blobval) values (?, ?, ?)"
        dataType = kDataTypeBlob
      else:
        self.reportError("setGlobalValue: invalid data type")
        return

      queryObj.prepare(createStr)

      queryObj.addBindValue(key)
      queryObj.addBindValue(dataType)
      queryObj.addBindValue(value)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to set a global value: {}".format(sqlErr.text()))


  def globalValueExists(self, key):
    """ Checks if a global value exists. """
    queryObj = QtSql.QSqlQuery(self.db)
    queryObj.prepare("select datatype from globals where key=?")
    queryObj.addBindValue(key)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()

    if sqlErr.type() != QtSql.QSqlError.NoError:
      return False
    else:
      atLeastOne = queryObj.next()
      return atLeastOne

  def isPasswordProtected(self):
    return self.globalValueExists('hashedPw')

  def storePassword(self, plainTextPassword):
    if len(plainTextPassword) > 0:
      self.encrypter.setPassword(plainTextPassword)
      hashedPassword = self.encrypter.hashedPassword()
      self.setGlobalValue('hashedPw', hashedPassword)
      self.dbPassword = plainTextPassword

  def getLogIdForDate(self, date: datetime.date) -> int:
    return dateToJulianDay(date)

  def getLogEntryDate(self, entryId: int) -> datetime.date:
    return julianDayToDate(entryId)

  def getEntryDates(self):
    """ Returns a list of dates for which log entries exist. """
    queryObj = QtSql.QSqlQuery(self.db)
    queryStr = "select entryid from logs"
    queryObj.prepare(queryStr)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("SQLite error in GetEntryDates: {}".format(sqlErr.text()))
      return []

    entryField = queryObj.record().indexOf('entryid')
    dateList = []

    while queryObj.next():
      julianDay = int(queryObj.value(entryField))
      date = julianDayToDate(julianDay)
      dateList.append(date)

    return dateList

  def entryExistsForDate(self, date: datetime.date) -> bool:
    entryId = dateToJulianDay(date)
    return self.entryExists(entryId)

  def entryExists(self, entryId: int) -> bool:
    queryObj = QtSql.QSqlQuery(self.db)
    queryStr = "select lastmodifieddate from logs where entryid=?"
    queryObj.prepare(queryStr)
    queryObj.addBindValue(entryId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to determine if an entry exists: {}".format(sqlErr.text()))
      return False

    return queryObj.next()

  def addNewLog(self, entryDate: datetime.date, logEntry: LogEntry) -> int:
    queryObj = QtSql.QSqlQuery(self.db)

    entryId = dateToJulianDay(entryDate)

    lastModifiedDateTimeTimestamp = logEntry.lastModifiedDateTimeAsTimestamp()

    if lastModifiedDateTimeTimestamp is None:
      lastModifiedDateTimeTimestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()

    # TODO: If password protected, encrypt the data
    encryptedData = logEntry.content

    queryStr = 'insert into logs (entryid, lastModifiedDate, numModifications, contents, tags) values (?, ?, ?, ?, ?)'

    queryObj.prepare(queryStr)

    queryObj.addBindValue(entryId)
    queryObj.addBindValue(lastModifiedDateTimeTimestamp)
    queryObj.addBindValue(1)    # Num modifications (always 1 for a new log)
    queryObj.addBindValue(encryptedData)
    queryObj.addBindValue(logEntry.tagsAsString())

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to store a new log entry: {}".format(sqlErr.text()))
      return kTempItemId

    return entryId

  def updateLog(self, entryId: int, content: str, tags: str) -> bool:
    existingLogEntry = self.getLogEntry(entryId)

    if existingLogEntry:
      existingLogEntry.incrementNumModifications()
      existingLogEntry.updateLastModificationDateTime()
      existingLogEntry.setTagsFromString(tags)

      # TODO: If password protected, encrypt the data
      # TODO: This should be done through a function call that can also be called from addNewLog.
      encryptedData = content

      queryObj = QtSql.QSqlQuery(self.db)

      queryObj.prepare('update logs set contents=?, tags=?, lastmodifieddate=?, nummodifications=? where entryid=?')

      queryObj.addBindValue(encryptedData)
      queryObj.addBindValue(existingLogEntry.tagsAsString())
      queryObj.addBindValue(existingLogEntry.lastModifiedDateTimeAsTimestamp())
      queryObj.addBindValue(existingLogEntry.numModifications)
      queryObj.addBindValue(entryId)

      queryObj.exec_()

      # Check for errors
      sqlErr = queryObj.lastError()
      if sqlErr.type() != QtSql.QSqlError.NoError:
        self.reportError(f'Error when attempting to store a new log entry: {sqlErr.text()}')
        return False
      else:
        return True
    else:
      self.reportError(f'Error retrieving existing log {entryId} for updating')
      return False

  def getLogEntry(self, entryId: int) -> LogEntry | None:
    queryObj = QtSql.QSqlQuery(self.db)
    queryObj.prepare("select contents, tags, lastmodifieddate, nummodifications from logs where entryid=?")

    queryObj.addBindValue(entryId)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to retrieve a log entry: {}".format(sqlErr.text()))
      return None

    if queryObj.next():
      contentData = queryObj.record().value(0)
      tagsData = queryObj.record().value(1)
      lastModifiedDate = datetime.datetime.fromtimestamp(queryObj.record().value(2), datetime.timezone.utc)
      numModifications = queryObj.record().value(3)

      # TODO: If encrypted, decrypt the contentsData

      logEntry = LogEntry()
      logEntry.entryId = entryId
      logEntry.content = contentData
      logEntry.setTagsFromString(tagsData)
      logEntry.lastModifiedDateTime = lastModifiedDate
      logEntry.numModifications = numModifications

      return logEntry
    else:
      # No entry found
      return None