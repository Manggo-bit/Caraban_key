// src/components/ReservationModal.tsx
import React, { useState, useEffect } from 'react';
import { Caravan } from '../data/caravans';
import './ReservationModal.css';

interface ReservationModalProps {
  caravan: Caravan;
  onClose: () => void;
  onSuccess: (name: string, caravanName: string) => void;
}

const ReservationModal: React.FC<ReservationModalProps> = ({
  caravan,
  onClose,
  onSuccess,
}) => {
  const [bookerName, setBookerName] = useState('');
  const [numberOfPeople, setNumberOfPeople] = useState(caravan.baseGuests); // 기본 인원
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [totalPrice, setTotalPrice] = useState(0);

  // 오늘 + 2일 후부터 예약 가능
  const minBookingDate = new Date();
  minBookingDate.setDate(minBookingDate.getDate() + 2);
  const minDateString = minBookingDate.toISOString().split('T')[0];

  // 날짜/인원/카라반 변경될 때마다 총 금액 계산
  useEffect(() => {
    let dailyRate = caravan.basePrice;
    if (numberOfPeople > caravan.baseGuests) {
      dailyRate += (numberOfPeople - caravan.baseGuests) * caravan.extraPersonPrice;
    }

    if (startDate && endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      if (start > end) {
        setTotalPrice(0);
        return;
      }
      const diffTime = Math.abs(end.getTime() - start.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
      setTotalPrice(dailyRate * (diffDays > 0 ? diffDays : 0));
    } else {
      setTotalPrice(0);
    }
  }, [startDate, endDate, numberOfPeople, caravan]);

  const handlePeopleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = parseInt(e.target.value, 10);
    if (isNaN(value)) value = 1;
    if (value < 1) value = 1;
    if (value > caravan.maxGuests) value = caravan.maxGuests;
    setNumberOfPeople(value);
  };

  const handleReservation = async () => {
    if (!bookerName || !startDate || !endDate || numberOfPeople <= 0) {
      alert('모든 필수 정보를 입력해주세요.');
      return;
    }
    if (new Date(startDate) > new Date(endDate)) {
      alert('시작일은 종료일보다 빨라야 합니다.');
      return;
    }
    if (numberOfPeople > caravan.maxGuests) {
      alert(`이 카라반의 최대 수용 인원은 ${caravan.maxGuests}명입니다.`);
      return;
    }
    if (totalPrice === 0) {
      alert('유효한 날짜를 선택하여 가격을 계산해주세요.');
      return;
    }
    if (!caravan.backendId) {
      alert('이 카라반의 서버 ID가 설정되어 있지 않습니다.');
      return;
    }

    try {
      // 🔹 FastAPI로 예약 생성 요청
      const res = await fetch('http://localhost:8000/api/reservations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          caravan_id: caravan.backendId, // uuid 사용
          start_date: startDate,         // YYYY-MM-DD
          end_date: endDate,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || '예약 생성에 실패했습니다.');
      }

      // 🔹 백엔드에서도 성공했을 때만 상위 컴포넌트에 성공 알림
      onSuccess(bookerName, caravan.name);
    } catch (e: any) {
      console.error(e);
      alert(e.message || '예약 처리 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <button className="modal-close-button" onClick={onClose}>
          X
        </button>

        <h2>{caravan.name} 예약</h2>
        <p>최대 수용 인원: {caravan.maxGuests}명</p>

        <img
          src={caravan.imageUrl}
          alt={caravan.name}
          className="modal-caravan-image"
        />

        <p className="modal-caravan-description">{caravan.description}</p>

        <div className="modal-caravan-price">
          <div>기본 {caravan.baseGuests}인: ₩{caravan.basePrice.toLocaleString()}/일</div>
          {caravan.extraPersonPrice > 0 && (
            <div>추가 1인당: ₩{caravan.extraPersonPrice.toLocaleString()}/일</div>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="bookerName">예약자 이름:</label>
          <input
            type="text"
            id="bookerName"
            value={bookerName}
            onChange={(e) => setBookerName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="numberOfPeople">
            인원 (최대 {caravan.maxGuests}명):
          </label>
          <input
            type="number"
            id="numberOfPeople"
            value={numberOfPeople}
            onChange={handlePeopleChange}
            min={1}
            max={caravan.maxGuests}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="startDate">시작일:</label>
          <input
            type="date"
            id="startDate"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            min={minDateString}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="endDate">종료일:</label>
          <input
            type="date"
            id="endDate"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            min={startDate || minDateString}
            required
          />
        </div>

        {totalPrice > 0 && (
          <div className="total-price">
            총 예상 가격: <span>₩{totalPrice.toLocaleString()}</span>
          </div>
        )}

        <button className="reserve-button" onClick={handleReservation}>
          예약하기
        </button>
      </div>
    </div>
  );
};

export default ReservationModal;
