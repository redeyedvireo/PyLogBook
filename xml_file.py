from PySide6 import QtCore, QtGui, QtWidgets
import datetime
import logging
import xml.etree.ElementTree as ET
from database import Database
from log_entry import LogEntry

from utility import dateToJulianDay, formatDate, formatDateTime, julianDayToDate

from constants import kLogEntryRoot, kLogEntry, kLogEntryId, kNumModifications, kLastModifiedDateTime, kTags, kLogEntryData

class XmlHandler(QtCore.QObject):
  def __init__(self, db: Database) -> None:
    self.db = db
    self.importCanceled = False
    self.exportCanceled = False

  def importLogFile(self, xmlLogFilePath) -> tuple[bool, list[int], datetime.date, datetime.date]:
    tree = ET.parse(xmlLogFilePath)
    root = tree.getroot()

    numEntries = len(root)

    entryIds: list[int] = []
    earliestEntry = 0
    latestEntry = 0
    numEntriesImported = 0
    self.importCanceled = False

    progressDialog = QtWidgets.QProgressDialog("Importing logs...", "Cancel", 0, numEntries)
    progressDialog.setWindowTitle("Log Import")
    progressDialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
    progressDialog.setMinimum(0)
    progressDialog.setMaximum(numEntries)
    progressDialog.setValue(0)

    progressDialog.canceled.connect(self.onImportCanceled)

    for child in root:
      QtWidgets.QApplication.processEvents()

      if not self.importCanceled:
        progressDialog.setValue(numEntriesImported)
        entryIdOrNone = self.readLogEntry(child)

        if entryIdOrNone is not None:
          entryIds.append(entryIdOrNone)
          earliestEntry = entryIdOrNone if earliestEntry == 0 else min(entryIdOrNone, earliestEntry)
          latestEntry = max(entryIdOrNone, latestEntry)
        else:
          logging.error(f'[importLogFile] Error reading log entry')

        numEntriesImported += 1
        progressDialog.setLabelText(f'Imported {numEntriesImported} of {numEntries}')
      else:
        # Import canceled
        # TODO: Use a SQL Transaction:
        # https://www.sqlite.org/lang_transaction.html
        # self.db.rollback()
        return (True, entryIds, julianDayToDate(earliestEntry), julianDayToDate(latestEntry))

    return (True, entryIds, julianDayToDate(earliestEntry), julianDayToDate(latestEntry))

  @QtCore.Slot()
  def onImportCanceled(self):
    logging.info('Import canceled')

    self.importCanceled = True

  def readLogEntry(self, logEntryElement) -> int | None:
    entryId = int(logEntryElement.attrib[kLogEntryId])
    entryDate = julianDayToDate(entryId)
    numModifications = int(logEntryElement.attrib[kNumModifications])
    lastModifiedDateTimeTimestamp = int(logEntryElement.attrib[kLastModifiedDateTime])
    lastModifiedDateTime = datetime.datetime.fromtimestamp(lastModifiedDateTimeTimestamp)

    # print(f'Entry ID: {entryId} ({formatDate(entryDate)}), Num modifications: {numModifications}, Last modified datetime: {formatDateTime(lastModifiedDateTime)}')

    tagsElement = logEntryElement[0]
    tags = tagsElement.text if tagsElement.text is not None else ''

    entryData = logEntryElement[1].text

    # TODO: Deal with timezone.  Should this be converted to UTC?
    logEntry = LogEntry.fromData(0, entryData, tags, lastModifiedDateTime)

    returnedEntryIdOrNone = self.db.addNewLog(entryDate, logEntry)

    return returnedEntryIdOrNone

  def exportLogFile(self, xmlPath: str) -> tuple[bool, int]:
    """
    Exports all log entries

    Args:
      xmlPath (str): Path to save the exported XML file.

    Returns:
      tuple[bool, int]: A tuple containing a boolean indicating success or failure, and the number of entries exported.
    """
    self.exportCanceled = False

    logEntryDates = self.db.getEntryDates()

    numEntries = len(logEntryDates)

    numEntriesExported = 0

    progressDialog = QtWidgets.QProgressDialog("Exporting logs...", "Cancel", 0, numEntries)
    progressDialog.setWindowTitle("Log Export")
    progressDialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
    progressDialog.setMinimum(0)
    progressDialog.setMaximum(numEntries)
    progressDialog.setValue(numEntriesExported)

    progressDialog.canceled.connect(self.onExportCanceled)

    root = ET.Element(kLogEntryRoot)

    for logEntryDate in logEntryDates:
      QtWidgets.QApplication.processEvents()

      logEntry = self.db.getLogEntry(dateToJulianDay(logEntryDate))

      if logEntry is not None:
        self.addLogEntryToDom(root, logEntry)
      else:
        logging.error(f'[exportLogFile] Error retrieving log from {logEntryDate}')

      numEntriesExported += 1
      progressDialog.setValue(numEntriesExported)
      progressDialog.setLabelText(f'Exported {numEntriesExported} of {numEntries}')

    elementTree = ET.ElementTree(root)

    # Write XML to disk
    try:
      elementTree.write(xmlPath, encoding='utf-8')
    except Exception as inst:
      logging.error(f'[exportLogFile] Exception: type: {type(inst)}')
      logging.error(f'[exportLogFile] Exception args: {inst.args}')
      logging.error(f'[exportLogFile] Exception object: {inst}')
      return (False, 0)

    return (True, numEntriesExported)

  def onExportCanceled(self):
    logging.info('Export canceled')
    self.exportCanceled = True

  def addLogEntryToDom(self, domRoot: ET.Element, logEntry: LogEntry):
    logEntryRoot = ET.SubElement(domRoot, kLogEntry)

    logEntryRoot.set(kLogEntryId, str(logEntry.entryId))
    logEntryRoot.set(kNumModifications, str(logEntry.numModifications))
    lastModifiedTimestamp = logEntry.lastModifiedDateTimeAsTimestamp() \
                            if logEntry.lastModifiedDateTimeAsTimestamp() is not None else 0
    logEntryRoot.set(kLastModifiedDateTime, str(lastModifiedTimestamp))

    tagsElement = ET.SubElement(logEntryRoot, kTags)
    tagsElement.text = logEntry.tagsAsString()

    logEntryDataElement = ET.SubElement(logEntryRoot, kLogEntryData)
    logEntryDataElement.text = logEntry.content