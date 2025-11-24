import uuid
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# src 폴더의 모듈들을 가져옵니다.
from src.models.user import User, UserRole
from src.models.caravan import Caravan, CaravanStatus
from src.repositories.user_repository import UserRepository
from src.repositories.caravan_repository import CaravanRepository
from src.repositories.reservation_repository import ReservationRepository
from src.services.reservation_validator import ReservationValidator
from src.services.reservation_service import ReservationService
from src.exceptions.reservation import ReservationError

# --- FastAPI 애플리케이션 설정 ---
app = FastAPI()

# --- CORS 미들웨어 설정 ---
# 프론트엔드 (React) 애플리케이션이 3000번 포트에서 실행될 것이므로, 해당 주소에서의 요청을 허용합니다.
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 의존성 설정 ---
def setup_dependencies():
    """애플리케이션 실행에 필요한 모든 구성요소를 생성하고 연결합니다."""
    user_repo = UserRepository()
    caravan_repo = CaravanRepository()
    reservation_repo = ReservationRepository()
    validator = ReservationValidator(reservation_repo)
    reservation_service = ReservationService(
        reservation_repo, caravan_repo, user_repo, validator
    )
    
    # 초기 데이터 생성
    if not user_repo.get_all():
        host = User(name="Host Alice", contact="host@example.com", role=UserRole.HOST)
        guest = User(name="Guest Bob", contact="guest@example.com", role=UserRole.GUEST)
        user_repo.add(host)
        user_repo.add(guest)

        caravan1 = Caravan(
            host_id=host.id,
            name="Cozy Camper",
            location="Seoul",
            capacity=4,
            daily_rate=150.0
        )
        caravan2 = Caravan(
            host_id=host.id,
            name="Luxury Land-Yacht",
            location="Busan",
            capacity=6,
            daily_rate=250.0
        )
        caravan_repo.add(caravan1)
        caravan_repo.add(caravan2)
        
    return user_repo, caravan_repo, reservation_repo, reservation_service

user_repo, caravan_repo, reservation_repo, reservation_service = setup_dependencies()

# --- Pydantic 모델 (데이터 유효성 검사) ---
class ReservationRequest(BaseModel):
    caravan_id: uuid.UUID
    start_date: date
    end_date: date

# --- API 엔드포인트 ---
@app.get("/api/caravans")
def get_caravans():
    """모든 카라반의 목록을 반환합니다."""
    return caravan_repo.get_all()

@app.post("/api/reservations")
def create_reservation(request: ReservationRequest):
    """새로운 예약을 생성합니다."""
    try:
        # 현재는 CLI에서 사용하던 'guest' 사용자를 하드코딩하여 사용합니다.
        # 향후 실제 사용자 인증 시스템이 도입되면 이 부분을 수정해야 합니다.
        guest = next((user for user in user_repo.get_all() if user.role == UserRole.GUEST), None)
        if not guest:
            raise HTTPException(status_code=404, detail="Guest user not found.")

        new_reservation = reservation_service.create_reservation(
            guest_id=guest.id,
            caravan_id=request.caravan_id,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return new_reservation
    except ReservationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CaravanShare API"}

