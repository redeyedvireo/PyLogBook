
from typing import TypedDict

from styleDef import StyleDef


class StyleManager:
  def __init__(self) -> None:
    self.styles = { }

  def applyStyle(self):
    # TODO: Implement
    print('Implement applyStyle')

  def getStyleIds(self) -> list[int]:
    # TODO: Implement
    print('Implement getStyleIds')
    return []

  def getStyle(self, styleId) -> StyleDef:
    # TODO: Implement
    return StyleDef()

  def addStyle(self, styleDef: StyleDef) -> int:
    # TODO: Implement
    return 0
