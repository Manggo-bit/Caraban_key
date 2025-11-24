from typing import Dict, List
import uuid
from src.models.reservation import Reservation

class ReservationRepository:
    """
    Manages the storage and retrieval of reservation data.
    This is an in-memory implementation designed for efficient lookups.
    """
    def __init__(self):
        # Provides O(1) lookup for a caravan's reservations
        self._reservations_by_caravan: Dict[uuid.UUID, List[Reservation]] = {}
        # Provides O(1) lookup for a specific reservation by its ID
        self._reservations_by_id: Dict[uuid.UUID, Reservation] = {}

    def add(self, reservation: Reservation) -> None:
        """Adds a new reservation to the repository."""
        if reservation.id in self._reservations_by_id:
            raise ValueError(f"Reservation with id {reservation.id} already exists.")

        self._reservations_by_id[reservation.id] = reservation
        
        self._reservations_by_caravan.setdefault(reservation.caravan_id, []).append(reservation)

    def get_by_id(self, reservation_id: uuid.UUID) -> Reservation | None:
        """Retrieves a reservation by its unique ID."""
        return self._reservations_by_id.get(reservation_id)

    def get_for_caravan(self, caravan_id: uuid.UUID) -> List[Reservation]:
        """Retrieves all reservations for a specific caravan."""
        return self._reservations_by_caravan.get(caravan_id, [])
