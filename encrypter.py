import hashlib

class Encrypter():
  def __init__(self, plainTextPassword) -> None:
    self.plainTextPassword = plainTextPassword

  def hashedPassword(self):
    m = hashlib.sha256()
    passwordAsBytes = self.plainTextPassword.encode('utf8')
    m.update(passwordAsBytes)
    return m.hexdigest()
