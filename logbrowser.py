from PyQt5 import uic, QtCore, QtGui, QtWidgets
import datetime

class LogBrowser(QtWidgets.QWidget):
  def __init__(self, parent):
    super(LogBrowser, self).__init__(parent)

  def clear(self):
    # TODO: Implement
    pass

  def addDate(self, date: datetime.date):
    # TODO: Implement
    pass

  def scrollToItem(self, inDate: datetime.date) -> None:
    # TODO: Implement
    pass
