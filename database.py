import logging
from PyQt5 import QtCore, QtSql
from pathlib import Path


class Database:
  def __init__(self):
    super(Database, self).__init__()
    self.db = None

  def open(self, pathName):
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
    else:
      logging.error("Could not open database")

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