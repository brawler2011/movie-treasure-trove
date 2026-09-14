export interface Movie {
  id: number;
  kinopoisk_id: number;
  name_ru: string;
  name_en?: string | null;
  name_original?: string | null;
  year?: number | null;
  film_length?: number | null;
  rating_kinopoisk?: number | null;
  rating_imdb?: number | null;
  rating_vote_count?: number | null;
  poster_url?: string | null;
  poster_url_preview?: string | null;
  description?: string | null;
  short_description?: string | null;
  type: string;
  genres: string[];
  countries: string[];
  web_url?: string | null;
}

export type SwipeDirection = 'left' | 'right' | 'up';

export interface UserProfile {
  telegram_id: number;
  username?: string | null;
  first_name?: string | null;
  stats: {
    likes: number;
    dislikes: number;
    watchlist: number;
  };
}

export interface FilterSettings {
  genre: string;
  type: 'ALL' | 'FILM' | 'TV_SERIES';
  minRating: number;
  minYear: number;
}
