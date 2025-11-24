# Architecture

이 문서는 CaravanShare 프로젝트의 전체 아키텍처, 코드 구조, 데이터 흐름을 설명합니다. 새로운 팀원이 이 문서를 통해 프로젝트를 빠르게 이해하고 기능 개발에 참여하는 것을 목표로 합니다.

## 1. 전체 아키텍처 개요

CaravanShare는 최신 웹 표준에 따라 프론트엔드와 백엔드가 명확히 분리된 **헤드리스(Headless) 구조**를 따릅니다.

```
+--------------------------------+      +---------------------------------+
|                                |      |                                 |
|      React + TypeScript        |      |         FastAPI (Python)        |
|          (Client)              |      |            (Server)             |
|                                |      |                                 |
+--------------------------------+      +---------------------------------+
           |                                     ^
           | (HTTP/JSON API Call)                | (Layered Architecture)
           v                                     |
+--------------------------------+      +---------------------------------+
|       API (api.py)             | <--> |  src/ (Domain & Business Logic) |
+--------------------------------+      +---------------------------------+
```

-   **프론트엔드 (Client)**: `React`와 `TypeScript`를 사용하여 사용자 인터페이스를 구축합니다. 사용자의 모든 인터랙션은 프론트엔드에서 처리되며, 데이터가 필요할 경우 백엔드에 API를 호출합니다.
-   **백엔드 (Server)**: `FastAPI`를 사용하여 프론트엔드가 호출할 수 있는 `JSON` 기반의 `RESTful API`를 제공합니다. 백엔드 내부는 역할에 따라 계층(Layer)이 나뉘어 있습니다.

### 데이터 흐름 요약

1.  **사용자 요청**: 사용자가 브라우저(`localhost:3000`)에서 특정 액션을 취합니다.
2.  **API 호출**: 프론트엔드의 `api` 모듈이 이 액션에 맞는 백엔드 API(`localhost:8000/api/...`)를 `fetch`를 이용해 호출합니다.
3.  **비즈니스 로직 처리**: 백엔드의 엔트리포인트(`api.py`)가 요청을 받아, `src` 폴더 내부의 서비스 및 리포지토리 계층에 로직 처리를 위임합니다.
4.  **응답**: 로직 처리 결과를 `JSON` 형태로 프론트엔드에 반환합니다.
5.  **UI 업데이트**: 프론트엔드는 받은 데이터로 상태(State)를 업데이트하고, 이에 따라 UI가 변경됩니다.

## 2. 백엔드 구조 (FastAPI)

백엔드는 **계층형 아키텍처(Layered Architecture)**를 적용하여 각 모듈이 명확한 책임을 갖도록 설계되었습니다.

-   **`api.py` (Presentation Layer)**
    -   **역할**: FastAPI 애플리케이션의 주 진입점. HTTP 요청을 직접 받고 응답을 반환하는 최상위 계층입니다.
    -   **주요 책임**:
        -   URL 엔드포인트(`/api/reservations` 등) 정의
        -   CORS, 미들웨어 등 앱 전역 설정
        -   요청 데이터를 Pydantic 모델(`ReservationRequest`)로 변환 및 검증
        -   비즈니스 로직을 `Service` 계층에 위임
        -   Service에서 발생한 예외(`ReservationError`)를 적절한 HTTP 상태 코드(400, 500 등)로 변환하여 클라이언트에 반환

-   **`src/` (Domain & Business Logic Layer)**
    -   **`models/`**: 애플리케이션의 핵심 데이터 구조를 정의합니다 (`Caravan`, `Reservation`, `User`). 순수한 데이터 객체(dataclass, Enum)이며, 비즈니스 로직은 포함하지 않습니다.
    -   **`repositories/` (Data Access Layer)**: 데이터의 영속성(Persistence)을 담당합니다. 현재는 In-memory `dict`를 사용하여 데이터를 저장하지만, 향후 DB로 교체될 수 있도록 인터페이스 역할을 합니다. (`add`, `get_by_id` 등)
    -   **`services/` (Service Layer)**: 핵심 비즈니스 로직을 수행합니다. 여러 리포지토리를 조합하여 복잡한 작업을 처리하고, 데이터의 유효성을 검증합니다. (예: `ReservationService`가 가격을 계산하고 예약을 생성)
    -   **`exceptions/`**: 비즈니스 로직에서 발생할 수 있는 커스텀 예외(`ReservationError` 등)를 정의합니다.

