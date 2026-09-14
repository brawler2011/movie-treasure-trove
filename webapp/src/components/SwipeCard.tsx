import React from 'react';
import { motion, useMotionValue, useTransform, type PanInfo } from 'framer-motion';
import { Star, Info, Film, Heart, X, Bookmark } from 'lucide-react';
import type { Movie, SwipeDirection } from '../types';
import { hapticImpact } from '../telegram';

interface SwipeCardProps {
  movie: Movie;
  isTop: boolean;
  onSwipe: (direction: SwipeDirection) => void;
  onOpenDetails: () => void;
}

export const SwipeCard: React.FC<SwipeCardProps> = ({
  movie,
  isTop,
  onSwipe,
  onOpenDetails,
}) => {
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  // Плавное вращение карточки при горизонтальном свайпе (-18 до +18 градусов)
  const rotate = useTransform(x, [-250, 250], [-18, 18]);

  // Индикаторы реакций, появляющиеся при вытягивании карточки
  const likeOpacity = useTransform(x, [30, 120], [0, 1]);
  const nopeOpacity = useTransform(x, [-30, -120], [0, 1]);
  const watchOpacity = useTransform(y, [-30, -120], [0, 1]);

  const handleDragEnd = (_: any, info: PanInfo) => {
    if (!isTop) return;

    const threshold = 100;
    const velocityThreshold = 400;

    // Свайп вверх (Буду смотреть)
    if (info.offset.y < -threshold || info.velocity.y < -velocityThreshold) {
      hapticImpact('heavy');
      onSwipe('up');
      return;
    }

    // Свайп вправо (Лайк)
    if (info.offset.x > threshold || info.velocity.x > velocityThreshold) {
      hapticImpact('heavy');
      onSwipe('right');
      return;
    }

    // Свайп влево (Дизлайк)
    if (info.offset.x < -threshold || info.velocity.x < -velocityThreshold) {
      hapticImpact('medium');
      onSwipe('left');
      return;
    }
  };

  return (
    <motion.div
      style={{
        x: isTop ? x : 0,
        y: isTop ? y : 0,
        rotate: isTop ? rotate : 0,
      }}
      drag={isTop}
      dragElastic={0.65}
      dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
      onDragEnd={handleDragEnd}
      whileTap={isTop ? { cursor: 'grabbing' } : undefined}
      className={`absolute inset-0 rounded-3xl overflow-hidden shadow-2xl transition-shadow select-none bg-[#161b26] border border-white/10 ${
        isTop ? 'cursor-grab active:cursor-grabbing z-20' : 'z-10'
      }`}
    >
      {/* Movie Poster Full Cover */}
      <div className="relative w-full h-full bg-[#0c0f17]">
        {movie.poster_url ? (
          <img
            src={movie.poster_url}
            alt={movie.name_ru}
            draggable={false}
            className="w-full h-full object-cover object-center pointer-events-none"
          />
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center text-slate-600">
            <Film size={64} className="mb-2" />
            <span className="text-sm font-medium">Нет постера</span>
          </div>
        )}

        {/* Cinematic Gradient Overlays */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/35 to-black/10 pointer-events-none" />

        {/* Top Badges (Rating & Type) */}
        <div className="absolute top-4 left-4 right-4 flex items-center justify-between pointer-events-none z-10">
          {movie.rating_kinopoisk ? (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black/60 backdrop-blur-md border border-white/10 text-white font-bold text-xs shadow-lg">
              <Star size={14} className="fill-orange-400 text-orange-400" />
              <span>{movie.rating_kinopoisk.toFixed(1)}</span>
            </div>
          ) : <div />}

          <div className="px-3 py-1.5 rounded-full bg-black/60 backdrop-blur-md border border-white/10 text-slate-300 font-semibold text-xs shadow-lg">
            {movie.type === 'TV_SERIES' ? 'Сериал' : 'Фильм'}
          </div>
        </div>

        {/* Dynamic Overlay Stamps when swiping */}
        {isTop && (
          <>
            {/* LIKE Stamp */}
            <motion.div
              style={{ opacity: likeOpacity }}
              className="absolute top-16 left-6 rotate-[-18deg] px-4 py-2 rounded-2xl border-4 border-emerald-500 bg-emerald-500/20 backdrop-blur-sm pointer-events-none z-30 shadow-glow-like"
            >
              <div className="flex items-center gap-2 text-emerald-400 font-black tracking-widest text-2xl uppercase">
                <Heart size={28} className="fill-emerald-400" />
                <span>ЛАЙК</span>
              </div>
            </motion.div>

            {/* NOPE Stamp */}
            <motion.div
              style={{ opacity: nopeOpacity }}
              className="absolute top-16 right-6 rotate-[18deg] px-4 py-2 rounded-2xl border-4 border-rose-500 bg-rose-500/20 backdrop-blur-sm pointer-events-none z-30 shadow-glow-dislike"
            >
              <div className="flex items-center gap-2 text-rose-400 font-black tracking-widest text-2xl uppercase">
                <X size={28} />
                <span>НЕ МОЁ</span>
              </div>
            </motion.div>

            {/* WATCHLIST Stamp */}
            <motion.div
              style={{ opacity: watchOpacity }}
              className="absolute bottom-36 left-1/2 -translate-x-1/2 px-5 py-2.5 rounded-2xl border-4 border-amber-500 bg-amber-500/20 backdrop-blur-sm pointer-events-none z-30 shadow-glow-watch"
            >
              <div className="flex items-center gap-2 text-amber-300 font-black tracking-wider text-xl uppercase">
                <Bookmark size={24} className="fill-amber-300" />
                <span>В СПИСОК</span>
              </div>
            </motion.div>
          </>
        )}

        {/* Bottom Movie Info Card */}
        <div className="absolute bottom-0 left-0 right-0 p-5 z-10 flex flex-col justify-end">
          <div className="flex items-end justify-between gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline gap-2 mb-1">
                <h3 className="text-2xl font-extrabold text-white leading-tight truncate">
                  {movie.name_ru}
                </h3>
                {movie.year && (
                  <span className="text-lg font-semibold text-slate-400 shrink-0">
                    {movie.year}
                  </span>
                )}
              </div>

              {movie.genres && movie.genres.length > 0 && (
                <p className="text-xs font-medium text-slate-300 line-clamp-1 mb-2">
                  {movie.genres.slice(0, 3).join(' • ')}
                </p>
              )}

              {/* Short snippet */}
              <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                {movie.short_description || movie.description || ''}
              </p>
            </div>

            {/* Info Trigger Button */}
            <button
              onClick={(e) => {
                e.stopPropagation();
                hapticImpact('light');
                onOpenDetails();
              }}
              className="p-3 rounded-full bg-white/10 hover:bg-white/20 active:scale-90 backdrop-blur-md border border-white/20 text-white shrink-0 transition-all shadow-lg"
              title="Подробнее о фильме"
            >
              <Info size={22} />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};
