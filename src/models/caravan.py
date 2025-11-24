import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List

class CaravanStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

@dataclass
class Caravan:
    # Fields without default values first
    host_id: uuid.UUID
    name: str
    location: str
    capacity: int
    daily_rate: float
    
    # Fields with default values last
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    amenities: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)
    status: CaravanStatus = CaravanStatus.AVAILABLE
