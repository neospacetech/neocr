from ..model import FastRecognizer, Recognizer

from typing import List, Union, Literal

class Quant:
    """
    Codependent set of atoms before recognition.
    Represents a word, formula cell, or table cell.
    """
    def __init__(self, bbox=None, type_: Union[Literal["horizontal", "vertical", "grid", "formula", "table"], None] = None):
        self.bbox = bbox
        self.type = type_
        self.children = []

    def decompose(self):
        raise NotImplementedError("Quant decomposition not implemented.")
    
    def recognize(self):
        from .atom import Atom
        from .group import Group
        from .delimiter import Delimiter
        from .symbol import Symbol
        
        entities = []
        if all(isinstance(child, Atom) for child in self.children):
            try:
                text = self.text_recognition()
                for char, confidence in text:
                    symbol = Symbol(value=char, confidence=confidence)
                    entities.append(symbol)
                return entities
            except Exception as e:
                pass
        
        for child in self.children:
            if isinstance(child, Atom):
                recognizer: Recognizer = Recognizer()
                symbol = child.recognize(recognizer)
                entities.append(symbol)
            if isinstance(child, Quant):
                group = Group()
                for entity in child.recognize():
                    group.add_child(entity)
                entities.append(group)
            if isinstance(child, Delimiter):
                entities.append(child)

        return entities
    
    def text_recognition(self):
        raise NotImplementedError("Smart text recognition not implemented. Fall back to atomic recognition.")

    def to_dict(self):
        return {
            "bbox": self.bbox,
            "type": self.type,
            "children": [c.to_dict() for c in self.children]
        }

    @classmethod
    def from_dict(cls, data):
        from .atom import Atom
        atoms = [Atom.from_dict(a) for a in data.get("atoms", [])]
        quant = cls(bbox=data.get("bbox"))
        quant.children = atoms
        quant.type = data.get("type")
        return quant

    def __repr__(self):
        return f"<Quant bbox={self.bbox} children={len(self.children)} type={self.type}>"
