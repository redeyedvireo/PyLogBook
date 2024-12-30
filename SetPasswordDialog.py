from PySide6 import QtCore, QtWidgets
from ui_SetPasswordDialog import Ui_SetPasswordDlg

class SetPasswordDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    super(SetPasswordDialog, self).__init__(parent)

    self.ui = Ui_SetPasswordDlg()
    self.ui.setupUi(self)

    self.ui.noPasswordButton.clicked.connect(self.onNoPasswordClicked)
    self.ui.buttonBox.accepted.connect(self.onOkClicked)

  def onNoPasswordClicked(self):
    self.ui.passwordEdit.clear()
    self.ui.reEnterPasswordEdit.clear()
    self.accept()

  def getPassword(self):
    return self.ui.passwordEdit.text()

  def onOkClicked(self):
    # Verify that the two passwords match
    if self.ui.passwordEdit.text() == self.ui.reEnterPasswordEdit.text():
      self.accept()
      return
    else:
      QtWidgets.QMessageBox.critical(self, "Password Mismatch", "The passwords don't match.")
