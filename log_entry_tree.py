from PyQt5 import uic, QtCore, QtGui, QtWidgets
import datetime

class CLogEntryTree(QtWidgets.QTreeWidget):
  def __init__(self, parent):
    super(CLogEntryTree, self).__init__(parent)
    print('LogEntryTree created.')

  def setLogDates(self, dateList):
    # TODO: Implement
    pass

  def makeTemporaryEntryPermanent(self, date, entryId):
    # TODO: Implement
    pass

  def setCurrentDate(self, date: datetime.date):
    # TODO: Implement
    pass
