class ReservationError(Exception):
    """Base exception for reservation-related errors."""
    pass

class InvalidDateError(ReservationError):
    """Raised when reservation dates are invalid."""
    pass

class CaravanNotAvailableError(ReservationError):
    """Raised when a caravan is not available for booking."""
    pass

class BookingConflictError(ReservationError):
    """Raised when a caravan is already booked for the selected dates."""
    pass
