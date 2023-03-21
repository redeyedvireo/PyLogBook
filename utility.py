from PyQt5 import QtCore
import os.path
import time
from datetime import timezone

def julianDayToDate(julianDay):
    """ Returns a Python date corresponding to the given Julian day. """
    qtDate = QtCore.QDate.fromJulianDay(julianDay)
    date = qtDate.toPyDate()
    return date

def dateToJulianDay(inDate):
    """ Returns a Julian day for the given Python date. """
    qtDate = QtCore.QDate(inDate.year, inDate.month, inDate.day)    # TODO: Python days and months start with 1.  Same true of QDate?
    return qtDate.toJulianDay()