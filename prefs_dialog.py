from PySide6 import QtCore, QtGui, QtWidgets
from ui_prefs_dialog import Ui_PrefsDialog

from preferences import Preferences

from constants import kStartupLoadPreviousLog, \
                      kStartupEmptyWorkspace

class PrefsDialog(QtWidgets.QDialog):
  def __init__(self, parent, prefs: Preferences):
    super(PrefsDialog, self).__init__(parent)

    self.ui = Ui_PrefsDialog()
    self.ui.setupUi(self)

    self.accepted.connect(self.onAccept)

    self.prefs = prefs
    self.ui.listWidget.setCurrentRow(0)

    # Populate widgets with pref data

    if self.prefs.getStartupAction() == kStartupEmptyWorkspace:
      self.ui.emptyWorkspaceRadio.setChecked(True)
    else:
      self.ui.loadPreviousLogRadio.setChecked(True)

    self.ui.defaultTextSizeSpin.setValue(self.prefs.editorDefaultFontSize)

    tempFont = QtGui.QFont()
    tempFont.setFamily(self.prefs.editorDefaultFontFamily)

    self.ui.logsPerPageSpin.setValue(self.prefs.getNumEntriesPerPage())

  def onAccept(self):
    if self.ui.emptyWorkspaceRadio.isChecked():
      self.prefs.setStartupAction(kStartupEmptyWorkspace)
    else:
      self.prefs.setStartupAction(kStartupLoadPreviousLog)

    self.prefs.editorDefaultFontSize = self.ui.defaultTextSizeSpin.value()

    currentFont = self.ui.defaultFontCombo.currentFont()
    self.prefs.editorDefaultFontFamily = currentFont.family()

    self.prefs.setNumEntriesPerPage(self.ui.logsPerPageSpin.value())
