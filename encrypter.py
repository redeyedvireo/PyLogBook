import hashlib
import base64
import os
import logging
import cryptography
from cryptography.fernet import Fernet
import cryptography.fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encrypter():
  def __init__(self) -> None:
    self.plainTextPassword = ''
    self.salt = b''
    self.fernet = None

  def hasPassword(self) -> bool:
    return len(self.plainTextPassword) > 0

  def setPasswordAndSalt(self, plainTextPassword: str, salt: bytes) -> None:
    self.plainTextPassword = plainTextPassword
    self.salt = salt
    self.fernet = self.createFernet()

  def setPasswordGenerateSalt(self, plainTextPassword: str) -> None:
    self.plainTextPassword = plainTextPassword
    self.salt = os.urandom(16)
    self.fernet = self.createFernet()

  def clear(self):
    self.plainTextPassword = ''
    self.salt = b''

  def hashedPassword(self):
    return self.hashValue(self.plainTextPassword) if len(self.plainTextPassword) > 0 else None

  def hashValue(self, value: str) -> str:
    m = hashlib.sha256()
    valueAsBytes = value.encode('utf8')
    m.update(valueAsBytes)
    return m.hexdigest()

  def createFernet(self) -> Fernet | None:
    """ Creates a Fernet object, which is used to encrypt and decrypt messages.
        The password and salt must exist when calling this function.
    """
    if len(self.salt) == 0 or len(self.plainTextPassword) == 0:
      return None

    passwordBytes = bytes(self.plainTextPassword, 'utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=self.salt,
        iterations=480000)

    key = base64.urlsafe_b64encode(kdf.derive(passwordBytes))
    return Fernet(key)

  def encrypt(self, contents: str) -> bytes:
    if len(self.salt) == 0 or len(self.plainTextPassword) == 0:
      return b''

    if self.fernet is None:
      raise Exception('Encrypt: fernet not initialized.')

    contentsBytes = bytes(contents, 'utf-8')
    encryptedContents = self.fernet.encrypt(contentsBytes)

    return encryptedContents

  def decrypt(self, encryptedContents: bytes) -> str:
    if self.fernet is None:
      raise Exception('Decrypt: fernet not initialized.')

    try:
      decryptedContentsBytes = self.fernet.decrypt(encryptedContents)
      decryptedContentsStr = decryptedContentsBytes.decode()

    except TypeError as e:
      logging.error(f'[Encrypter.decrypt] Decryption error: {e}')
      return ''
    except cryptography.fernet.InvalidToken as e:
      logging.error(f'[Encrypter.decrypt] Invalid token: {e}')
      return ''

    return decryptedContentsStr
