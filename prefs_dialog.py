from PyQt5 import uic, QtCore, QtGui, QtWidgets

from preferences import Preferences

from constants import kStartupLoadPreviousLog, \
                      kStartupEmptyWorkspace

class PrefsDialog(QtWidgets.QDialog):
  def __init__(self, parent, prefs: Preferences):
    super(PrefsDialog, self).__init__(parent)
    uic.loadUi('prefs_dialog.ui', self)

    self.accepted.connect(self.onAccept)

    self.prefs = prefs
    self.listWidget.setCurrentRow(0)

    # Populate widgets with pref data

    if self.prefs.getStartupAction() == kStartupEmptyWorkspace:
      self.emptyWorkspaceRadio.setChecked(True)
    else:
      self.loadPreviousLogRadio.setChecked(True)

    self.defaultTextSizeSpin.setValue(self.prefs.getEditorDefaultFontSize())

    tempFont = QtGui.QFont()
    tempFont.setFamily(self.prefs.getEditorDefaultFontFamily())

    self.logsPerPageSpin.setValue(self.prefs.getNumEntriesPerPage())

  def onAccept(self):
    if self.emptyWorkspaceRadio.isChecked():
      self.prefs.setStartupAction(kStartupEmptyWorkspace)
    else:
      self.prefs.setStartupAction(kStartupLoadPreviousLog)

    self.prefs.setEditorDefaultFontSize(self.defaultTextSizeSpin.value())

    currentFont = self.defaultFontCombo.currentFont()
    self.prefs.setEditorDefaultFontFamily(currentFont.family())

    self.prefs.setNumEntriesPerPage(self.logsPerPageSpin.value())
