import unittest
from unittest.mock import Mock
import uuid
from datetime import date, timedelta
from src.services.reservation_validator import ReservationValidator
from src.models.caravan import Caravan, CaravanStatus
from src.models.reservation import Reservation, ReservationStatus
from src.exceptions.reservation import (
    InvalidDateError,
    CaravanNotAvailableError,
    BookingConflictError,
)

class TestReservationValidator(unittest.TestCase):

    def setUp(self):
        """Set up a mock repository and validator for each test."""
        self.mock_repo = Mock()
        self.validator = ReservationValidator(self.mock_repo)
        
        self.caravan = Caravan(
            id=uuid.uuid4(),
            host_id=uuid.uuid4(),
            name="Test Caravan",
            location="Test Location",
            capacity=4,
            daily_rate=100.0,
            status=CaravanStatus.AVAILABLE,
        )
        self.today = date.today()
        self.start_date = self.today + timedelta(days=10)
        self.end_date = self.today + timedelta(days=15)

    def test_execute_success_with_no_existing_reservations(self):
        """Should pass with valid inputs and no conflicts."""
        self.mock_repo.get_for_caravan.return_value = []
        try:
            self.validator.execute(self.caravan, self.start_date, self.end_date)
        except Exception as e:
            self.fail(f"Validation failed unexpectedly: {e}")

    def test_validate_dates_end_date_before_start_date(self):
        """Should raise InvalidDateError if end_date is before start_date."""
        with self.assertRaisesRegex(InvalidDateError, "End date must be after start date."):
            self.validator.execute(self.caravan, self.end_date, self.start_date)

    def test_validate_dates_start_date_in_past(self):
        """Should raise InvalidDateError if start_date is in the past."""
        past_date = self.today - timedelta(days=1)
        with self.assertRaisesRegex(InvalidDateError, "Start date cannot be in the past."):
            self.validator.execute(self.caravan, past_date, self.start_date)

    def test_validate_caravan_status_not_available(self):
        """Should raise CaravanNotAvailableError if caravan status is not AVAILABLE."""
        self.caravan.status = CaravanStatus.MAINTENANCE
        with self.assertRaisesRegex(CaravanNotAvailableError, "is not available for booking"):
            self.validator.execute(self.caravan, self.start_date, self.end_date)

    def test_validate_booking_conflict_direct_overlap(self):
        """Should raise BookingConflictError if dates overlap with an existing reservation."""
        existing_reservation = Reservation(
            id=uuid.uuid4(),
            guest_id=uuid.uuid4(),
            caravan_id=self.caravan.id,
            start_date=self.start_date + timedelta(days=1), # Starts within the new request
            end_date=self.end_date - timedelta(days=1),   # Ends within the new request
            total_price=200.0,
        )
        self.mock_repo.get_for_caravan.return_value = [existing_reservation]
        
        with self.assertRaisesRegex(BookingConflictError, "Caravan is already booked"):
            self.validator.execute(self.caravan, self.start_date, self.end_date)

    def test_validate_booking_conflict_ignores_cancelled_reservations(self):
        """Should not raise a conflict if the overlapping reservation is cancelled."""
        cancelled_reservation = Reservation(
            id=uuid.uuid4(),
            guest_id=uuid.uuid4(),
            caravan_id=self.caravan.id,
            start_date=self.start_date + timedelta(days=1),
            end_date=self.end_date - timedelta(days=1),
            total_price=200.0,
            status=ReservationStatus.CANCELLED,
        )
        self.mock_repo.get_for_caravan.return_value = [cancelled_reservation]
        
        try:
            self.validator.execute(self.caravan, self.start_date, self.end_date)
        except BookingConflictError:
            self.fail("Validator incorrectly flagged a conflict with a cancelled reservation.")

if __name__ == '__main__':
    unittest.main()
