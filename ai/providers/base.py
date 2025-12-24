from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_answer(self, question: str, context: str) -> str:
        """Generate an answer given a question and context."""
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        """Generate an embedding vector for the given text."""
        pass
