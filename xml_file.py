import datetime
import xml.etree.ElementTree as ET
from log_entry import LogEntry

from utility import formatDate, formatDateTime, julianDayToDate

class XmlHandler:
  def __init__(self, db) -> None:
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
    entryId = int(logEntryElement.attrib['LogEntryID'])
    entryDate = julianDayToDate(entryId)
    numModifications = int(logEntryElement.attrib['NumModifications'])
    lastModifiedDateTimeTimestamp = int(logEntryElement.attrib['LastModifiedDateTime'])
    lastModifiedDateTime = datetime.datetime.fromtimestamp(lastModifiedDateTimeTimestamp)

    # print(f'Entry ID: {entryId} ({formatDate(entryDate)}), Num modifications: {numModifications}, Last modified datetime: {formatDateTime(lastModifiedDateTime)}')

    tagsElement = logEntryElement[0]
    tags = tagsElement.text if tagsElement.text is not None else ''

    entryData = logEntryElement[1].text

    # TODO: Deal with timezone.  Should this be converted to UTC?
    logEntry = LogEntry.fromData(0, entryData, tags, lastModifiedDateTime)

    returnedEntryIdOrNone = self.db.addNewLog(entryDate, logEntry)

    return returnedEntryIdOrNone

  def exportLogFile(self, xmlPath) -> bool:
    # TODO: Implement
    return False
