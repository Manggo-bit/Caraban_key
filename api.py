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

# 🔐 간단한 인증용: 이메일 -> 비밀번호(평문) 매핑
# ※ 실제 서비스에서는 절대 이렇게 하면 안 되고, 비밀번호 해싱 + DB 사용이 필요합니다.
users_passwords: dict[str, str] = {}

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

        # 🔐 기본 비밀번호 설정 (테스트용)
        users_passwords[host.contact] = "host1234"
        users_passwords[guest.contact] = "guest1234"

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


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
    role: UserRole


# 🔐 --- 인증 관련 API 엔드포인트 ---  ⬅⬅⬅ 여기 부분이 지금 질문하신 코드입니다!

@app.post("/api/auth/register")
def register_user(request: RegisterRequest):
    """
    새 사용자 회원가입.
    - 이미 같은 이메일이 있으면 400 에러
    - 성공 시 생성된 사용자 정보 반환
    """
    # 이미 같은 이메일(=contact)을 가진 유저가 있는지 확인
    for user in user_repo.get_all():
        if user.contact == request.email:
            raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

    # 새 유저 생성 (기본은 GUEST 역할)
    new_user = User(
        name=request.name,
        contact=request.email,
        role=UserRole.GUEST,
    )
    user_repo.add(new_user)

    # 비밀번호 저장 (평문) — 과제용이므로 단순하게 구현
    users_passwords[request.email] = request.password

    return {
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.contact,
        "role": new_user.role,
    }


@app.post("/api/auth/login", response_model=LoginResponse)
def login_user(request: LoginRequest):
    """
    이메일 + 비밀번호로 로그인.
    - 이메일이 없거나 비밀번호가 틀리면 401 에러
    - 성공 시 유저 정보 반환 (간단한 형태)
    """
    # 이메일로 유저 찾기
    user = next((u for u in user_repo.get_all() if u.contact == request.email), None)
    if not user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # 비밀번호 확인
    saved_password = users_passwords.get(request.email)
    if saved_password is None or saved_password != request.password:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    return LoginResponse(
        user_id=user.id,
        name=user.name,
        email=user.contact,
        role=user.role,
    )


# --- 기존 카라반/예약 API 엔드포인트 ---
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
