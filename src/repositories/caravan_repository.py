import uuid
from typing import Dict, List
from src.models.caravan import Caravan

class CaravanRepository:
    """Manages storage for Caravan objects in memory."""
    def __init__(self):
        self._caravans: Dict[uuid.UUID, Caravan] = {}

    def add(self, caravan: Caravan) -> None:
        """Adds a caravan to the repository."""
        if caravan.id in self._caravans:
            raise ValueError(f"Caravan with ID {caravan.id} already exists.")
        self._caravans[caravan.id] = caravan

    def get_by_id(self, caravan_id: uuid.UUID) -> Caravan | None:
        """Retrieves a caravan by its unique ID."""
        return self._caravans.get(caravan_id)

    def get_all(self) -> List[Caravan]:
        """Returns a list of all caravans."""
        return list(self._caravans.values())
