import React, { useEffect, useState, useCallback } from 'react';
import { Sparkles, RefreshCw } from 'lucide-react';
import type { FilterSettings, Movie, SwipeDirection, UserProfile } from './types';
import { fetchProfile, fetchRecommendations, sendSwipe, sendUndo } from './api';
import { CardDeck } from './components/CardDeck';
import { ListsTab } from './components/ListsTab';
import { FiltersTab } from './components/FiltersTab';
import { BottomNav, type TabType } from './components/BottomNav';
import { initTelegramApp, hapticImpact } from './telegram';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('deck');
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [history, setHistory] = useState<{ movie: Movie; action: SwipeDirection }[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const [filters, setFilters] = useState<FilterSettings>({
    genre: 'Все',
    type: 'ALL',
    minRating: 0,
    minYear: 0,
  });

  const loadProfile = useCallback(async () => {
    try {
      const p = await fetchProfile();
      setProfile(p);
    } catch (e) {
      console.warn("Could not load profile:", e);
    }
  }, []);

  // Инициализация Telegram WebApp
  useEffect(() => {
    initTelegramApp();
    loadProfile();
  }, [loadProfile]);

  // Загрузка рекомендаций
  const loadRecommendations = useCallback(async (currentFilters: FilterSettings, resetQueue = false) => {
    setLoading(true);
    try {
      const recs = await fetchRecommendations(currentFilters, 15);
      setMovies((prev) => (resetQueue ? recs : [...prev, ...recs.filter(r => !prev.some(p => p.id === r.id))]));
    } catch (e) {
      console.error("Error fetching recommendations:", e);
    } finally {
      setLoading(false);
    }
  }, []);

  // Первоначальная загрузка
  useEffect(() => {
    loadRecommendations(filters, true);
  }, [filters, loadRecommendations]);

  // Обработка свайпа
  const handleSwipe = useCallback(async (movie: Movie, direction: SwipeDirection) => {
    // 1. Мгновенно убираем из очереди на фронтенде для 60fps UX
    setMovies((prev) => {
      const nextList = prev.filter((m) => m.id !== movie.id);
      if (nextList.length <= 4) {
        loadRecommendations(filters, false);
      }
      return nextList;
    });

    // 2. Добавляем в стек отмены
    setHistory((prev) => [...prev, { movie, action: direction }]);

    // 3. Отправляем на бэкенд
    const actionMap: Record<SwipeDirection, 'LIKE' | 'DISLIKE' | 'WATCHLIST'> = {
      right: 'LIKE',
      left: 'DISLIKE',
      up: 'WATCHLIST',
    };
    const apiAction = actionMap[direction];

    try {
      await sendSwipe(movie.id, apiAction);
      // Обновляем счетчик
      setProfile((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          stats: {
            ...prev.stats,
            likes: prev.stats.likes + (direction === 'right' ? 1 : 0),
            dislikes: prev.stats.dislikes + (direction === 'left' ? 1 : 0),
            watchlist: prev.stats.watchlist + (direction === 'up' ? 1 : 0),
          },
        };
      });
    } catch (err) {
      console.error("Swipe API error:", err);
    }
  }, [filters, loadRecommendations]);

  // Обработка отмены (Undo)
  const handleUndo = useCallback(async () => {
    if (history.length === 0) return;
    const lastItem = history[history.length - 1];
    setHistory((prev) => prev.slice(0, -1));

    try {
      await sendUndo(lastItem.movie.id);
      // Возвращаем фильм на вершину стека
      setMovies((prev) => [lastItem.movie, ...prev]);

      setProfile((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          stats: {
            ...prev.stats,
            likes: Math.max(0, prev.stats.likes - (lastItem.action === 'right' ? 1 : 0)),
            dislikes: Math.max(0, prev.stats.dislikes - (lastItem.action === 'left' ? 1 : 0)),
            watchlist: Math.max(0, prev.stats.watchlist - (lastItem.action === 'up' ? 1 : 0)),
          },
        };
      });
    } catch (err) {
      console.error("Undo error:", err);
    }
  }, [history]);

  const handleApplyFilters = (newFilters: FilterSettings) => {
    setFilters(newFilters);
    setHistory([]);
    loadRecommendations(newFilters, true);
    setActiveTab('deck');
  };

  return (
    <div className="flex flex-col h-full w-full bg-[#0c0f17] text-white relative select-none">
      {/* Top App Header */}
      <header className="w-full max-w-md mx-auto px-4 pt-3 pb-2 flex items-center justify-between z-30 shrink-0 border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-orange-600 to-amber-500 flex items-center justify-center shadow-lg shadow-orange-900/30">
            <span className="text-base">🎬</span>
          </div>
          <div>
            <h1 className="text-sm font-extrabold tracking-tight text-white flex items-center gap-1.5">
              <span>Кинокладезь</span>
              <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-400 border border-orange-500/30">
                TMA
              </span>
            </h1>
            <p className="text-[10px] font-medium text-slate-400">kino.steins.ru</p>
          </div>
        </div>

        {/* User Stats / Active Filters pill */}
        <div className="flex items-center gap-2">
          {filters.genre !== 'Все' || filters.type !== 'ALL' || filters.minRating > 0 ? (
            <button
              onClick={() => {
                hapticImpact('light');
                setActiveTab('filters');
              }}
              className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/30 text-[11px] font-bold"
            >
              <Sparkles size={11} />
              <span>Фильтры</span>
            </button>
          ) : null}

          <button
            onClick={() => {
              hapticImpact('light');
              loadRecommendations(filters, true);
            }}
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 active:scale-95 text-slate-300 border border-white/10 transition-all"
            title="Обновить рекомендации"
          >
            <RefreshCw size={15} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </header>

      {/* Main Tab View */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        {activeTab === 'deck' && (
          <CardDeck
            movies={movies}
            onSwipe={handleSwipe}
            onUndo={handleUndo}
            canUndo={history.length > 0}
            isLoading={loading}
            onRefresh={() => loadRecommendations(filters, true)}
            onOpenFilters={() => setActiveTab('filters')}
          />
        )}

        {activeTab === 'lists' && (
          <ListsTab onOpenDeck={() => setActiveTab('deck')} />
        )}

        {activeTab === 'filters' && (
          <FiltersTab
            currentFilters={filters}
            onApplyFilters={handleApplyFilters}
            onClose={() => setActiveTab('deck')}
          />
        )}
      </main>

      {/* Bottom Navigation */}
      <BottomNav
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        watchlistCount={profile?.stats.watchlist || 0}
      />
    </div>
  );
};

export default App;
