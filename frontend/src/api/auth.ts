// src/api/auth.ts

// 🔹 백엔드에서 로그인/회원가입 응답으로 받는 타입
export type LoginResponse = {
  user_id: string;
  name: string;
  email: string;
  role: 'host' | 'guest';
};

// 🔹 로그인 API
export async function login(email: string, password: string): Promise<LoginResponse> {
  const res = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || '로그인에 실패했습니다.');
  }

  return data;
}

// 🔹 회원가입 API
export async function register(
  name: string,
  email: string,
  password: string
): Promise<LoginResponse> {
  const res = await fetch('http://localhost:8000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || '회원가입에 실패했습니다.');
  }

  return data;
}

// 🔹 isolatedModules가 "이 파일은 모듈이다"라고 확실히 알도록
export {};
