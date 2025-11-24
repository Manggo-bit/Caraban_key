import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class Payment:
    # Fields without default values first
    reservation_id: uuid.UUID
    amount: float

    # Fields with default values last
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    status: PaymentStatus = PaymentStatus.PENDING
