from abc import ABC, abstractmethod
from src.characters.domain.models import Character

class CharacterRepository(ABC):
    @abstractmethod
    def all(self)->list[Character]: ...
    
    @abstractmethod
    def save(self,character: Character)->None:...