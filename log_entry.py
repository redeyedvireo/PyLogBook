from PySide6 import QtGui
from constants import kTempItemId
import datetime
import time

from utility import formatDateTime, julianDayToDate

class LogEntry():
  def __init__(self) -> None:
    self.entryId = kTempItemId    # This is the Julian day corresponding to the entry's date
    self.content: str = ''
    self.tags = []
    self.lastModifiedDateTime: datetime.datetime | None = None
    self.numModifications = 0

  def isEntryIdValid(self) -> bool:
    return self.entryId > 0

  def setTagsFromString(self, tagsString: str) -> None:
    self.tags = tagsString.split(',')

  def tagsAsString(self) -> str:
    return ','.join(self.tags)

  def lastModifiedDateAsFormattedString(self) -> str:
    if self.lastModifiedDateTime is not None:
      return formatDateTime(self.lastModifiedDateTime)
    else:
      return ''

  def lastModifiedDateTimeAsTimestamp(self) -> int | None:
    if self.lastModifiedDateTime is not None:
      return int(time.mktime(self.lastModifiedDateTime.timetuple()))
    else:
      return None

  def entryDate(self) -> datetime.date | None:
    if self.isEntryIdValid():
      return julianDayToDate(self.entryId)
    else:
      return None

  def entryDateAsString(self) -> str:
    if self.isEntryIdValid():
      date = julianDayToDate(self.entryId)
      return date.strftime('%B %d, %Y') if date is not None else ''
    else:
      return ''

  def containsString(self, searchString: str) -> bool:
    searchString = searchString.lower()

    textDoc = QtGui.QTextDocument()
    textDoc.setHtml(self.content)
    textContents = textDoc.toPlainText().lower()

    return searchString in textContents or searchString in self.tagsAsString().lower()

  def numModificationsAsString(self) -> str:
    return str(self.numModifications)

  def incrementNumModifications(self) -> None:
    self.numModifications += 1

  def updateLastModificationDateTime(self) -> None:
    self.lastModifiedDateTime = datetime.datetime.now(datetime.timezone.utc)

  @staticmethod
  def fromData(entryId: int, content: str, tags: str, lastModificationDateTime: datetime.datetime):
    logEntry = LogEntry()

    logEntry.entryId = entryId
    logEntry.content = content
    logEntry.setTagsFromString(tags)
    logEntry.lastModifiedDateTime = lastModificationDateTime

    return logEntry
