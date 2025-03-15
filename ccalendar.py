import typing
from PySide6 import QtCore, QtGui, QtWidgets
import datetime
from utility import qDateToPyDate

class CCalendar(QtWidgets.QCalendarWidget):
  dateSelectedSignal = QtCore.Signal(datetime.date)

  def __init__(self, parent):
    super(CCalendar, self).__init__(parent)

    self.logDates = []

    self.clicked.connect(self.onDateClicked) # type: ignore

  def clear(self):
    # TODO: Implement
    pass

  def setLogDates(self, dateList: list[datetime.date]):
    self.logDates = dateList

  def addLogDate(self, date: datetime.date):
    if not self.hasLogEntry(date):
      self.logDates.append(date)
      self.update()

  def addLogDates(self, dates: list[datetime.date]):
    for date in dates:
      self.addLogDate(date)

  def setCurrentDate(self, date: datetime.date):
    qtDate = QtCore.QDate(date.year, date.month, date.day)
    self.setSelectedDate(qtDate)

  def paintCell(self, painter: QtGui.QPainter, rect: QtCore.QRect, date: typing.Union[QtCore.QDate, datetime.date]) -> None:
    theDate = None
    if isinstance(date, datetime.date):
      theDate = date
    elif isinstance(date, QtCore.QDate):
      theDate = qDateToPyDate(date)

    if theDate is not None and self.hasLogEntry(theDate):
      painter.fillRect(rect, QtCore.Qt.GlobalColor.yellow)
      painter.save()
      painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, f'{theDate.day}')
      painter.restore()
    else:
      return super().paintCell(painter, rect, date)

  def hasLogEntry(self, date: datetime.date) -> bool:
    return date in self.logDates

  @QtCore.Slot(QtCore.QDate)
  def onDateClicked(self, qtDate: QtCore.QDate):
    date = qDateToPyDate(qtDate)
    self.dateSelectedSignal.emit(date)
