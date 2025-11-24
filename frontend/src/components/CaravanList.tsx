import React from 'react';
import { caravans, Caravan } from '../data/caravans';
import './CaravanList.css';

interface CaravanListProps {
  onBook: (caravan: Caravan) => void;
}

const CaravanList: React.FC<CaravanListProps> = ({ onBook }) => {
  return (
    <div className="caravan-list-container">
      {caravans.map((caravan: Caravan) => (
        <div key={caravan.id} className="caravan-card">
          <img src={caravan.imageUrl} alt={caravan.name} className="caravan-image" />
          <div className="caravan-details">
            <h3>{caravan.name}</h3>
            <p>{caravan.description}</p>
            <div className="caravan-booking">
              <span className="caravan-price">₩{caravan.basePrice.toLocaleString()} / 일 (기본 {caravan.baseGuests}인)</span>
              <button className="book-now-button" onClick={() => onBook(caravan)}>
                지금 예약하기
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CaravanList;
