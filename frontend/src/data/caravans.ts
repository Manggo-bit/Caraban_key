export type Caravan = {
  id: number;
  name: string;
  description: string;
  basePrice: number;
  baseGuests: number;
  extraPersonPrice: number;
  imageUrl: string;
  maxGuests: number;
};

export const caravans: Caravan[] = [
  {
    id: 1,
    name: '모던 익스플로러',
    description: '커플에게 완벽한 세련되고 현대적인 카라반입니다. 완비된 주방과 편안한 침실 공간을 갖추고 있습니다.',
    basePrice: 120000,
    baseGuests: 2,
    extraPersonPrice: 0, // No extra charge as max guests is 2
    imageUrl: '/images/modern-explorer.png',
    maxGuests: 2,
  },
  {
    id: 2,
    name: '패밀리 보이저',
    description: '넓고 가족 친화적인 이 카라반은 최대 6명까지 수용 가능합니다. 욕실과 엔터테인먼트 시스템이 포함되어 있습니다.',
    basePrice: 180000,
    baseGuests: 4,
    extraPersonPrice: 20000,
    imageUrl: '/images/family-voyager.png',
    maxGuests: 6,
  },
  {
    id: 3,
    name: '레트로 어드벤처러',
    description: '향수를 불러일으키는 여행을 위한 클래식한 빈티지 스타일의 카라반입니다. 단순하고 매력적이며 견인하기 쉽습니다.',
    basePrice: 95000,
    baseGuests: 2,
    extraPersonPrice: 15000,
    imageUrl: '/images/retro-adventurer.png',
    maxGuests: 3,
  },
  {
    id: 4,
    name: '오프로드 비스트',
    description: '야생을 위해 제작된 이 견고한 카라반은 어떤 지형이든 감당할 수 있습니다. 태양광 패널과 추가 물 저장 공간이 함께 제공됩니다.',
    basePrice: 250000,
    baseGuests: 2,
    extraPersonPrice: 30000,
    imageUrl: '/images/offroad-beast.png',
    maxGuests: 4,
  }
];
