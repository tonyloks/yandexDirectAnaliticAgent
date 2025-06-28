// Типы для сообщений чата
export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  imageData?: string; // base64 изображение для графиков
}

// Типы для настроек модели
export interface ModelSettings {
  modelName: string;
  apiKey: string;
  temperature: number;
  maxTokens: number;
}

// Типы для WebSocket сообщений
export interface WebSocketMessage {
  type: 'message' | 'typing' | 'error' | 'settings_update';
  data: {
    message?: Message;
    isTyping?: boolean;
    error?: string;
    settings?: ModelSettings;
  };
}

// Типы для аккаунтов Яндекс.Директ
export interface YandexDirectAccount {
  id: string;
  name: string;
  token: string;
  clientId: string;
  isActive: boolean;
  createdAt: Date;
}

// Типы для состояния чата
export interface ChatState {
  messages: Message[];
  isConnected: boolean;
  isTyping: boolean;
  currentChatId: string | null;
}

// Типы для состояния настроек
export interface SettingsState {
  modelSettings: ModelSettings;
  accounts: YandexDirectAccount[];
  isSettingsOpen: boolean;
}

// Типы для ответов API
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
} 