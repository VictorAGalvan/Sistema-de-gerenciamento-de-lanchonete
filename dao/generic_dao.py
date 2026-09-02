from abc import ABC, abstractmethod
from typing import Any, List, Optional

class GenericDAO(ABC):
    @abstractmethod
    def insert(self, objeto: Any) -> Any:
        pass

    @abstractmethod
    def select_por_id(self, id_objeto: int) -> Optional[Any]:
        pass

    @abstractmethod
    def select_todos(self) -> List[Any]:
        pass

    @abstractmethod
    def delete(self, id_objeto: int) -> None:
        pass

    @abstractmethod
    def update(self, objeto: Any) -> Any:
        pass