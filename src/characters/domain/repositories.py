from abc import ABC, abstractmethod

from src.characters.domain.models import Character

class CharacterRepository(ABC):
    @abstractmethod
    def all(self)-> list[Character]:...
    
    @abstractmethod
    def get_by_id(self, id: int) -> Character | None:...
    
    @abstractmethod
    def save(self, character: Character) -> Character:...
    
    @abstractmethod
    def update(self, id: int, character: Character) -> Character | None:...
    
    @abstractmethod
    def delete(self, id: int) -> bool:...