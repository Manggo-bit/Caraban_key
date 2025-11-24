# CaravanShare

카라반(캠핑 트레일러)을 온라인으로 찾아보고 예약할 수 있는 간단한 웹 애플리케이션입니다.  
사용자는 웹 화면에서 이용 가능한 카라반 목록을 확인하고, 원하는 카라반을 선택해 날짜와 인원을 입력하여 예약을 생성할 수 있습니다.

이 프로젝트는 **프런트엔드(React + TypeScript)** 와 **백엔드(FastAPI)** 가 분리된 구조의 풀스택 예제입니다.

---

## 주요 기능

- **카라반 목록 조회**
  - FastAPI 백엔드에서 `/api/caravans` 엔드포인트로 카라반 목록을 가져옵니다.
  - 프런트엔드에서 카드 UI로 카라반 이미지, 설명, 기본 요금, 최대 인원을 보여줍니다.

- **예약 생성**
  - 사용자가 “지금 예약하기” 버튼을 누르면 예약 모달(팝업)이 열립니다.
  - 예약자 이름, 인원, 시작일/종료일을 입력하면
    - 인원 수와 날짜에 따라 **총 예상 가격**을 계산해서 보여줍니다.
  - “예약하기” 버튼을 누르면 FastAPI의 `/api/reservations` 로 POST 요청을 보내 실제 예약을 생성합니다.
  - 예약이 성공하면 화면 상단에 “성공! ~님, ~ 예약이 완료되었습니다.” 메시지가 잠시 표시됩니다.

- **기본 도메인 모델**
  - **User** (Host / Guest 역할)
  - **Caravan** (위치, 수용 인원, 1박 요금 등)
  - **Reservation** (게스트, 카라반, 시작일, 종료일, 총 금액 등)
  - 현재는 인메모리(in-memory) 저장소를 사용하며, 실제 DB는 연결하지 않았습니다.

> ⚠️ 로그인/회원가입, 소셜 로그인(카카오/네이버/구글) 등은 아직 구현되지 않았으며,  
>   추후 확장 가능한 “다음 단계”로 남겨두었습니다.

---

## 기술 스택

### 프런트엔드

- React
- TypeScript
- create-react-app
- Fetch API

### 백엔드

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

## 폴더 구조 (요약)

프로젝트 루트 기준 구조입니다.

```text
Caraban_key/
├── api.py                 # FastAPI 엔트리포인트
├── main.py                # CLI용 예제 (현재는 주로 api.py 사용)
├── requirements.txt       # 백엔드 Python 패키지 목록
├── src/
│   ├── models/            # 도메인 모델 (User, Caravan, Reservation 등)
│   ├── repositories/      # 인메모리 저장소 구현
│   ├── services/          # 비즈니스 로직 (예약 서비스, 검증 로직 등)
│   └── exceptions/        # 커스텀 예외 정의
└── frontend/
    ├── package.json       # 프론트엔드 의존성
    └── src/
        ├── App.tsx        # 메인 React 컴포넌트
        ├── api/
        │   ├── caravan.ts     # 백엔드에서 카라반 목록 fetch
        │   └── reservation.ts # (옵션) 예약 API 래퍼
        ├── components/
        │   ├── CaravanList.tsx    # 카라반 카드 리스트 표시
        │   └── ReservationModal.tsx # 예약 모달 UI + 예약 요청
        └── data/
            └── caravans.ts   # UI용 더미 카라반 데이터(이미지/설명 등)
