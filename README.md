# CaravanShare

CaravanShare는 주말 여행이나 장기 모험을 위한 카라반을 쉽게 찾고 예약할 수 있는 웹 애플리케이션입니다. 이 프로젝트는 최신 웹 기술을 사용하여 아이디어를 빠르게 프로토타이핑하는 과정을 보여주기 위해 만들어졌습니다.

현재 이 프로젝트는 Python FastAPI를 이용한 백엔드 서버와 React/TypeScript 기반의 프론트엔드를 통해 **카라반 목록을 조회**하고, 원하는 날짜를 선택하여 **예약하는 핵심 기능**을 구현하고 있습니다.

## 🚀 주요 기능

- **카라반 목록 조회**: 등록된 모든 카라반의 사진, 설명, 기본 가격 등의 정보를 한눈에 볼 수 있습니다.
- **예약 기능**:
  - '지금 예약하기' 버튼을 통해 예약 모달을 엽니다.
  - 날짜(시작일, 종료일)를 선택하면 실시간으로 총 예약 금액이 계산됩니다.
  - 예약 요청 시 FastAPI 백엔드로 데이터를 전송하여 예약을 생성합니다.
- **실시간 피드백**: 예약이 성공적으로 완료되면 사용자에게 성공 메시지를 보여줍니다.

#### 현재 구현 범위
- 인메모리(In-memory) 데이터를 사용한 카라반 목록 조회 및 신규 예약 생성
- 프론트엔드와 백엔드 간의 기본적인 API 연동

#### 향후 구현 예정
- 실제 데이터베이스(예: PostgreSQL) 연동
- 사용자 회원가입 및 로그인 기능
- 예약 내역 조회 및 관리 페이지

## 🛠️ 기술 스택

| 구분 | 기술 | 설명 |
|---|---|---|
| **백엔드** | Python, FastAPI, Uvicorn, Pydantic | 빠르고 현대적인 API 서버를 구축합니다. |
| **프론트엔드** | React, TypeScript, Create React App | 타입 안정성을 갖춘 동적인 사용자 인터페이스를 구현합니다. |
| **API 통신** | Fetch API | 브라우저 내장 API를 사용하여 백엔드와 비동기 통신을 수행합니다. |

## 📁 폴더 구조

주요 디렉터리 및 파일 구조는 다음과 같습니다.

```
/
├── api.py                  # FastAPI 애플리케이션의 메인 엔트리 포인트
├── requirements.txt        # Python 백엔드 의존성 목록
│
├── src/                    # 백엔드 비즈니스 로직
│   ├── models/             # Pydantic 데이터 모델 (Caravan, Reservation 등)
│   ├── repositories/       # 데이터 접근 로직 (In-memory DB 역할)
│   ├── services/           # 예약 생성, 검증 등 핵심 비즈니스 로직
│   └── exceptions/         # 커스텀 예외 정의
│
└── frontend/               # React 프론트엔드 프로젝트 루트
    ├── package.json        # Node.js 의존성 및 스크립트
    ├── src/
    │   ├── App.tsx         # 메인 애플리케이션 컴포넌트
    │   ├── components/     # 재사용 가능한 React 컴포넌트 (CaravanList, ReservationModal)
    │   ├── api/            # 백엔드 API 호출 함수 (fetchCaravans, createReservation)
    │   └── data/           # 프론트엔드 UI용 정적 데이터 (이미지 URL, 설명 등)
    └── public/             # 정적 에셋 (index.html, 이미지)
```

## 💻 로컬 실행 방법

이 프로젝트를 로컬 환경에서 실행하려면 아래 단계를 따르세요. (WSL/Linux 기준)

### 1. 백엔드 서버 실행

```bash
# 1) 레포지토리 클론 및 이동
git clone https://github.com/Manggo-bit/Caraban_key.git
cd Caraban_key

# 2) Python 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 3) 백엔드 의존성 설치
pip install -r requirements.txt

# 4) 백엔드 서버 실행 (FastAPI)
# --reload 옵션으로 코드 변경 시 자동 재시작됩니다.
python3 -m uvicorn api:app --reload --port 8000
```
> 백엔드 서버는 `http://localhost:8000` 에서 실행됩니다.

### 2. 프론트엔드 서버 실행

새 터미널을 열고 다음 명령어를 실행하세요.

```bash
# 1) 프론트엔드 디렉터리로 이동
cd frontend

# 2) 프론트엔드 의존성 설치
npm install

# 3) 프론트엔드 개발 서버 실행
npm start
```
> 프론트엔드 개발 서버는 `http://localhost:3000` 에서 실행되며, 자동으로 브라우저 창이 열립니다.

이제 `http://localhost:3000` 으로 접속하여 CaravanShare 서비스를 이용할 수 있습니다.

## 📄 API 엔드포인트

