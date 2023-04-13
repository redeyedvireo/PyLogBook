import xml.etree.ElementTree as ET

class XmlHandler:
  def __init__(self, db) -> None:
    self.db = db

  def importLogFile(self, xmlLogFilePath) -> bool:
    tree = ET.parse(xmlLogFilePath)
    root = tree.getroot()

    for child in root:
      self.readLogEntry(child)
    return False

  def readLogEntry(self, logEntryElement):
    entryId = logEntryElement.attrib['LogEntryID']
    numModifications = logEntryElement.attrib['NumModifications']
    lastModifiedDateTime = logEntryElement.attrib['LastModifiedDateTime']

    print(f'Entry ID: {entryId}, Num modifications: {numModifications}, Last modified datetime: {lastModifiedDateTime}')

    tagsElement = logEntryElement[0]
    tags = tagsElement.text if tagsElement.text is not None else ''

    print(f'Tags: {tags}')

    entryData = logEntryElement[1]
    print(f'Entry data: {entryData.text}')

    # TODO: Store in database

  def exportLogFile(self, xmlPath) -> bool:
    # TODO: Implement
    return False
