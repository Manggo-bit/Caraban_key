import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Review:
    # Fields without default values first
    reservation_id: uuid.UUID
    author_id: uuid.UUID
    target_id: uuid.UUID # Can be a host_id or a caravan_id
    rating: int
    comment: str

    # Fields with default values last
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