### 예약 생성 시 함수 호출 흐름

1.  **`POST /api/reservations`**: `api.py`의 `create_reservation` 함수가 호출됩니다.
2.  **`ReservationService.create_reservation()`**: `api.py`는 HTTP 요청 데이터를 `ReservationService`의 `create_reservation` 메소드에 전달합니다.
3.  **`ReservationValidator.execute()`**: `ReservationService`는 예약 규칙(날짜, 중복 여부 등)을 검증하기 위해 `ReservationValidator`를 호출합니다.
4.  **`CaravanRepository.get_by_id()`**: 서비스가 예약할 카라반 정보를 리포지토리에서 조회합니다.
5.  **가격 계산**: 서비스가 예약 기간과 카라반의 `daily_rate`를 이용해 총가격을 계산합니다.
6.  **`ReservationRepository.add()`**: 모든 로직이 성공하면, 서비스는 완성된 `Reservation` 객체를 `ReservationRepository`에 전달하여 저장합니다.
7.  `api.py`는 생성된 `Reservation` 객체를 클라이언트에 `JSON`으로 반환합니다.

## 3. 프론트엔드 구조 (React)

프론트엔드는 **컴포넌트 기반 아키텍처(Component-Based Architecture)**를 따르며, 역할에 따라 파일이 분리되어 있습니다.

-   **`App.tsx` (루트 컴포넌트)**: 전체 애플리케이션의 레이아웃과 상태를 관리하는 최상위 부모 컴포넌트입니다. 카라반 목록 데이터, 예약 대상 카라반(`bookingCaravan`) 등의 핵심 상태를 가집니다.
-   **`components/`**: 재사용 가능한 UI 조각들입니다.
    -   `CaravanList.tsx`: 카라반 목록을 받아 화면에 렌더링하는 역할만 담당하는 순수 UI 컴포넌트.
    -   `ReservationModal.tsx`: 특정 카라반의 예약 과정을 처리하는 모달 컴포넌트. 내부적으로 날짜 선택, 가격 계산, API 호출 등의 상태를 관리합니다.
-   **`api/`**: 백엔드 API 호출을 담당하는 함수들을 모아둔 곳입니다.
    -   `caravan.ts`: 카라반 관련 API (`fetchCaravans`)
    -   `reservation.ts`: 예약 관련 API (`createReservation`)
-   **`data/`**: 순수 데이터 또는 타입을 정의합니다.
    -   `caravans.ts`: 카라반의 UI 관련 데이터(설명, 이미지 경로 등)와 프론트엔드용 `Caravan` 타입을 정의합니다.

### "지금 예약하기" 클릭 시 동작 흐름

1.  **`CaravanList.tsx`**: 사용자가 특정 카라반의 "지금 예약하기" 버튼을 클릭합니다.
2.  **`onBook` 콜백 호출**: `CaravanList`는 부모(`App.tsx`)로부터 받은 `onBook` 함수를 클릭된 카라반 정보와 함께 호출합니다.
3.  **`App.tsx` 상태 업데이트**: `App.tsx`의 `handleBookNow` 함수가 실행되어 `bookingCaravan` 상태를 클릭된 카라반 객체로 업데이트합니다.
4.  **모달 렌더링**: `bookingCaravan` 상태가 `null`이 아니게 되면서, `ReservationModal` 컴포넌트가 화면에 렌더링됩니다.
5.  **`ReservationModal.tsx`**: 사용자가 모달 내에서 날짜를 선택하고 "예약 확정"을 누르면, 모달은 `api/reservation.ts`의 `createReservation` 함수를 호출하여 백엔드에 `POST` 요청을 보냅니다.
6.  **성공/실패 처리**: API 호출 결과에 따라 `onSuccess` 콜백을 호출하거나 `alert`로 에러 메시지를 표시합니다.

## 4. 데이터 모델 & 타입

프론트엔드와 백엔드는 각자의 필요에 따라 별도의 데이터 타입을 가집니다.

