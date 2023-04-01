import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path
import datetime

from encrypter import Encrypter
from log_entry import LogEntry
from utility import bytesToQByteArray, dateToJulianDay, julianDayToDate

from constants import kTempItemId, kHashedPwFieldName, kSaltFieldName


# Global value data type constants
kDataTypeInteger = 0
kDataTypeString = 1
kDataTypeBlob = 2

class Database:
  def __init__(self):
    super(Database, self).__init__()
    self.db = None
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

  def getGlobalValue(self, key: str) -> int | str | bytes | None:
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

      if isinstance(value, QtCore.QByteArray):
        value = bytes(value)

      return value

  def setGlobalValue(self, key: str, value: int | str | bytes):
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
      elif isinstance(value, bytes):
        createStr = "update globals set blobval=? where key=?"

        # Must convert to a QByteArray
        value = bytesToQByteArray(value)
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
      elif isinstance(value, bytes):
        createStr = "insert into globals (key, datatype, blobval) values (?, ?, ?)"
        dataType = kDataTypeBlob

        # Must convert to a QByteArray
        value = bytesToQByteArray(value)
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
    return self.globalValueExists(kHashedPwFieldName)

  def setPasswordInMemory(self, plainTextPassword) -> None:
    # First, get the salt value from the database
    salt = self.getGlobalValue(kSaltFieldName)

    if salt is not None and isinstance(salt, bytes):
      self.encrypter.setPasswordAndSalt(plainTextPassword, salt)

  def storePassword(self, plainTextPassword) -> None:
    """ Sets the password for a new log file.  The salt is generated here. """
    if len(plainTextPassword) > 0:
      self.encrypter.setPasswordGenerateSalt(plainTextPassword)
      hashedPassword = self.encrypter.hashedPassword()

      if hashedPassword is not None:
        self.setGlobalValue(kHashedPwFieldName, hashedPassword)
        self.setGlobalValue(kSaltFieldName, self.encrypter.salt)

  def passwordMatch(self, password) -> bool:
    storedHashedPassword = self.getGlobalValue(kHashedPwFieldName)

    if storedHashedPassword is not None and isinstance(storedHashedPassword, str):
      hashedPw = self.encrypter.hashValue(password)

      return storedHashedPassword == hashedPw
    else:
      logging.error(f'[passwordMatch] Error retrieving hashed password.')
      return False

  def getEntryDates(self) -> list[datetime.date]:
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
    dateList: list[datetime.date] = []

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

  def addNewLog(self, entryDate: datetime.date, logEntry: LogEntry) -> int | None:
    """ Adds a new log to the database.  Returns the entryId of the entry, or None
        if there was an error.
    """
    queryObj = QtSql.QSqlQuery(self.db)

    entryId = dateToJulianDay(entryDate)

    lastModifiedDateTimeTimestamp = logEntry.lastModifiedDateTimeAsTimestamp()

    if lastModifiedDateTimeTimestamp is None:
      lastModifiedDateTimeTimestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()

    encryptedData = b''
    encryptedTags = b''

    # If password protected, encrypt the data
    if self.encrypter.hasPassword():
      encryptedData = self.encrypter.encrypt(logEntry.content)
      encryptedTags = self.encrypter.encrypt(logEntry.tagsAsString())
    else:
      encryptedData = bytes(logEntry.content, 'utf-8')
      encryptedTags = bytes(logEntry.tagsAsString(), 'utf-8')

    # Must convert bytes to QByteArray
    encryptedData = bytesToQByteArray(encryptedData)
    encryptedTags = bytesToQByteArray(encryptedTags)

    queryStr = 'insert into logs (entryid, lastModifiedDate, numModifications, contents, tags) values (?, ?, ?, ?, ?)'

    queryObj.prepare(queryStr)

    queryObj.addBindValue(entryId)
    queryObj.addBindValue(lastModifiedDateTimeTimestamp)
    queryObj.addBindValue(1)    # Num modifications (always 1 for a new log)
    queryObj.addBindValue(encryptedData)
    queryObj.addBindValue(encryptedTags)

    queryObj.exec_()

    # Check for errors
    sqlErr = queryObj.lastError()
    if sqlErr.type() != QtSql.QSqlError.NoError:
      self.reportError("Error when attempting to store a new log entry: {}".format(sqlErr.text()))
      return None

    return entryId

  def updateLog(self, entryId: int, content: str, tags: str) -> bool:
    existingLogEntry = self.getLogEntry(entryId)

    if existingLogEntry:
      existingLogEntry.incrementNumModifications()
      existingLogEntry.updateLastModificationDateTime()
      existingLogEntry.setTagsFromString(tags)

      # If password protected, encrypt the data
      encryptedData = b''
      encryptedTags = b''

      # If password protected, encrypt the data
      if self.encrypter.hasPassword():
        encryptedData = self.encrypter.encrypt(existingLogEntry.content)
        encryptedTags = self.encrypter.encrypt(existingLogEntry.tagsAsString())
      else:
        encryptedData = bytes(existingLogEntry.content, 'utf-8')
        encryptedTags = bytes(existingLogEntry.tagsAsString(), 'utf-8')

      # Must convert bytes to QByteArray
      encryptedData = bytesToQByteArray(encryptedData)
      encryptedTags = bytesToQByteArray(encryptedTags)

      queryObj = QtSql.QSqlQuery(self.db)

      queryObj.prepare('update logs set contents=?, tags=?, lastmodifieddate=?, nummodifications=? where entryid=?')

      queryObj.addBindValue(encryptedData)
      queryObj.addBindValue(encryptedTags)
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

      logEntry = LogEntry()

      # If encrypted, decrypt the contentsData
      if self.encrypter.hasPassword():
        logEntry.content = self.encrypter.decrypt(bytes(contentData))
        logEntry.setTagsFromString(self.encrypter.decrypt(bytes(tagsData)))
      else:
        logEntry.content = contentData.decode()
        logEntry.setTagsFromString(tagsData.decode())

      logEntry.entryId = entryId
      logEntry.lastModifiedDateTime = lastModifiedDate
      logEntry.numModifications = numModifications

      return logEntry
    else:
      # No entry found
      return None