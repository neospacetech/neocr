from io import BytesIO

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .quant import Quant
    from .group import Group

class Document:
    """
    Top-level document abstraction.
    Holds either Quants (pre-recognition) or Groups/Symbols (post-recognition).
    """
    def __init__(self, data=None):
        if data is None:
            raise ValueError("Document must be initialized with data.")
        
        if isinstance(data, bytes):
            self.data = data
        elif isinstance(data, str):
            with open(data, 'rb') as f:
                self.data = f.read()
        elif isinstance(data, BytesIO):
            self.data = data.read()
        else:
            raise TypeError("Data must be bytes, file path, or BytesIO.")
        
        self.quants: List[Quant] = []
        self.groups: List[Group] = []
    
    def get_image(self, bbox):
        import cv2
        import numpy as np
        
        image = cv2.imdecode(np.frombuffer(self.data, np.uint8), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Failed to decode image data.")
        
        x, y, w, h = bbox
        return image[y:y+h, x:x+w]
    
    def recognize(self):
        if not self.quants:
            raise ValueError("No quants to recognize in the document.")
        
        self.groups = []
        for quant in self.quants:
            group = Group()
            for entity in quant.recognize():
                group.add_child(entity)
            self.groups.append(group)
    
    def to_dict(self):
        return {
            "quants": [q.to_dict() for q in self.quants],
            "data": self.data,
            "groups": [g.to_dict() for g in self.groups]
        }
        
    def decompose(self):
        raise NotImplementedError("Document decomposition not implemented.")