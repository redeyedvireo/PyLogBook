from PyQt5 import uic, QtCore, QtGui, QtWidgets

class PrefsDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    super(PrefsDialog, self).__init__(parent)
    uic.loadUi('prefs_dialog.ui', self)