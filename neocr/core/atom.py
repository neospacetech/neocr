from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .document import Document
    from .symbol import Symbol
    from ..model import BaseRecognizer

class Atom:
    """
    Smallest indivisible unit detected in deconstruction.
    Represents a raw image/stroke fragment before recognition.
    """
    def __init__(self, bbox: Optional[tuple] = None, document: Optional["Document"] = None):
        self.bbox = bbox
        self.document = document

    def to_dict(self):
        return {
            "bbox": self.bbox
        }
        
    def recognize(self, recognizer: "BaseRecognizer") -> "Symbol":
        from .symbol import Symbol
        
        if self.document is None:
            raise ValueError("Atom must be linked to a Document for recognition.")
        
        image = self.document.get_image(self.bbox)
        if image is None:
            raise ValueError("Atom has no associated image for recognition.")
        
        value, confidence = recognizer.recognize(image)
        return Symbol(value=value, confidence=confidence)

    @classmethod
    def from_dict(cls, data):
        return cls(bbox=data.get("bbox"), document=data.get("document"))

    def __repr__(self):
        return f"<Atom bbox={self.bbox} document={self.document}>"