| Method | URL | 설명 | 요청 예시 | 응답 예시 (성공) | 사용처 (프론트) |
|---|---|---|---|---|---|
| `GET` | `/` | API 서버 헬스 체크 | - | `{"message": "Welcome to the CaravanShare API"}` | - |
| `GET` | `/api/caravans` | 모든 카라반 목록 조회 | - | `[{"host_id": "...", "name": "모던 익스플로러", ...}]` | `App.tsx` |
| `POST` | `/api/reservations` | 신규 예약 생성 | ```json { "caravan_id": "uuid-string", "start_date": "2025-12-24", "end_date": "2025-12-26" } ``` | ```json { "guest_id": "...", "caravan_id": "...", ..., "total_price": 240000.0 } ``` | `ReservationModal.tsx` |

## ✨ 프론트엔드 동작 흐름

1.  **`App.tsx`**:
    -   페이지가 로드되면 `useEffect` 훅을 통해 `fetchCaravans` API를 호출합니다 (`GET /api/caravans`).
    -   백엔드에서 받은 카라반 데이터(`BackendCaravan`)와 프론트엔드 `data/caravans.ts`에 정의된 UI용 데이터(이미지, 설명 등)를 병합(merge)합니다.
        -   **핵심**: 백엔드의 `daily_rate`, `capacity` 등 실시간 정보와 프론트엔드의 정적 UI 정보를 합쳐 완전한 `Caravan` 객체를 만듭니다.
    -   병합된 카라반 목록을 `CaravanList` 컴포넌트에 전달합니다.

2.  **`CaravanList.tsx`**:
    -   전달받은 카라반 목록을 순회하며 각 카라반 정보를 카드 형태로 표시합니다.
    -   사용자가 '지금 예약하기' 버튼을 클릭하면, `App.tsx`에 있는 `handleBookNow` 함수를 호출하여 예약할 카라반 정보를 상태로 저장합니다.

3.  **`ReservationModal.tsx`**:
    -   `App.tsx`의 상태 변경에 따라 모달 창으로 표시됩니다.
    -   사용자가 시작일과 종료일을 선택하면, `(종료일 - 시작일) * 일일 요금` 공식을 사용해 총 예약금을 계산하여 보여줍니다.
    -   '예약 확정' 버튼을 누르면 `createReservation` API를 호출하여 백엔드에 `POST /api/reservations` 요청을 보냅니다.
    -   요청이 성공하면 `onSuccess` 콜백을 호출하여 `App.tsx`의 상태를 업데이트하고 성공 메시지를 표시합니다.

## 🧪 테스트

프론트엔드 프로젝트에는 기본적인 React 컴포넌트 테스트가 설정되어 있습니다. 아래 명령어로 실행할 수 있습니다.

```bash
# /frontend 디렉터리에서 실행
npm test
```

## ☁️ 배포 아이디어

이 프로젝트를 클라우드(AWS, GCP 등) 서버에 배포하려면 다음과 같은 접근 방식을 고려할 수 있습니다.

-   **백엔드 (FastAPI)**:
    -   `Gunicorn`과 `Uvicorn` 워커를 사용하여 프로덕션 환경에서 FastAPI 앱을 실행합니다.
    -   `systemd`나 `PM2` 같은 프로세스 관리 도구를 사용해 앱을 서비스로 등록하여 안정적으로 운영합니다.
    -   `Nginx`를 리버스 프록시로 앞에 두어 로드 밸런싱, SSL 처리, 정적 파일 서빙 등을 담당하게 합니다.

-   **프론트엔드 (React)**:
    -   `npm run build` 명령어로 프로젝트를 정적 파일(HTML, CSS, JS)로 빌드합니다.
    -   빌드 결과물(`frontend/build` 디렉터리)을 `Nginx`가 직접 서빙하도록 설정합니다.
    -   `/api/*` 경로로 들어오는 요청만 백엔드 FastAPI 서버로 포워딩하도록 `Nginx`를 구성합니다.

## 📅 향후 개선 계획

-   **로그인/회원가입**: JWT 토큰 기반의 인증 시스템을 도입하여 사용자별 기능을 제공합니다.
-   **소셜 로그인**: Google, Kakao 등 OAuth 2.0을 이용한 간편 로그인 기능을 추가합니다.
-   **데이터베이스 연동**: 현재 메모리 기반인 데이터 저장소를 PostgreSQL, MySQL 등 실제 DB로 교체합니다.
-   **예약 관리**: 사용자가 자신의 예약 내역을 확인하고 관리(취소 등)할 수 있는 '마이페이지'를 구현합니다.
-   **카라반 상세 페이지**: 각 카라반의 더 자세한 정보(어메니티, 상세 사진 등)를 볼 수 있는 별도 페이지를 추가합니다.
