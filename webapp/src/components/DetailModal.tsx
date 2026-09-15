import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Star, Calendar, Clock, Film, Tv, ExternalLink, Play } from 'lucide-react';
import type { Movie } from '../types';
import { hapticImpact, openExternalLink } from '../telegram';

interface DetailModalProps {
  movie: Movie | null;
  onClose: () => void;
}

export const DetailModal: React.FC<DetailModalProps> = ({ movie, onClose }) => {
  if (!movie) return null;

  const isSeries = ['TV_SERIES', 'MINI_SERIES', 'TV_SHOW'].includes((movie.type || '').toUpperCase());
  const typeLabel = (movie.type || '').toUpperCase() === 'MINI_SERIES' ? 'Мини-сериал' : (isSeries ? 'Сериал' : 'Фильм');

  const formatLength = (minutes?: number | null) => {
    if (!minutes) return null;
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    if (h > 0) return `${h} ч ${m > 0 ? `${m} мин` : ''}`;
    return `${m} мин`;
  };

  const handleClose = () => {
    hapticImpact('light');
    onClose();
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={handleClose}
          className="absolute inset-0 bg-black/80 backdrop-blur-md"
        />

        {/* Modal content */}
        <motion.div
          initial={{ y: '100%', opacity: 0.5 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: '100%', opacity: 0 }}
          transition={{ type: 'spring', damping: 26, stiffness: 280 }}
          className="relative w-full max-w-lg max-h-[85vh] overflow-y-auto no-scrollbar rounded-t-3xl sm:rounded-3xl bg-[#161b26] border border-white/10 shadow-2xl flex flex-col z-10"
        >
          {/* Header Image & Poster Backdrop */}
          <div className="relative w-full h-72 sm:h-80 bg-slate-900 overflow-hidden shrink-0">
            {movie.poster_url ? (
              <img
                src={movie.poster_url}
                alt={movie.name_ru}
                className="w-full h-full object-cover object-center"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-slate-600">
                <Film size={64} />
              </div>
            )}
            <div className="absolute inset-0 bg-gradient-to-t from-[#161b26] via-[#161b26]/50 to-transparent" />

            {/* Close Button */}
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 p-2.5 rounded-full bg-black/60 text-white/90 hover:bg-black/80 backdrop-blur-md border border-white/10 active:scale-95 transition-all"
            >
              <X size={20} />
            </button>

            {/* Title & Ratings inside header */}
            <div className="absolute bottom-4 left-5 right-5">
              <h2 className="text-2xl sm:text-3xl font-bold text-white leading-tight drop-shadow-md">
                {movie.name_ru}
              </h2>
              {(movie.name_en || movie.name_original) && (
                <p className="text-sm font-medium text-slate-300 drop-shadow mt-0.5">
                  {movie.name_en || movie.name_original}
                </p>
              )}
            </div>
          </div>

          {/* Details Body */}
          <div className="p-5 sm:p-6 space-y-5">
            {/* Meta badges row */}
            <div className="flex flex-wrap items-center gap-2 text-xs font-semibold">
              {movie.rating_kinopoisk && (
                <div className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30">
                  <Star size={13} className="fill-orange-400" />
                  <span>Кинопоиск {movie.rating_kinopoisk.toFixed(1)}</span>
                </div>
              )}
              {movie.rating_imdb && (
                <div className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-yellow-500/20 text-yellow-400 border border-yellow-500/30">
                  <Star size={13} className="fill-yellow-400" />
                  <span>IMDb {movie.rating_imdb.toFixed(1)}</span>
                </div>
              )}
              {movie.year && (
                <div className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  <Calendar size={13} />
                  <span>{movie.year}</span>
                </div>
              )}
              {movie.film_length && (
                <div className="flex items-center gap-1 px-3 py-1.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  <Clock size={13} />
                  <span>{isSeries ? `${formatLength(movie.film_length)} / серия` : formatLength(movie.film_length)}</span>
                </div>
              )}
              <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full ${
                isSeries
                  ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30'
                  : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
              }`}>
                {isSeries ? <Tv size={13} className="text-sky-400" /> : <Film size={13} className="text-blue-400" />}
                <span>{typeLabel}</span>
              </div>
            </div>

            {/* Genres Chips */}
            {movie.genres && movie.genres.length > 0 && (
              <div>
                <h4 className="text-xs uppercase tracking-wider text-slate-400 font-bold mb-2">
                  Жанры
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {movie.genres.map((genre) => (
                    <span
                      key={genre}
                      className="px-2.5 py-1 rounded-lg bg-slate-800/80 text-slate-200 text-xs border border-white/5"
                    >
                      {genre}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Countries */}
            {movie.countries && movie.countries.length > 0 && (
              <div>
                <h4 className="text-xs uppercase tracking-wider text-slate-400 font-bold mb-1">
                  Страны
                </h4>
                <p className="text-sm text-slate-300">
                  {movie.countries.join(', ')}
                </p>
              </div>
            )}

            {/* Synopsis / Description */}
            <div>
              <h4 className="text-xs uppercase tracking-wider text-slate-400 font-bold mb-2">
                О сюжете
              </h4>
              <p className="text-sm sm:text-base leading-relaxed text-slate-300 select-text">
                {movie.description || movie.short_description || 'Описание пока отсутствует.'}
              </p>
            </div>

            {/* Action Links */}
            <div className="pt-2 space-y-2.5">
              {movie.kinopoisk_id && (
                <button
                  type="button"
                  onClick={() => {
                    hapticImpact('medium');
                    openExternalLink(`https://www.kinopoisk.cx/film/${movie.kinopoisk_id}/`);
                  }}
                  className="flex items-center justify-center gap-2 w-full py-3.5 px-4 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-sm shadow-lg shadow-emerald-950/40 active:scale-[0.98] transition-all cursor-pointer"
                >
                  <Play size={18} className="fill-white" />
                  <span>🍿 Смотреть бесплатно</span>
                </button>
              )}

              {movie.web_url && (
                <button
                  type="button"
                  onClick={() => {
                    hapticImpact('light');
                    openExternalLink(movie.web_url!);
                  }}
                  className="flex items-center justify-center gap-2 w-full py-3.5 px-4 rounded-2xl bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-500 hover:to-amber-500 text-white font-bold text-sm shadow-lg shadow-orange-950/40 active:scale-[0.98] transition-all cursor-pointer"
                >
                  <ExternalLink size={18} />
                  <span>Открыть на Кинопоиске</span>
                </button>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
