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
  } catch (e) {
    // Ignore in standard desktop browsers
  }
}

export function hapticNotification(type: 'error' | 'success' | 'warning') {
  try {
    tg()?.HapticFeedback?.notificationOccurred(type);
  } catch (e) {
    // Ignore
  }
}

export function hapticSelection() {
  try {
    tg()?.HapticFeedback?.selectionChanged();
  } catch (e) {
    // Ignore
  }
}
