import React, { useState } from 'react';
import './App.css';
import CaravanList from './components/CaravanList';
import { Caravan } from './data/caravans';
import ReservationModal from './components/ReservationModal'; // Will be created next

function App() {
  const [bookingCaravan, setBookingCaravan] = useState<Caravan | null>(null);
  const [reservationMessage, setReservationMessage] = useState('');

  // This function will be called from CaravanList
  const handleBookNow = (caravan: Caravan) => {
    setReservationMessage(''); // Clear previous messages
    setBookingCaravan(caravan);
  };

  const handleCloseModal = () => {
    setBookingCaravan(null);
  };

  const handleReservationSuccess = (name: string, caravanName: string) => {
    setBookingCaravan(null); // Close the modal
    setReservationMessage(`성공! ${name}님, ${caravanName} 예약이 완료되었습니다.`);
    // Hide the message after a few seconds
    setTimeout(() => setReservationMessage(''), 5000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>CaravanShare에 오신 것을 환영합니다</h1>
        <p>카라반 렌탈과 모험을 위한 원스톱 솔루션입니다.</p>
      </header>
      <main>
        {reservationMessage && (
          <div className="reservation-success-message">
            {reservationMessage}
          </div>
        )}

        <h2>이용 가능한 카라반</h2>
        <CaravanList onBook={handleBookNow} />

        {/* The modal will be rendered here when a caravan is selected */}
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
