from PyQt5 import uic, QtCore, QtGui, QtWidgets


class CCalendar(QtWidgets.QCalendarWidget):
  def __init__(self, parent):
    super(CCalendar, self).__init__(parent)

  def clear(self):
    # TODO: Implement
    pass

  def setLogDates(self, dateList):
    # TODO: Implement
    pass