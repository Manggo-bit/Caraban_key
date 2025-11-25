// src/components/AuthPanel.tsx
import React, { useState } from 'react';
import { login, register } from '../api/auth';
import type { LoginResponse } from '../api/auth';
import './AuthPanel.css';

// ✅ 이메일/비밀번호에서 비-ASCII(한글 등) 포함 여부만 검사
// 0x20(공백) ~ 0x7E(일반 ASCII 문자) 범위 밖이 하나라도 있으면 false
const isAsciiSafe = (value: string) => {
  return !/[^\x20-\x7E]/.test(value);
};

type Props = {
  currentUser: LoginResponse | null;
  onLogin: (user: LoginResponse) => void;
  onLogout: () => void;
};

const AuthPanel: React.FC<Props> = ({ currentUser, onLogin, onLogout }) => {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [name, setName] = useState(''); // 닉네임: 한글/영어 다 허용
  const [email, setEmail] = useState('guest@example.com');
  const [password, setPassword] = useState('guest1234');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [info, setInfo] = useState<string | null>(null); // 회원가입 안내 메시지

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setInfo(null);
    setLoading(true);

    try {
      if (mode === 'login') {
        // 🔐 로그인: 성공 시 상위(App)에 로그인 상태 전달
        const user = await login(email, password);
        onLogin(user);
      } else {
        // 🧾 회원가입: 계정만 만들고 자동 로그인은 하지 않음
        await register(name, email, password);

        setInfo('회원가입이 완료되었습니다. 이제 로그인 해 주세요.');
        setMode('login');

        // ✅ 회원가입 후에는 직접 다시 입력하게 초기화
        setEmail('');
        setPassword('');
        setName('');
      }
    } catch (err: any) {
      setError(err.message || '요청 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 이미 로그인된 상태라면
  if (currentUser) {
    return (
      <div className="auth-panel">
        <span>{currentUser.name}님으로 로그인됨</span>
        <button type="button" onClick={onLogout}>
          로그아웃
        </button>
      </div>
    );
  }

  // 로그인/회원가입 폼
  return (
    <div className="auth-panel">
      <div className="auth-tabs">
        <button
          type="button"
          className={mode === 'login' ? 'active' : ''}
          onClick={() => setMode('login')}
        >
          로그인
        </button>
        <button
          type="button"
          className={mode === 'register' ? 'active' : ''}
          onClick={() => setMode('register')}
        >
          회원가입
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {mode === 'register' && (
          <div>
            <input
              type="text"
              placeholder="이름 / 닉네임"
              value={name}
              onChange={(e) => setName(e.target.value)} // 🔹 닉네임은 한글/영어 다 허용
              required
            />
          </div>
        )}
        <div>
          <input
            type="email"
            placeholder="이메일 (영문만)"
            value={email}
            onChange={(e) => {
              const next = e.target.value;
              // 한글 등 비-ASCII가 들어오면 state 업데이트를 아예 하지 않음
              if (!isAsciiSafe(next)) return;
              setEmail(next);
            }}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="비밀번호 (영문/숫자/기호)"
            value={password}
            onChange={(e) => {
              const next = e.target.value;
              if (!isAsciiSafe(next)) return;
              setPassword(next);
            }}
            required
          />
        </div>

        {error && <p className="error-message">{error}</p>}
        {info && <p className="info-message">{info}</p>}

        <button type="submit" disabled={loading}>
          {loading ? '처리 중...' : mode === 'login' ? '로그인' : '회원가입'}
        </button>
      </form>
    </div>
  );
};

export default AuthPanel;
