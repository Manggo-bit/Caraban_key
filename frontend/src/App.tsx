import React, { useState, useEffect } from 'react';
import './App.css';
import CaravanList from './components/CaravanList';
import { Caravan, caravans as staticCaravans } from './data/caravans';
import ReservationModal from './components/ReservationModal';
import { fetchCaravans, BackendCaravan } from './api/caravan';

import AuthPanel from './components/AuthPanel';
import type { LoginResponse } from './api/auth';

function App() {
  const [currentUser, setCurrentUser] = useState<LoginResponse | null>(null);
  const [bookingCaravan, setBookingCaravan] = useState<Caravan | null>(null);
  const [reservationMessage, setReservationMessage] = useState('');
  const [caravans, setCaravans] = useState<Caravan[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = (user: LoginResponse) => {
    setCurrentUser(user);
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  useEffect(() => {
    const loadCaravans = async () => {
      try {
        const backendCaravans: BackendCaravan[] = await fetchCaravans();

        // 백엔드 데이터 + UI용 데이터 합치기
        const count = Math.min(staticCaravans.length, backendCaravans.length);
        const merged: Caravan[] = [];

        for (let i = 0; i < count; i++) {
          const ui = staticCaravans[i];
          const backend = backendCaravans[i];

          merged.push({
            ...ui,
            backendId: backend.id,         // 예약할 때 쓸 uuid
            basePrice: backend.daily_rate, // 요금은 백엔드 값
            maxGuests: backend.capacity,   // 수용 인원도 백엔드 값
            location: backend.location,
          });
        }

        setCaravans(merged);
      } catch (err) {
        console.error(err);
        setError('카라반 정보를 불러오는 데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };

    loadCaravans();
  }, []);

  const handleBookNow = (caravan: Caravan) => {
    setReservationMessage('');
    setBookingCaravan(caravan);
  };

  const handleCloseModal = () => {
    setBookingCaravan(null);
  };

  const handleReservationSuccess = (name: string, caravanName: string) => {
    setBookingCaravan(null);
    setReservationMessage(`성공! ${name}님, ${caravanName} 예약이 완료되었습니다.`);
    setTimeout(() => setReservationMessage(''), 5000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>CaravanShare에 오신 것을 환영합니다</h1>
        <p>카라반 렌탈과 모험을 위한 원스톱 솔루션입니다.</p>

        
        {/* 🔐 로그인 / 회원가입 패널 */}
        <AuthPanel
          currentUser={currentUser}
          onLogin={handleLogin}
          onLogout={handleLogout}
        />
      </header>
      <main>
        {reservationMessage && (
          <div className="reservation-success-message">
            {reservationMessage}
          </div>
        )}

        <h2>이용 가능한 카라반</h2>

        {loading && <p>로딩 중...</p>}
        {error && <p className="error-message">{error}</p>}
        {!loading && !error && (
          <CaravanList caravans={caravans} onBook={handleBookNow} />
        )}

        {bookingCaravan && (
          <ReservationModal
            caravan={bookingCaravan}
            onClose={handleCloseModal}
            onSuccess={handleReservationSuccess}
          />
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; 2025 CaravanShare. 모든 권리 보유.</p>
      </footer>
    </div>
  );
}

export default App;