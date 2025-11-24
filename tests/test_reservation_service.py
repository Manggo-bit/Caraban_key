import unittest
from unittest.mock import Mock, MagicMock
import uuid
from datetime import date, timedelta

from src.services.reservation_service import ReservationService
from src.models.user import User, UserRole
from src.models.caravan import Caravan
from src.models.reservation import Reservation
from src.exceptions.reservation import BookingConflictError

class TestReservationService(unittest.TestCase):

    def setUp(self):
        """Set up mock components for each test."""
        self.mock_res_repo = Mock()
        self.mock_caravan_repo = Mock()
        self.mock_user_repo = Mock()
        self.mock_validator = Mock()

        self.service = ReservationService(
            reservation_repo=self.mock_res_repo,
            caravan_repo=self.mock_caravan_repo,
            user_repo=self.mock_user_repo,
            validator=self.mock_validator,
        )

        self.guest = User(name="Test Guest", contact="test@guest.com", role=UserRole.GUEST)
        self.caravan = Caravan(
            host_id=uuid.uuid4(),
            name="Test Caravan",
            location="Test Location",
            capacity=4,
            daily_rate=100.0,
        )
        
        self.start_date = date.today() + timedelta(days=5)
        self.end_date = date.today() + timedelta(days=10)

    def test_create_reservation_success(self):
        """Should create and return a reservation on success."""
        self.mock_user_repo.get_by_id.return_value = self.guest
        self.mock_caravan_repo.get_by_id.return_value = self.caravan
        
        # Mock the validator to indicate success (no return value means success)
        self.mock_validator.execute.return_value = None 

        # Use MagicMock for the 'add' method to allow assertions on it
        self.mock_res_repo.add = MagicMock()

        result = self.service.create_reservation(
            guest_id=self.guest.id,
            caravan_id=self.caravan.id,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        # 1. Verify the validator was called correctly
        self.mock_validator.execute.assert_called_once_with(self.caravan, self.start_date, self.end_date)
        
        # 2. Verify the reservation was saved
        self.mock_res_repo.add.assert_called_once()
        
        # 3. Verify the returned object is correct
        self.assertIsInstance(result, Reservation)
        self.assertEqual(result.guest_id, self.guest.id)
        self.assertEqual(result.caravan_id, self.caravan.id)
        self.assertEqual(result.total_price, 5 * 100.0) # 5 days * 100/day

    def test_create_reservation_guest_not_found(self):
        """Should raise ValueError if the guest does not exist."""
        self.mock_user_repo.get_by_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Guest with ID .* not found"):
            self.service.create_reservation(uuid.uuid4(), self.caravan.id, self.start_date, self.end_date)

    def test_create_reservation_caravan_not_found(self):
        """Should raise ValueError if the caravan does not exist."""
        self.mock_user_repo.get_by_id.return_value = self.guest
        self.mock_caravan_repo.get_by_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Caravan with ID .* not found"):
            self.service.create_reservation(self.guest.id, uuid.uuid4(), self.start_date, self.end_date)

    def test_create_reservation_validation_fails(self):
        """Should not create a reservation if the validator raises an error."""
        self.mock_user_repo.get_by_id.return_value = self.guest
        self.mock_caravan_repo.get_by_id.return_value = self.caravan
        
        # Configure the mock validator to raise a specific error
        self.mock_validator.execute.side_effect = BookingConflictError("Dates are already booked")

        # Verify that the service propagates the exception
        with self.assertRaises(BookingConflictError):
            self.service.create_reservation(self.guest.id, self.caravan.id, self.start_date, self.end_date)

        # Verify that the 'add' method was NOT called, ensuring no reservation is saved
        self.mock_res_repo.add.assert_not_called()

if __name__ == '__main__':
    unittest.main()
