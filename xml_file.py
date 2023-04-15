import datetime
import logging
import xml.etree.ElementTree as ET
from database import Database
from log_entry import LogEntry

from utility import dateToJulianDay, formatDate, formatDateTime, julianDayToDate

from constants import kLogEntryRoot, kLogEntry, kLogEntryId, kNumModifications, kLastModifiedDateTime, kTags, kLogEntryData

class XmlHandler:
  def __init__(self, db: Database) -> None:
    self.db = db

  def importLogFile(self, xmlLogFilePath) -> tuple[bool, list[int], datetime.date, datetime.date]:
    tree = ET.parse(xmlLogFilePath)
    root = tree.getroot()

    entryIds: list[int] = []
    earliestEntry = 0
    latestEntry = 0

    for child in root:
      entryIdOrNone = self.readLogEntry(child)

      if entryIdOrNone is not None:
        entryIds.append(entryIdOrNone)
        earliestEntry = entryIdOrNone if earliestEntry == 0 else min(entryIdOrNone, earliestEntry)
        latestEntry = max(entryIdOrNone, latestEntry)
      else:
        return (False, entryIds, julianDayToDate(earliestEntry), julianDayToDate(latestEntry))

    return (True, entryIds, julianDayToDate(earliestEntry), julianDayToDate(latestEntry))

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

  def exportLogFile(self, xmlPath: str) -> bool:
    logEntryDates = self.db.getEntryDates()

    root = ET.Element(kLogEntryRoot)

    for logEntryDate in logEntryDates:
      logEntry = self.db.getLogEntry(dateToJulianDay(logEntryDate))

      if logEntry is not None:
        self.addLogEntryToDom(root, logEntry)

    elementTree = ET.ElementTree(root)

    try:
      elementTree.write(xmlPath, encoding='utf-8')
    except Exception as inst:
      logging.error(f'[exportLogFile] Exception: type: {type(inst)}')
      logging.error(f'[exportLogFile] Exception args: {inst.args}')
      logging.error(f'[exportLogFile] Exception object: {inst}')
      return False

    return True

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