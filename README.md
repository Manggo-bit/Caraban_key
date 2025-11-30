# CaravanShare

CaravanShare는 주말 여행이나 장기 모험을 위한 카라반을 쉽게 찾고 예약할 수 있는 웹 애플리케이션입니다. 이 프로젝트는 최신 웹 기술 스택인 **Create-React-App(TypeScript)**과 **FastAPI(Python)**를 사용하여 아이디어를 빠르게 프로토타이핑하는 과정을 보여주기 위해 만들어졌습니다.

현재 이 프로젝트는 카라반 목록을 조회하고, 원하는 날짜를 선택하여 예약하는 핵심 기능을 구현하고 있습니다. 프론트엔드는 `http://localhost:3000`에서, 백엔드 API 서버는 `http://localhost:8000`에서 독립적으로 동작합니다.

## 🌐 데모 URL

[CaravanShare 데모 페이지로 이동](https://manggo-bit.github.io/Caraban_key/)

## 🚀 주요 기능

-   **사용자 인증**: 간단한 사용자 이름과 비밀번호로 로그인할 수 있으며, 예약 기능은 로그인한 사용자만 이용할
    수 있습니다.
-   **카라반 목록 조회**: 등록된 모든 카라반의 사진, 설명, 기본 가격 등의 정보를 한눈에 볼 수 있습니다.
-   **초기 데이터 제공**: `frontend/src/data/caravans.ts` 파일을 통해 미리 정의된 카라반 목록을 화면에
    표시하여, 별도의 데이터베이스 설정 없이도 즉시 기능을 확인할 수 있습니다.
-   **예약 기능**:
    -   '지금 예약하기' 버튼을 통해 예약 모달을 엽니다.
    -   날짜(시작일, 종료일)를 선택하면 실시간으로 총 예약 금액이 계산됩니다.
    -   예약 요청 시 FastAPI 백엔드로 데이터를 전송하여 예약을 생성합니다.
-   **실시간 피드백**: 예약이 성공적으로 완료되면 사용자에게 성공 메시지를 보여줍니다.

## 🛠️ 기술 스택

| 구분 | 기술 | 설명 |
| --- | --- | --- |
| **백엔드** | Python, FastAPI, Uvicorn | 빠르고 현대적인 RESTful API 서버를 구축합니다. |
| **프론트엔드** | React, TypeScript, Create React App | 타입 안정성을 갖춘 동적인 사용자 인터페이스를 구현합니다. |
| **API 통신**| Fetch API | 브라우저 내장 API를 사용하여 백엔드와 비동기 통신을 수행합니다. |
| **데이터 검증**| Pydantic | 백엔드에서 API 요청/응답 데이터의 유효성을 검사합니다. |

프로젝트는 백엔드(루트)와 프론트엔드(`frontend/`) 디렉터리로 명확하게 분리되어 있습니다.

```
/home/tini/Caraban_key/Caraban_key/
├───.gitignore                # 버전 관리 무시 파일 (필요 시 확인)
├───api.py                    # FastAPI 애플리케이션의 메인 엔트리 포인트
├───ARCHITECTURE.md           # 아키텍처 문서
├───DESIGN.md                 # 디자인 문서
├───main.py                   # (메인 실행 스크립트일 수 있음)
├───package.json              # Node.js 프로젝트 설정 (전역)
├───README.md                 # 프로젝트 설명 파일
├───requirements.txt          # Python 백엔드 의존성 목록
├───src/                      # 백엔드 소스 코드
│   ├───exceptions/           # 예외 처리
│   │   └───reservation.py
│   ├───models/               # 데이터 모델 (Caravan, Reservation 등)
│   │   ├───caravan.py
│   │   ├───payment.py
│   │   ├───reservation.py
│   │   ├───review.py
│   │   └───user.py
│   ├───repositories/         # 데이터 접근 로직
│   │   ├───caravan_repository.py
│   │   ├───reservation_repository.py
│   │   └───user_repository.py
│   └───services/             # 핵심 비즈니스 로직
│       ├───reservation_service.py
│       └───reservation_validator.py
├───frontend/                 # React 프론트엔드 프로젝트 루트
│   ├───package.json          # 프론트엔드 Node.js 의존성 및 스크립트
│   └───src/
│       ├───App.tsx           # 메인 애플리케이션 컴포넌트
│       ├───index.tsx         # 애플리케이션 진입점
│       ├───api/              # 백엔드 API 호출 함수
│       │   ├───auth.ts
│       │   ├───caravan.ts
│       │   └───reservation.ts
│       ├───components/       # 재사용 가능한 React 컴포넌트들
│       │   ├───AuthPanel.tsx
│       │   ├───CaravanList.tsx
│       │   └───ReservationModal.tsx
│       └───data/             # 초기 데이터
│           └───caravans.ts
└───tests/                    # 테스트 코드
    ├───test_reservation_service.py
    └───test_reservation_validator.py
```

## 💻 로컬 실행 방법

이 프로젝트를 로컬 환경에서 실행하려면 아래 단계를 순서대로 따르세요. (WSL/Linux 기준)

### 1. 백엔드 서버 실행

먼저 Python으로 작성된 백엔드 API 서버를 실행합니다.

```bash
# 1) 레포지토리 클론 및 이동
git clone <이 레포 주소>
cd <레포지토리 이름>

# 2) Python 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate

# 3) 백엔드 의존성 설치
pip install -r requirements.txt

# 4) 백엔드 서버 실행 (FastAPI)
# --host 0.0.0.0 옵션은 외부 네트워크에서의 접속을 허용합니다.
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```
> 성공적으로 실행되면, 백엔드 서버는 `http://localhost:8000` 에서 요청을 기다립니다.

### 2. 프론트엔드 서버 실행

새로운 터미널을 열고 React로 작성된 프론트엔드 개발 서버를 실행합니다.

```bash
# 1) 프론트엔드 디렉터리로 이동
cd frontend

# 2) 프론트엔드 의존성 설치
npm install

# 3) 프론트엔드 개발 서버 실행
npm start
```
> 성공적으로 실행되면, `http://localhost:3000` 주소의 브라우저가 자동으로 열립니다.

이제 `http://localhost:3000` 으로 접속하여 CaravanShare 서비스를 이용할 수 있습니다.

## 📄 API 요약

| Method | URL | 설명 | 요청 예시 (Body) |
|---|---|---|---|
| `GET` | `/` | API 서버 헬스 체크 | - |
| `GET` | `/api/caravans` | 모든 카라반 목록 조회 | - |
| `POST`| `/api/reservations` | 신규 예약 생성 | `{ "caravan_id": "uuid", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD" }` |

## ✨ 프론트엔드 동작 흐름

1.  **데이터 로딩**: `App.tsx`가 렌더링될 때 `useEffect`를 통해 백엔드 API(`GET /api/caravans`)를 호출하여 카라반 목록을 가져옵니다.
2.  **목록 표시**: 가져온 데이터를 `CaravanList.tsx` 컴포넌트에 전달하여 화면에 카라반 목록을 표시합니다.
3.  **예약 시작**: 사용자가 '지금 예약하기' 버튼을 누르면, 해당 카라반 정보가 `App.tsx`의 상태로 저장되고, 이 정보를 바탕으로 `ReservationModal.tsx`가 화면에 나타납니다.
4.  **예약 처리**: 사용자가 모달에서 날짜를 선택하고 '예약 확정'을 누르면, `ReservationModal.tsx`가 백엔드에 예약 정보(`caravan_id`, `start_date`, `end_date`)를 담아 `POST /api/reservations` API를 호출합니다.
5.  **결과 피드백**: API 호출이 성공하면 모달을 닫고 성공 메시지를 사용자에게 보여줍니다. 실패 시 에러 메시지를 `alert`로 표시합니다.

## 📅 향후 개선 아이디어

-   **로그인/회원가입**: JWT 토큰 기반의 인증 시스템을 도입하여 사용자별 기능을 제공합니다.
-   **데이터베이스 연동**: 현재 메모리 기반인 데이터 저장소를 PostgreSQL, MySQL 등 실제 DB로 교체합니다.
-   **예약 관리 페이지**: 사용자가 자신의 예약 내역을 확인하고 관리(취소 등)할 수 있는 '마이페이지'를 구현합니다.
-   **카라반 상세 페이지**: 각 카라반의 더 자세한 정보(어메니티, 상세 사진 등)를 볼 수 있는 별도 페이지를 추가합니다.
-   **검색 및 필터링**: 위치, 가격, 날짜 등으로 카라반을 검색하고 필터링하는 기능을 추가합니다.
-   **결제 시스템 연동**: 실제 예약 과정에 결제 기능을 추가하여 사용자가 예약과 동시에 결제를 완료할 수 있도록 합니다.
-   **리뷰 및 평점 기능**: 사용자가 이용 후기를 작성하고 별점을 매길 수 있는 기능을 추가하여 다른 사용자에게 참고 정보를 제공합니다.