import React, { useState, useEffect } from 'react';
import { Bookmark, Heart, Star, Trash2, Film, RefreshCw } from 'lucide-react';
import type { Movie } from '../types';
import { deleteFromList, fetchLists } from '../api';
import { DetailModal } from './DetailModal';
import { hapticImpact, hapticNotification } from '../telegram';

interface ListsTabProps {
  onOpenDeck: () => void;
}

export const ListsTab: React.FC<ListsTabProps> = ({ onOpenDeck }) => {
  const [activeTab, setActiveTab] = useState<'watchlist' | 'liked'>('watchlist');
  const [items, setItems] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);

  const loadList = async (type: 'watchlist' | 'liked') => {
    setLoading(true);
    try {
      const data = await fetchLists(type);
      setItems(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadList(activeTab);
  }, [activeTab]);

  const handleDelete = async (movieId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    hapticImpact('medium');
    try {
      await deleteFromList(movieId, activeTab);
      setItems((prev) => prev.filter((m) => m.id !== movieId));
      hapticNotification('success');
    } catch (err) {
      console.error(err);
      hapticNotification('error');
    }
  };

  return (
    <div className="flex-1 flex flex-col w-full max-w-lg mx-auto p-4 overflow-hidden">
      {/* Top Segmented Control */}
      <div className="flex bg-[#161b26] p-1 rounded-2xl border border-white/10 mb-4 shrink-0 shadow-md">
        <button
          onClick={() => {
            hapticImpact('light');
            setActiveTab('watchlist');
          }}
          className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl font-bold text-xs sm:text-sm transition-all ${
            activeTab === 'watchlist'
              ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30 shadow'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Bookmark size={16} className={activeTab === 'watchlist' ? 'fill-amber-400' : ''} />
          <span>Буду смотреть</span>
        </button>
        <button
          onClick={() => {
            hapticImpact('light');
            setActiveTab('liked');
          }}
          className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl font-bold text-xs sm:text-sm transition-all ${
            activeTab === 'liked'
              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <Heart size={16} className={activeTab === 'liked' ? 'fill-emerald-400' : ''} />
          <span>Понравившиеся</span>
        </button>
      </div>

      {/* List Content */}
      <div className="flex-1 overflow-y-auto no-scrollbar pb-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 text-slate-400 gap-3">
            <RefreshCw size={28} className="animate-spin text-orange-400" />
            <span className="text-sm">Загружаем список...</span>
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-center text-slate-400 px-4">
            <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center mb-3">
              {activeTab === 'watchlist' ? (
                <Bookmark size={28} className="text-amber-400" />
              ) : (
                <Heart size={28} className="text-emerald-400" />
              )}
            </div>
            <h4 className="text-lg font-bold text-white mb-1">
              {activeTab === 'watchlist' ? 'Список «Буду смотреть» пуст' : 'Пока нет понравившихся'}
            </h4>
            <p className="text-xs text-slate-400 mb-5 max-w-xs">
              {activeTab === 'watchlist'
                ? 'Свайпайте карточки вверх или нажимайте кнопку с закладкой, чтобы сохранить фильм на вечер.'
                : 'Свайпайте вправо или жмите сердечко, чтобы обучать свой вкус и собирать коллекцию.'}
            </p>
            <button
              onClick={() => {
                hapticImpact('light');
                onOpenDeck();
              }}
              className="px-5 py-2.5 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold text-xs transition-all shadow-md"
            >
              Перейти к фильмам
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {items.map((movie) => (
              <div
                key={movie.id}
                onClick={() => {
                  hapticImpact('light');
                  setSelectedMovie(movie);
                }}
                className="group relative rounded-2xl overflow-hidden bg-[#161b26] border border-white/10 shadow-lg cursor-pointer hover:border-orange-500/50 transition-all flex flex-col aspect-[2/3]"
              >
                {/* Poster */}
                {movie.poster_url_preview || movie.poster_url ? (
                  <img
                    src={movie.poster_url_preview || movie.poster_url!}
                    alt={movie.name_ru}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-slate-600 bg-slate-900">
                    <Film size={32} />
                  </div>
                )}

                {/* Gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/30 to-transparent" />

                {/* Rating Badge */}
                {movie.rating_kinopoisk && (
                  <div className="absolute top-2 left-2 flex items-center gap-1 px-2 py-0.5 rounded-md bg-black/70 backdrop-blur-sm text-xs font-bold text-orange-400 border border-white/10">
                    <Star size={11} className="fill-orange-400" />
                    <span>{movie.rating_kinopoisk.toFixed(1)}</span>
                  </div>
                )}

                {/* Delete button */}
                <button
                  onClick={(e) => handleDelete(movie.id, e)}
                  className="absolute top-2 right-2 p-1.5 rounded-full bg-black/60 hover:bg-rose-900/80 text-white/80 hover:text-rose-300 backdrop-blur-sm border border-white/10 opacity-80 hover:opacity-100 active:scale-90 transition-all"
                  title="Удалить из списка"
                >
                  <Trash2 size={13} />
                </button>

                {/* Bottom title & year */}
                <div className="absolute bottom-2 left-2 right-2">
                  <p className="text-xs font-bold text-white line-clamp-2 leading-tight">
                    {movie.name_ru}
                  </p>
                  {movie.year && (
                    <span className="text-[10px] text-slate-400 font-medium">
                      {movie.year}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Movie Details Modal */}
      <DetailModal
        movie={selectedMovie}
        onClose={() => setSelectedMovie(null)}
      />
    </div>
  );
};
