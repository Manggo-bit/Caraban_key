// src/api/caravan.ts

export type BackendCaravan = {
  id: string;
  host_id: string;
  name: string;
  location: string;
  capacity: number;
  daily_rate: number;
  amenities: string[];
  photos: string[];
  status: string;
};

export async function fetchCaravans(): Promise<BackendCaravan[]> {
  const res = await fetch('http://localhost:8000/api/caravans');
  if (!res.ok) {
    throw new Error('Failed to fetch caravans');
  }
  return res.json();
}