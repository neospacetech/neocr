from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .group import Group


class Delimiter:
    """
    Represents a delimiter symbol, such as space, line break, or tab.
    """
    def __init__(self, value=None, confidence=None):
        self.value = value
        self.confidence = confidence
        self.parent: Optional[Group] = None

    def to_dict(self):
        return {
            "value": self.value,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            value=data.get("value"),
            confidence=data.get("confidence"),
        )

    def __repr__(self):
        return f"<Delimiter value={self.value} confidence={self.confidence}>"