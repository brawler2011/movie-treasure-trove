import React from 'react';
import { Layers, Bookmark, SlidersHorizontal } from 'lucide-react';
import { hapticImpact } from '../telegram';

export type TabType = 'deck' | 'lists' | 'filters';

interface BottomNavProps {
  activeTab: TabType;
  onSelectTab: (tab: TabType) => void;
  watchlistCount?: number;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  activeTab,
  onSelectTab,
  watchlistCount = 0,
}) => {
  const tabs = [
    { id: 'deck' as TabType, label: 'Карточки', icon: Layers },
    { id: 'lists' as TabType, label: 'Мои списки', icon: Bookmark, badge: watchlistCount },
    { id: 'filters' as TabType, label: 'Фильтры', icon: SlidersHorizontal },
  ];

  const handleTabClick = (id: TabType) => {
    if (activeTab !== id) {
      hapticImpact('light');
      onSelectTab(id);
    }
  };

  return (
    <div className="w-full bg-[#121622]/90 backdrop-blur-lg border-t border-white/10 shrink-0 z-40 px-4 py-2 flex items-center justify-around max-w-md mx-auto">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;

        return (
          <button
            key={tab.id}
            onClick={() => handleTabClick(tab.id)}
            className={`flex flex-col items-center justify-center py-1 px-3 rounded-2xl transition-all relative ${
              isActive ? 'text-orange-400 font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <div className="relative mb-1">
              <Icon size={22} className={isActive ? 'stroke-[2.5]' : 'stroke-[1.8]'} />
              {tab.badge && tab.badge > 0 ? (
                <span className="absolute -top-1.5 -right-2 px-1.5 py-0.2 rounded-full bg-orange-500 text-[10px] text-white font-extrabold shadow">
                  {tab.badge}
                </span>
              ) : null}
            </div>
            <span className="text-[11px]">{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
};
