from dataclasses import dataclass, field
from enum import Enum
import uuid

class UserRole(Enum):
    GUEST = "guest"
    HOST = "host"

@dataclass
class User:
    # Fields without default values first
    name: str
    contact: str
    role: UserRole
    
    # Fields with default values last
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    identity_verified: bool = False
