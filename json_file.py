from PySide6 import QtCore, QtWidgets
import logging
import json
from io import TextIOWrapper

from database import Database
from log_entry import LogEntry
from utility import dateToJulianDay

class JsonHandler(QtCore.QObject):
  def __init__(self, db: Database) -> None:
    super().__init__()
    self.db = db
    self.exportCanceled = False

  def exportLogFile(self, jsonFilePath: str):
    """
    Exports all log entries to a JSON file.

    Args:
      jsonFilePath (str): Path to save the exported JSON file.

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


    try:
      # First, create JSON blocks for each log entry
      jsonBlocks = []

      for logEntryDate in logEntryDates:
        QtWidgets.QApplication.processEvents()

        logEntry = self.db.getLogEntry(dateToJulianDay(logEntryDate))

        if logEntry is not None:
          jsonBlocks.append({
            "date": logEntry.entryDateAsString(),
            "last_modified": logEntry.lastModifiedDateTimeAsTimestamp(),
            "tags": logEntry.tagsAsString(),
            "content": logEntry.contentAsPlainText
          })
        else:
          logging.error(f'[JsonHandler.exportLogFile] Error retrieving log from {logEntryDate}')

        numEntriesExported += 1
        progressDialog.setValue(numEntriesExported)
        progressDialog.setLabelText(f'Exported {numEntriesExported} of {numEntries}')

      with open(jsonFilePath, 'w', encoding='utf-8') as file:
        json.dump(jsonBlocks, file)
        file.write("\n")

    except Exception as e:
      QtWidgets.QMessageBox.critical(None, "Export Error", f"Failed to export log entries: {str(e)}") # type: ignore
      return (False, 0)

    return (True, numEntriesExported)

  def onExportCanceled(self):
    self.exportCanceled = True
    logging.info('Export canceled')
    QtWidgets.QMessageBox.information(None, "Export Canceled", "The export operation has been canceled.") # type: ignore

  # def addLogEntryToFile(self, file: TextIOWrapper, logEntry: LogEntry):
  #   entry_dict = {
  #     "date": logEntry.entryDateAsString(),
  #     "last_modified": logEntry.lastModifiedDateTimeAsTimestamp(),
  #     "tags": logEntry.tagsAsString(),
  #     "content": logEntry.contentAsPlainText
  #   }
  #   json.dump(entry_dict, file)
  #   file.write("\n")