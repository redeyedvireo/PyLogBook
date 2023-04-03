from PyQt5 import QtCore
import os.path
import time
import datetime
from datetime import timezone

def julianDayToDate(julianDay: int) -> datetime.date:
  """ Returns a Python date corresponding to the given Julian day. """
  qtDate = QtCore.QDate.fromJulianDay(julianDay)
  date = qtDate.toPyDate()
  return date

def dateToJulianDay(inDate: datetime.date) -> int:
  """ Returns a Julian day for the given Python date. """
  qtDate = QtCore.QDate(inDate.year, inDate.month, inDate.day)    # TODO: Python days and months start with 1.  Same true of QDate?
  return qtDate.toJulianDay()

def formatDateTime(inDateTime: datetime.datetime) -> str:
  return inDateTime.strftime("%B %d, %Y %I:%M %p")

# Format date for the Log Entry Tree
def formatDate(inDate: datetime.date) -> str:
  return inDate.strftime("%a %b %d %Y")

# Take a date string formatted for the Log Entry Tree, and convert it to a date
def dateFromFormattedString(dateStr: str) -> datetime.date:
  thisDateTime = datetime.datetime.strptime(dateStr, "%a %b %d %Y")
  return thisDateTime.date()

def bytesToQByteArray(data: bytes) -> QtCore.QByteArray:
  return QtCore.QByteArray(data)

def qByteArrayToBytes(data: QtCore.QByteArray) -> bytes:
  return bytes(data, 'utf-8')
