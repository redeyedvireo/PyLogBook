import typing
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

class CCalendar(QtWidgets.QCalendarWidget):
  dateSelectedSignal = QtCore.pyqtSignal(datetime.date)

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

  def setCurrentDate(self, date: datetime.date):
    qtDate = QtCore.QDate(date.year, date.month, date.day)
    self.setSelectedDate(qtDate)

  def paintCell(self, painter: QtGui.QPainter, rect: QtCore.QRect, date: typing.Union[QtCore.QDate, datetime.date]) -> None:
    theDate = None
    if isinstance(date, datetime.date):
      theDate = date
    elif isinstance(date, QtCore.QDate):
      theDate = date.toPyDate()

    if theDate is not None and self.hasLogEntry(theDate):
      painter.fillRect(rect, QtCore.Qt.GlobalColor.yellow)
      painter.save()
      painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, f'{theDate.day}')
      painter.restore()
    else:
      return super().paintCell(painter, rect, date)

  def hasLogEntry(self, date: datetime.date) -> bool:
    return date in self.logDates

  @QtCore.pyqtSlot(QtCore.QDate)
  def onDateClicked(self, qtDate: QtCore.QDate):
    date = qtDate.toPyDate()
    print(f'Date clicked: {date}')
    self.dateSelectedSignal.emit(date)
