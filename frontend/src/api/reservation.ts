// frontend/src/api/reservation.ts
export type CreateReservationPayload = {
  caravanId: string;
  startDate: string; // "YYYY-MM-DD"
  endDate: string;   // "YYYY-MM-DD"
};

export async function createReservation(payload: CreateReservationPayload) {
  const res = await fetch('http://localhost:8000/api/reservations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      caravan_id: payload.caravanId,
      start_date: payload.startDate,
      end_date: payload.endDate,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || '예약 생성에 실패했습니다.');
  }

  return data;
}