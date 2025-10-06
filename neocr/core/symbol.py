from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .group import Group
    from .document import Document

class Symbol:
    """
    Recognized unit created after OCR on atoms.
    Holds semantic value and links to underlying atoms.
    """
    def __init__(self, value=None, confidence=None):
        self.value = value
        self.confidence = confidence
        self.parent: Optional[Group] = None

    def to_dict(self):
        return {
            "value": self.value,
            "confidence": self.confidence
        }

    @classmethod
    def from_dict(cls, data):
        return cls(value=data.get("value"), confidence=data.get("confidence"))

    def __repr__(self):
        return f"<Symbol '{self.value}' conf={self.confidence}>"
