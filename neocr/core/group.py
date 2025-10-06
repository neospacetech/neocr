from typing import List, Literal, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .symbol import Symbol
    from .document import Document
    
class Group:
    """
    Collection of Symbols after recognition.
    Represents a logical grouping like a word, formula cell, or table cell.
    """
    def __init__(self, structure: Union[Literal["horizontal", "vertical", "grid", "formula", "table"], None] = None):
        self.children: List[Union["Symbol", Group]] = []
        self.structure: Union[Literal["horizontal", "vertical", "grid", "formula", "table"], None] = structure
        self.parent: Union[Document, Group, None] = None

    def add_child(self, entity: Union["Symbol", "Group"]):
        entity.parent = self
        self.children.append(entity)

    def to_dict(self):
        return {
            "children": [c.to_dict() for c in self.children],
            "structure": self.structure
        }

    @classmethod
    def from_dict(cls, data):
        from .symbol import Symbol
        group = cls()
        children = [
            Symbol.from_dict(child) if 'value' in child else Group.from_dict(child) 
            for child in data.get("children", [])
        ]
        for c in children:
            group.add_child(c)

        return group

    def __repr__(self):
        return f"<Group children={len(self.children)}>"