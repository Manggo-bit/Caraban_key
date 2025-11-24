import uuid
from datetime import datetime, date

# src 폴더의 모듈들을 가져옵니다.
from src.models.user import User, UserRole
from src.models.caravan import Caravan, CaravanStatus
from src.repositories.user_repository import UserRepository
from src.repositories.caravan_repository import CaravanRepository
from src.repositories.reservation_repository import ReservationRepository
from src.services.reservation_validator import ReservationValidator
from src.services.reservation_service import ReservationService
from src.exceptions.reservation import ReservationError

def setup_dependencies():
    """애플리케이션 실행에 필요한 모든 구성요소를 생성하고 연결합니다."""
    user_repo = UserRepository()
    caravan_repo = CaravanRepository()
    reservation_repo = ReservationRepository()
    validator = ReservationValidator(reservation_repo)
    reservation_service = ReservationService(
        reservation_repo, caravan_repo, user_repo, validator
    )
    return user_repo, caravan_repo, reservation_repo, reservation_service

def seed_data(user_repo: UserRepository, caravan_repo: CaravanRepository):
    """CLI 실행 시 사용할 초기 데이터를 생성합니다."""
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
    
    print("✅ 초기 데이터 생성 완료.")
    return guest # 예약을 생성할 게스트를 반환합니다.

def list_caravans(caravan_repo: CaravanRepository):
    """등록된 모든 카라반의 목록을 출력합니다."""
    print("\n--- 🚐 Available Caravans ---")
    caravans = caravan_repo.get_all()
    if not caravans:
        print("등록된 카라반이 없습니다.")
        return
    
    for caravan in caravans:
        print(f"  ID: {caravan.id}")
        print(f"  Name: {caravan.name}")
        print(f"  Location: {caravan.location}")
        print(f"  Capacity: {caravan.capacity} people")
        print(f"  Rate: ${caravan.daily_rate}/day")
        print("-" * 20)

def make_reservation(reservation_service: ReservationService, guest: User, caravan_repo: CaravanRepository):
    """사용자로부터 입력을 받아 예약을 생성합니다."""
    print("\n--- 📅 Make a Reservation ---")
    list_caravans(caravan_repo)
    
    try:
        caravan_id_str = input("예약할 카라반의 ID를 입력하세요: ")
        caravan_id = uuid.UUID(caravan_id_str)
        
        start_date_str = input("시작 날짜를 입력하세요 (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        
        end_date_str = input("종료 날짜를 입력하세요 (YYYY-MM-DD): ")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # 예약 서비스 호출
        new_reservation = reservation_service.create_reservation(
            guest_id=guest.id,
            caravan_id=caravan_id,
            start_date=start_date,
            end_date=end_date
        )
        
        print("\n🎉 예약이 성공적으로 완료되었습니다!")
        print(f"  Reservation ID: {new_reservation.id}")
        print(f"  Total Price: ${new_reservation.total_price:.2f}")

    except (ValueError, ReservationError) as e:
        print(f"\n❌ 오류: 예약을 생성하지 못했습니다. ({e})")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")


def main():
    """CLI 애플리케이션의 메인 루프입니다."""
    user_repo, caravan_repo, reservation_repo, reservation_service = setup_dependencies()
    guest = seed_data(user_repo, caravan_repo)
    
    print("\nWelcome to CaravanShare CLI!")

    while True:
        print("\n--- Menu ---")
        print("1. 카라반 목록 보기")
        print("2. 예약하기")
        print("3. 종료")
        choice = input("원하는 작업의 번호를 입력하세요: ")

        if choice == '1':
            list_caravans(caravan_repo)
        elif choice == '2':
            make_reservation(reservation_service, guest, caravan_repo)
        elif choice == '3':
            print("애플리케이션을 종료합니다. Goodbye!")
            break
        else:
            print("잘못된 입력입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
