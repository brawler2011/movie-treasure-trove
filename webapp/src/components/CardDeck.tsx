import React, { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { RotateCcw, X, Bookmark, Heart, Info, RefreshCw, SlidersHorizontal, Sparkles } from 'lucide-react';
import type { Movie, SwipeDirection } from '../types';
import { SwipeCard } from './SwipeCard';
import { DetailModal } from './DetailModal';
import { hapticImpact } from '../telegram';

interface CardDeckProps {
  movies: Movie[];
  onSwipe: (movie: Movie, direction: SwipeDirection) => void;
  onUndo: () => void;
  canUndo: boolean;
  isLoading: boolean;
  onRefresh: () => void;
  onOpenFilters: () => void;
}

export const CardDeck: React.FC<CardDeckProps> = ({
  movies,
  onSwipe,
  onUndo,
  canUndo,
  isLoading,
  onRefresh,
  onOpenFilters,
}) => {
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);

  const topMovie = movies[0];
  const nextMovie = movies[1];
  const thirdMovie = movies[2];

  const handleActionClick = (direction: SwipeDirection) => {
    if (!topMovie) return;
    hapticImpact(direction === 'right' ? 'heavy' : 'medium');
    onSwipe(topMovie, direction);
  };

  const handleUndoClick = () => {
    if (!canUndo) return;
    hapticImpact('medium');
    onUndo();
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-between p-4 max-w-md w-full mx-auto relative overflow-hidden">
      {/* Top Deck Area */}
      <div className="relative w-full flex-1 flex items-center justify-center my-2 max-h-[72vh]">
        {isLoading && movies.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-3 text-slate-400">
            <RefreshCw size={36} className="animate-spin text-orange-400" />
            <p className="text-sm font-medium">Подбираем персональные фильмы...</p>
          </div>
        ) : movies.length === 0 ? (
          /* Empty Deck State */
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="w-full h-full max-h-[500px] rounded-3xl bg-[#161b26] border border-white/10 p-6 flex flex-col items-center justify-center text-center shadow-xl"
          >
            <div className="w-16 h-16 rounded-full bg-orange-500/20 text-orange-400 flex items-center justify-center mb-4">
              <Sparkles size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Фильмы закончились!</h3>
            <p className="text-sm text-slate-400 mb-6 max-w-xs">
              Вы просмотрели всю актуальную подборку по текущим фильтрам.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 w-full max-w-xs">
              <button
                onClick={() => {
                  hapticImpact('medium');
                  onRefresh();
                }}
                className="flex items-center justify-center gap-2 w-full py-3 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold text-sm transition-all"
              >
                <RefreshCw size={16} />
                <span>Обновить ленту</span>
              </button>
              <button
                onClick={() => {
                  hapticImpact('light');
                  onOpenFilters();
                }}
                className="flex items-center justify-center gap-2 w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-sm transition-all"
              >
                <SlidersHorizontal size={16} />
                <span>Сменить фильтры</span>
              </button>
            </div>
          </motion.div>
        ) : (
          /* Cards Deck */
          <div className="relative w-full h-full max-w-sm aspect-[2/3] max-h-[560px] touch-none select-none">
            {/* 3rd Card in stack */}
            {thirdMovie && (
              <div className="absolute inset-0 rounded-3xl bg-[#161b26] border border-white/5 shadow-sm scale-[0.88] translate-y-7 opacity-40 transition-transform duration-300 pointer-events-none will-change-transform" />
            )}

            {/* 2nd Card in stack */}
            {nextMovie && (
              <div className="absolute inset-0 rounded-3xl bg-[#161b26] border border-white/10 shadow-md scale-[0.94] translate-y-3.5 opacity-80 transition-transform duration-300 pointer-events-none overflow-hidden will-change-transform">
                {nextMovie.poster_url && (
                  <img
                    src={nextMovie.poster_url}
                    alt={nextMovie.name_ru}
                    loading="lazy"
                    decoding="async"
                    className="w-full h-full object-cover opacity-60 pointer-events-none select-none"
                  />
                )}
                <div className="absolute inset-0 bg-black/40" />
              </div>
            )}

            {/* Active Top Card */}
            <AnimatePresence mode="popLayout">
              {topMovie && (
                <SwipeCard
                  key={topMovie.id}
                  movie={topMovie}
                  isTop={true}
                  onSwipe={(dir) => onSwipe(topMovie, dir)}
                  onOpenDetails={() => setSelectedMovie(topMovie)}
                />
              )}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Bottom Action Controls Bar */}
      <div className="w-full max-w-sm flex items-center justify-between px-3 py-3 gap-2 z-30">
        {/* Undo Button */}
        <button
          onClick={handleUndoClick}
          disabled={!canUndo}
          className={`p-3.5 rounded-full border transition-all shadow-md active:scale-90 ${
            canUndo
              ? 'bg-slate-800/90 hover:bg-slate-700 border-slate-600 text-yellow-400 cursor-pointer'
              : 'bg-slate-900/60 border-slate-800 text-slate-600 cursor-not-allowed opacity-40'
          }`}
          title="Отменить последний свайп"
        >
          <RotateCcw size={20} />
        </button>

        {/* Dislike / Nope Button */}
        <button
          onClick={() => handleActionClick('left')}
          disabled={!topMovie}
          className="p-4 rounded-full bg-[#1e2433] hover:bg-[#252c3e] active:scale-90 border border-rose-500/30 text-rose-500 hover:text-rose-400 shadow-lg shadow-rose-950/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          title="Не моё (дизлайк)"
        >
          <X size={26} strokeWidth={2.5} />
        </button>

        {/* Watchlist Button */}
        <button
          onClick={() => handleActionClick('up')}
          disabled={!topMovie}
          className="p-3.5 rounded-full bg-[#1e2433] hover:bg-[#252c3e] active:scale-90 border border-amber-500/30 text-amber-400 hover:text-amber-300 shadow-lg shadow-amber-950/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          title="Буду смотреть (в вишлист)"
        >
          <Bookmark size={22} className="fill-amber-400/20" />
        </button>

        {/* Info Button */}
        <button
          onClick={() => {
            if (topMovie) {
              hapticImpact('light');
              setSelectedMovie(topMovie);
            }
          }}
          disabled={!topMovie}
          className="p-3.5 rounded-full bg-slate-800/90 hover:bg-slate-700 active:scale-90 border border-slate-600 text-blue-400 shadow-md transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          title="Информация о фильме"
        >
          <Info size={20} />
        </button>

        {/* Like Button */}
        <button
          onClick={() => handleActionClick('right')}
          disabled={!topMovie}
          className="p-4 rounded-full bg-[#1e2433] hover:bg-[#252c3e] active:scale-90 border border-emerald-500/30 text-emerald-400 hover:text-emerald-300 shadow-lg shadow-emerald-950/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          title="Нравится (лайк)"
        >
          <Heart size={26} className="fill-emerald-400" />
        </button>
      </div>

      {/* Details Modal */}
      <DetailModal
        movie={selectedMovie}
        onClose={() => setSelectedMovie(null)}
      />
    </div>
  );
};
