from datetime import date
import uuid
from src.models.reservation import Reservation
from src.repositories.reservation_repository import ReservationRepository
from src.repositories.caravan_repository import CaravanRepository
from src.repositories.user_repository import UserRepository
from src.services.reservation_validator import ReservationValidator
from src.exceptions.reservation import ReservationError

class ReservationService:
    """
    Orchestrates the business logic for creating and managing reservations.
    """
    def __init__(
        self,
        reservation_repo: ReservationRepository,
        caravan_repo: CaravanRepository,
        user_repo: UserRepository,
        validator: ReservationValidator,
    ):
        self._reservation_repo = reservation_repo
        self._caravan_repo = caravan_repo
        self._user_repo = user_repo
        self._validator = validator

    def create_reservation(
        self, guest_id: uuid.UUID, caravan_id: uuid.UUID, start_date: date, end_date: date
    ) -> Reservation:
        """
        Creates and stores a new reservation after validating the request.

        Raises:
            ValueError: If the guest or caravan cannot be found.
            ReservationError: If the reservation request is invalid.
        """
        guest = self._user_repo.get_by_id(guest_id)
        if not guest:
            raise ValueError(f"Guest with ID {guest_id} not found.")

        caravan = self._caravan_repo.get_by_id(caravan_id)
        if not caravan:
            raise ValueError(f"Caravan with ID {caravan_id} not found.")

        # 1. Validation: Delegate to the validator service.
        self._validator.execute(caravan, start_date, end_date)

        # 2. Calculation: Determine the total price.
        duration_days = (end_date - start_date).days
        if duration_days <= 0:
            # This case should be caught by the validator, but as a safeguard:
            raise ReservationError("Reservation must be for at least one day.")
        total_price = duration_days * caravan.daily_rate

        # 3. Creation: Instantiate the new reservation object.
        # A Factory pattern could be used here if creation becomes more complex.
        new_reservation = Reservation(
            guest_id=guest_id,
            caravan_id=caravan_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
        )

        # 4. Storage: Persist the new reservation.
        self._reservation_repo.add(new_reservation)

        # In a real application, this is where you might trigger other processes,
        # such as payment processing or sending notifications to the host/guest
        # (potentially using an Observer pattern).
        
        return new_reservation
