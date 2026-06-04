"""
Abstract memory interface — swap SessionMemoryStore for DatabaseMemoryStore later.
"""
from abc import ABC, abstractmethod

from .schemas import SessionMemory


class MemoryStore(ABC):
    @abstractmethod
    def load(self, session_key: str) -> SessionMemory:
        ...

    @abstractmethod
    def save(self, memory: SessionMemory) -> None:
        ...
