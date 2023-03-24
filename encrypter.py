import hashlib

class Encrypter():
  def __init__(self) -> None:
    self.plainTextPassword = ''

  def setPassword(self, plainTextPassword):
    self.plainTextPassword = plainTextPassword

  def clear(self):
    self.plainTextPassword = ''

  def hashedPassword(self):
    if len(self.plainTextPassword) > 0:
      m = hashlib.sha256()
      passwordAsBytes = self.plainTextPassword.encode('utf8')
      m.update(passwordAsBytes)
      return m.hexdigest()
    else:
      return None
