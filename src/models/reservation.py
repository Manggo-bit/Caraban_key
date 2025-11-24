import uuid
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

class ReservationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class Reservation:
    # Fields without default values first
    guest_id: uuid.UUID
    caravan_id: uuid.UUID
    start_date: date
    end_date: date
    total_price: float
    
    # Fields with default values last
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: ReservationStatus = ReservationStatus.PENDING
