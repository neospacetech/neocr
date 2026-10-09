class BaseRecognizer:
    def recognize(self, image) -> tuple[str, float]:
        raise NotImplementedError("Base recognizer does not implement recognition.")

class Recognizer(BaseRecognizer):
    def recognize(self, image) -> tuple[str, float]:
        raise NotImplementedError("Character recognition not implemented.")
    
class FastRecognizer(BaseRecognizer):
    def recognize(self, image) -> tuple[str, float]:
        raise NotImplementedError("Fast character recognition not implemented.")