-   **백엔드 모델 (`src/models/*.py`)**: 서버와 데이터베이스를 기준으로 설계된 순수한 데이터 모델입니다.
    -   `Caravan`: `host_id`, `name`, `location`, `capacity`, `daily_rate` 등 핵심 비즈니스 데이터를 가집니다.
    -   `Reservation`: `guest_id`, `caravan_id`, `start_date`, `end_date`, `total_price` 등 예약 정보를 가집니다.

-   **프론트엔드 타입 (`api/*.ts`, `data/*.ts`)**: UI 표현을 기준으로 설계되었습니다.
    -   `BackendCaravan` (`api/caravan.ts`): 백엔드 API 응답과 1:1로 매칭되는 타입입니다 (`snake_case` 필드명, `daily_rate` 등).
    -   `Caravan` (`data/caravans.ts`): 실제 UI 컴포넌트에서 사용하는 타입입니다. `imageUrl`, `description` 등 UI에만 필요한 필드를 포함하며, `camelCase` 필드명을 사용합니다.

### 데이터 병합 (Merge) 로직

`App.tsx`에서는 두 타입을 병합하여 UI에서 사용하기 좋은 형태로 가공합니다.
> `useEffect` 내에서 `fetchCaravans` 호출 → `BackendCaravan[]` 획득 → `data/caravans.ts`의 `Caravan[]`과 매핑 → 백엔드의 `daily_rate`, `id` 등을 프론트엔드 `Caravan` 객체에 추가

이러한 분리는 **관심사의 분리(Separation of Concerns)** 원칙을 따릅니다. 백엔드는 순수한 비즈니스 데이터만 신경 쓰고, 프론트엔드는 UI 표현에 필요한 데이터를 자유롭게 추가/변경할 수 있습니다.

## 5. 에러 처리 흐름

-   **백엔드**:
    1.  `ReservationService`나 `Validator`에서 예약 규칙에 위배되는 상황이 발생하면 `raise ReservationError("에러 메시지")`와 같이 커스텀 예외를 발생시킵니다.
    2.  `api.py`의 API 핸들러(`create_reservation`)는 `try...except ReservationError as e:` 블록으로 이 예외를 잡습니다.
    3.  잡힌 예외는 `FastAPI`의 `HTTPException(status_code=400, detail=str(e))`으로 변환되어 클라이언트에 `400 Bad Request` 응답과 함께 에러 메시지를 `JSON`으로 전달합니다.

-   **프론트엔드**:
    1.  `ReservationModal.tsx`의 `handleReservation` 함수에서 `fetch` API를 호출합니다.
    2.  응답 객체의 `res.ok`가 `false`이면 `throw new Error(data.detail)` 구문을 통해 에러를 발생시킵니다. (`data.detail`에는 백엔드가 보낸 에러 메시지가 담겨 있습니다)
    3.  `try...catch` 블록이 이 에러를 잡아, `alert(e.message)`를 통해 사용자에게 백엔드에서 온 에러 메시지를 그대로 보여줍니다.

## 6. 확장 포인트

이 아키텍처는 향후 기능 확장을 용이하게 하도록 설계되었습니다.

-   **DB 연동**:
    -   **현재**: `CaravanRepository` 등은 데이터를 메모리 상의 `dict`에 저장합니다.
    -   **확장**: `PostgresCaravanRepository`와 같은 새로운 클래스를 만들고, 기존 `CaravanRepository`와 동일한 메소드(`add`, `get_by_id` 등)를 구현합니다. (리포지토리 패턴)
    -   `api.py`의 `setup_dependencies` 함수에서 `caravan_repo = CaravanRepository()`를 `caravan_repo = PostgresCaravanRepository()`로 교체하기만 하면, 다른 서비스 코드의 변경 없이 DB 연동이 완료됩니다.

-   **인증 기능 추가**:
    -   **백엔드**: `FastAPI`의 `Depends` 시스템을 활용하여 엔드포인트에 인증 미들웨어를 추가할 수 있습니다. JWT 토큰을 검증하고 유효한 사용자 정보를 `request`에 주입하는 의존성을 만듭니다.
    -   **프론트엔드**: 로그인 페이지를 만들고, 로그인 성공 시 받은 JWT 토큰을 `localStorage`나 `Context`에 저장합니다. 이후 모든 API 요청의 `Authorization` 헤더에 이 토큰을 담아 보냅니다.
