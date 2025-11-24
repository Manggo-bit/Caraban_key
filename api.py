# api.py

import uuid
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# src 폴더의 모듈들을 가져옵니다.
from src.models.user import User, UserRole
from src.models.caravan import Caravan
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

        # 🔹 4개의 카라반 등록 (프론트 UI와 이름 맞춤)
        caravan1 = Caravan(
            host_id=host.id,
            name="모던 익스플로러",
            location="Seoul",
            capacity=2,
            daily_rate=120000.0,
        )
        caravan2 = Caravan(
            host_id=host.id,
            name="패밀리 보이저",
            location="Busan",
            capacity=6,
            daily_rate=180000.0,
        )
        caravan3 = Caravan(
            host_id=host.id,
            name="레트로 어드벤처러",
            location="Incheon",
            capacity=3,
            daily_rate=95000.0,
        )
        caravan4 = Caravan(
            host_id=host.id,
            name="오프로드 비스트",
            location="Jeju",
            capacity=4,
            daily_rate=250000.0,
        )

        caravan_repo.add(caravan1)
        caravan_repo.add(caravan2)
        caravan_repo.add(caravan3)
        caravan_repo.add(caravan4)

    return user_repo, caravan_repo, reservation_repo, reservation_service


# 전역에서 사용할 리포지토리/서비스 인스턴스
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
        # 현재는 GUEST 역할의 첫 번째 사용자를 예약자라고 가정
        guest = next(
            (user for user in user_repo.get_all() if user.role == UserRole.GUEST),
            None,
        )
        if not guest:
            raise HTTPException(status_code=404, detail="Guest user not found.")

        new_reservation = reservation_service.create_reservation(
            guest_id=guest.id,
            caravan_id=request.caravan_id,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        return new_reservation
    except ReservationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CaravanShare API"}