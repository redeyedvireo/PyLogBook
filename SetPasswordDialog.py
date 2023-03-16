from PyQt5 import uic, QtCore, QtWidgets

class SetPasswordDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    super(SetPasswordDialog, self).__init__(parent)
    uic.loadUi('SetPasswordDialog.ui', self)

    self.noPasswordButton.clicked.connect(self.onNoPasswordClicked)
    self.buttonBox.accepted.connect(self.onOkClicked)

  def onNoPasswordClicked(self):
    self.passwordEdit.clear()
    self.reEnterPasswordEdit.clear()
    self.accept()

  def getPassword(self):
    return self.passwordEdit.text()

  def onOkClicked(self):
    # Verify that the two passwords match
    if self.passwordEdit.text() == self.reEnterPasswordEdit.text():
      self.accept()
      return
    else:
      QtWidgets.QMessageBox.critical(self, "Password Mismatch", "The passwords don't match.")
