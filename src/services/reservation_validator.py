from datetime import date
import uuid
from src.models.caravan import Caravan, CaravanStatus
from src.repositories.reservation_repository import ReservationRepository
from src.exceptions.reservation import (
    InvalidDateError,
    CaravanNotAvailableError,
    BookingConflictError,
)
from src.models.reservation import ReservationStatus

class ReservationValidator:
    def __init__(self, reservation_repo: ReservationRepository):
        self._reservation_repo = reservation_repo

    def execute(self, caravan: Caravan, start_date: date, end_date: date) -> None:
        """
        Runs all validation checks for a new reservation request.
        Raises a specific exception if any check fails.
        """
        self._validate_dates(start_date, end_date)
        self._validate_caravan_status(caravan)
        self._validate_booking_conflict(caravan.id, start_date, end_date)

    def _validate_dates(self, start_date: date, end_date: date) -> None:
        """Ensures reservation dates are logical."""
        if start_date >= end_date:
            raise InvalidDateError("End date must be after start date.")
        if start_date < date.today():
            raise InvalidDateError("Start date cannot be in the past.")

    def _validate_caravan_status(self, caravan: Caravan) -> None:
        """Ensures the caravan is available for booking."""
        if caravan.status != CaravanStatus.AVAILABLE:
            raise CaravanNotAvailableError(f"Caravan '{caravan.name}' is not available for booking.")

    def _validate_booking_conflict(self, caravan_id: uuid.UUID, start_date: date, end_date: date) -> None:
        """Checks for overlapping reservations to prevent double booking."""
        reservations = self._reservation_repo.get_for_caravan(caravan_id)
        
        for r in reservations:
            if r.status in [ReservationStatus.CANCELLED, ReservationStatus.REJECTED]:
                continue
            # Check for overlap: (StartA < EndB) and (EndA > StartB)
            if r.start_date < end_date and r.end_date > start_date:
                raise BookingConflictError(
                    f"Caravan is already booked between {r.start_date} and {r.end_date}."
                )
