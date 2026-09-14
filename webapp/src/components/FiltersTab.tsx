import React, { useState, useEffect } from 'react';
import { SlidersHorizontal, RotateCcw, Sparkles } from 'lucide-react';
import type { FilterSettings } from '../types';
import { fetchGenres } from '../api';
import { hapticImpact, hapticNotification } from '../telegram';

interface FiltersTabProps {
  currentFilters: FilterSettings;
  onApplyFilters: (filters: FilterSettings) => void;
  onClose: () => void;
}

export const FiltersTab: React.FC<FiltersTabProps> = ({
  currentFilters,
  onApplyFilters,
  onClose,
}) => {
  const [filters, setFilters] = useState<FilterSettings>(currentFilters);
  const [genres, setGenres] = useState<string[]>([]);

  useEffect(() => {
    fetchGenres().then(setGenres);
  }, []);

  const handleGenreSelect = (g: string) => {
    hapticImpact('light');
    setFilters((prev) => ({ ...prev, genre: g }));
  };

  const handleTypeSelect = (type: 'ALL' | 'FILM' | 'TV_SERIES') => {
    hapticImpact('light');
    setFilters((prev) => ({ ...prev, type }));
  };

  const handleRatingPreset = (rating: number) => {
    hapticImpact('light');
    setFilters((prev) => ({ ...prev, minRating: rating }));
  };

  const handleYearPreset = (year: number) => {
    hapticImpact('light');
    setFilters((prev) => ({ ...prev, minYear: year }));
  };

  const handleReset = () => {
    hapticImpact('medium');
    const defaultFilters: FilterSettings = {
      genre: 'Все',
      type: 'ALL',
      minRating: 0,
      minYear: 0,
    };
    setFilters(defaultFilters);
  };

  const handleApply = () => {
    hapticNotification('success');
    onApplyFilters(filters);
    onClose();
  };

  return (
    <div className="flex-1 flex flex-col w-full max-w-lg mx-auto p-4 overflow-y-auto no-scrollbar pb-10">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-orange-500/20 text-orange-400">
            <SlidersHorizontal size={20} />
          </div>
          <h2 className="text-lg font-bold text-white">Фильтры рекомендаций</h2>
        </div>

        <button
          onClick={handleReset}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white text-xs font-semibold transition-all"
        >
          <RotateCcw size={13} />
          <span>Сбросить</span>
        </button>
      </div>

      {/* Type Selector (Film / Series / All) */}
      <div className="mb-6">
        <label className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-2.5">
          Тип контента
        </label>
        <div className="grid grid-cols-3 gap-2 bg-[#161b26] p-1 rounded-2xl border border-white/10">
          {[
            { id: 'ALL', label: 'Всё подряд' },
            { id: 'FILM', label: 'Только фильмы' },
            { id: 'TV_SERIES', label: 'Сериалы' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => handleTypeSelect(item.id as any)}
              className={`py-2 px-1 text-center rounded-xl text-xs font-bold transition-all ${
                filters.type === item.id
                  ? 'bg-orange-500 text-white shadow-md'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      {/* Genres Chips */}
      <div className="mb-6">
        <label className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-2.5">
          Жанр
        </label>
        <div className="flex flex-wrap gap-2">
          {genres.map((g) => {
            const isSelected = filters.genre.toLowerCase() === g.toLowerCase();
            return (
              <button
                key={g}
                onClick={() => handleGenreSelect(g)}
                className={`px-3 py-2 rounded-xl text-xs font-semibold border transition-all ${
                  isSelected
                    ? 'bg-orange-500/20 border-orange-500 text-orange-300 shadow'
                    : 'bg-[#161b26] border-white/10 text-slate-300 hover:border-white/20'
                }`}
              >
                {g}
              </button>
            );
          })}
        </div>
      </div>

      {/* Rating Filter */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2.5">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Минимальный рейтинг Кинопоиска
          </label>
          <span className="text-xs font-extrabold text-orange-400">
            {filters.minRating === 0 ? 'Любой' : `от ${filters.minRating.toFixed(1)}`}
          </span>
        </div>

        <div className="grid grid-cols-4 gap-2 mb-3">
          {[
            { val: 0, label: 'Любой' },
            { val: 6.5, label: '6.5+' },
            { val: 7.0, label: '7.0+' },
            { val: 8.0, label: '8.0+ Топ' },
          ].map((p) => (
            <button
              key={p.val}
              onClick={() => handleRatingPreset(p.val)}
              className={`py-2 rounded-xl text-xs font-bold border transition-all ${
                filters.minRating === p.val
                  ? 'bg-orange-500 text-white border-orange-500 shadow'
                  : 'bg-[#161b26] text-slate-300 border-white/10 hover:border-white/20'
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>

        <input
          type="range"
          min="0"
          max="8.5"
          step="0.5"
          value={filters.minRating}
          onChange={(e) =>
            setFilters((prev) => ({ ...prev, minRating: parseFloat(e.target.value) }))
          }
          className="w-full accent-orange-500 h-2 bg-slate-800 rounded-lg cursor-pointer"
        />
      </div>

      {/* Year Filter */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2.5">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Год премьеры
          </label>
          <span className="text-xs font-extrabold text-orange-400">
            {filters.minYear === 0 ? 'Любой' : `с ${filters.minYear} года`}
          </span>
        </div>

        <div className="grid grid-cols-4 gap-2">
          {[
            { val: 0, label: 'Все' },
            { val: 2000, label: '2000+' },
            { val: 2010, label: '2010+' },
            { val: 2020, label: '2020+ Новинки' },
          ].map((p) => (
            <button
              key={p.val}
              onClick={() => handleYearPreset(p.val)}
              className={`py-2 rounded-xl text-xs font-bold border transition-all ${
                filters.minYear === p.val
                  ? 'bg-orange-500 text-white border-orange-500 shadow'
                  : 'bg-[#161b26] text-slate-300 border-white/10 hover:border-white/20'
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      {/* Apply Button */}
      <button
        onClick={handleApply}
        className="w-full py-4 rounded-2xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-extrabold text-sm shadow-xl shadow-orange-950/40 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
      >
        <Sparkles size={18} />
        <span>Применить и показать фильмы</span>
      </button>
    </div>
  );
};
