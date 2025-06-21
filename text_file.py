from io import TextIOWrapper
from PySide6 import QtCore, QtWidgets
import logging

from database import Database
from log_entry import LogEntry
from utility import dateToJulianDay

class TextHandler(QtCore.QObject):
  def __init__(self, db: Database) -> None:
    self.db = db
    self.exportCanceled = False

  def exportLogFile(self, textFilePath: str):
    """
    Exports all log entries to a text file.

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


    try:
      with open(textFilePath, 'w', encoding='utf-8') as file:
        for logEntryDate in logEntryDates:
          QtWidgets.QApplication.processEvents()

          logEntry = self.db.getLogEntry(dateToJulianDay(logEntryDate))

          if logEntry is not None:
            self.addLogEntryToFile(file, logEntry)
          else:
            logging.error(f'[exportLogFile] Error retrieving log from {logEntryDate}')

          numEntriesExported += 1
          progressDialog.setValue(numEntriesExported)
          progressDialog.setLabelText(f'Exported {numEntriesExported} of {numEntries}')

    except Exception as e:
      QtWidgets.QMessageBox.critical(None, "Export Error", f"Failed to export log entries: {str(e)}") # type: ignore
      return (False, 0)

    return (True, numEntriesExported)

  def onExportCanceled(self):
    self.exportCanceled = True
    logging.info('Export canceled')
    QtWidgets.QMessageBox.information(None, "Export Canceled", "The export operation has been canceled.") # type: ignore

  def addLogEntryToFile(self, file: TextIOWrapper, logEntry: LogEntry):
    # Exporting as text isn't meant to be re-importable, so just write out the date and content as plain text.
    file.write(f"Date: {logEntry.entryDateAsString()}\n")
    file.write(f"{logEntry.contentAsPlainText}\n\n")