import type { FilterSettings, Movie, UserProfile } from './types';
import { getTelegramInitData } from './telegram';

// Base API URL (относительный путь /api работает отлично и через локальный порт, и через домен kino.steins.ru)
const API_BASE = '/api';

function getHeaders(): HeadersInit {
  const initData = getTelegramInitData();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  if (initData) {
    headers['X-Telegram-Init-Data'] = initData;
  }
  return headers;
}

export async function fetchProfile(): Promise<UserProfile> {
  const res = await fetch(`${API_BASE}/me`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error('Ошибка загрузки профиля');
  return res.json();
}

export async function fetchRecommendations(
  filters: FilterSettings,
  limit: number = 15
): Promise<Movie[]> {
  const params = new URLSearchParams();
  if (filters.genre && filters.genre !== 'Все') {
    params.set('genre', filters.genre);
  }
  if (filters.type && filters.type !== 'ALL') {
    params.set('type', filters.type);
  }
  if (filters.minRating > 0) {
    params.set('min_rating', filters.minRating.toString());
  }
  if (filters.minYear > 1900) {
    params.set('min_year', filters.minYear.toString());
  }
  params.set('limit', limit.toString());

  const res = await fetch(`${API_BASE}/recommendations?${params.toString()}`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error('Ошибка получения рекомендаций');
  const data = await res.json();
  return data.items || [];
}

export async function sendSwipe(
  movieId: number,
  action: 'LIKE' | 'DISLIKE' | 'WATCHLIST' | 'SKIP'
): Promise<void> {
  const res = await fetch(`${API_BASE}/swipe`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ movie_id: movieId, action }),
  });
  if (!res.ok) throw new Error('Ошибка сохранения реакции');
}

export async function sendUndo(movieId?: number): Promise<Movie | null> {
  const res = await fetch(`${API_BASE}/undo`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ movie_id: movieId || null }),
  });
  if (!res.ok) {
    if (res.status === 404) return null;
    throw new Error('Ошибка отмены действия');
  }
  const data = await res.json();
  return data.movie || null;
}

export async function fetchLists(type: 'watchlist' | 'liked'): Promise<Movie[]> {
  const res = await fetch(`${API_BASE}/lists?type=${type}`, {
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error('Ошибка загрузки списков');
  const data = await res.json();
  return data.items || [];
}

export async function deleteFromList(
  movieId: number,
  type: 'watchlist' | 'liked'
): Promise<void> {
  const res = await fetch(`${API_BASE}/lists/${movieId}?type=${type}`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error('Ошибка удаления из списка');
}

export async function fetchGenres(): Promise<string[]> {
  try {
    const res = await fetch(`${API_BASE}/genres`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error();
    const data = await res.json();
    return data.genres || [];
  } catch {
    return [
      'Все',
      'фантастика',
      'драма',
      'комедия',
      'триллер',
      'боевик',
      'детектив',
      'криминал',
      'приключения',
      'фэнтези',
      'ужасы',
    ];
  }
}
