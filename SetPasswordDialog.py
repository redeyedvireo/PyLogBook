from PySide6 import QtCore, QtWidgets
from ui_SetPasswordDialog import Ui_SetPasswordDlg

class SetPasswordDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    super(SetPasswordDialog, self).__init__(parent)

    self.ui = Ui_SetPasswordDlg()
    self.ui.setupUi(self)

    # Disable the OK button until a password is entered
    self.updateOkButtonEnableState()
    self.updatePasswordMatchLabel()

    self.ui.noPasswordButton.clicked.connect(self.onNoPasswordClicked)
    self.ui.buttonBox.accepted.connect(self.onOkClicked)
    self.ui.passwordEdit.textEdited.connect(self.onPasswordEdited)
    self.ui.reEnterPasswordEdit.textEdited.connect(self.onPasswordEdited)

  def onPasswordEdited(self):
    self.updateOkButtonEnableState()
    self.updatePasswordMatchLabel()

  def onNoPasswordClicked(self):
    self.ui.passwordEdit.clear()
    self.ui.reEnterPasswordEdit.clear()
    self.accept()

  def getPassword(self):
    return self.ui.passwordEdit.text()

  def updateOkButtonEnableState(self):
    """Sets the enabled state of the OK button.  If the passwords match, the OK button is enabled.  Otherwise, it is disabled.
    """
    enableOkButton = False

    if len(self.ui.passwordEdit.text()) > 0:
      # If passwords match, set the OK button to enabled
      enableOkButton = True if self.ui.passwordEdit.text() == self.ui.reEnterPasswordEdit.text() else False
    else:
      # If no password is entered, enable the OK button (ie, the notebook will not be encrypted)
      enableOkButton = True

    okButton = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
    okButton.setEnabled(enableOkButton)

  def updatePasswordMatchLabel(self):
    """Updates the password match label.  If the passwords match, the label is hidden.  Otherwise, it is shown.
    """
    if self.ui.passwordEdit.text() == self.ui.reEnterPasswordEdit.text() or len(self.ui.passwordEdit.text()) == 0:
      self.ui.passwordsNotMatchLabel.hide()
    else:
      self.ui.passwordsNotMatchLabel.show()

  def onOkClicked(self):
    # Verify that the two passwords match
    if self.ui.passwordEdit.text() == self.ui.reEnterPasswordEdit.text():
      self.accept()
      return
    else:
      QtWidgets.QMessageBox.critical(self, "Password Mismatch", "The passwords don't match.")
