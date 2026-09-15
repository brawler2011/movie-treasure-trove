// Telegram WebApp helper utilities

declare global {
  interface Window {
    Telegram?: {
      WebApp?: any;
    };
  }
}

export const tg = () => window.Telegram?.WebApp;

export function initTelegramApp() {
  const app = tg();
  if (!app) return;

  try {
    app.ready();
    app.expand();
    // Настраиваем цвета шапки Telegram в цвет темы Cinema
    if (app.setHeaderColor) {
      app.setHeaderColor('#0c0f17');
    }
    if (app.setBackgroundColor) {
      app.setBackgroundColor('#0c0f17');
    }
    // Отключаем вертикальные свайпы закрытия Telegram Mini App,
    // чтобы жесты свайпа карточки на Android не конфликтовали со шторкой Telegram
    if (typeof app.disableVerticalSwipes === 'function') {
      app.disableVerticalSwipes();
    }
  } catch (e) {
    console.warn("Telegram WebApp init error:", e);
  }
}

export function getTelegramInitData(): string {
  return tg()?.initData || '';
}

export function hapticImpact(style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft' = 'medium') {
  try {
    tg()?.HapticFeedback?.impactOccurred(style);
  } catch {
    // Ignore in standard desktop browsers
  }
}

export function hapticNotification(type: 'error' | 'success' | 'warning') {
  try {
    tg()?.HapticFeedback?.notificationOccurred(type);
  } catch {
    // Ignore
  }
}

export function hapticSelection() {
  try {
    tg()?.HapticFeedback?.selectionChanged();
  } catch {
    // Ignore
  }
}

export function openExternalLink(url: string) {
  try {
    const app = tg();
    if (app && typeof app.openLink === 'function') {
      app.openLink(url);
      return;
    }
  } catch {
    // Ignore
  }
  window.open(url, '_blank', 'noopener,noreferrer');
}
