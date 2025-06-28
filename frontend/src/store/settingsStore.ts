// Store для управления настройками приложения
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { ModelSettings, YandexDirectAccount, SettingsState } from '../types';

interface SettingsStore extends SettingsState {
  // Действия для настроек модели
  updateModelSettings: (settings: Partial<ModelSettings>) => void;
  resetModelSettings: () => void;
  
  // Действия для аккаунтов
  addAccount: (account: Omit<YandexDirectAccount, 'id' | 'createdAt'>) => void;
  updateAccount: (id: string, updates: Partial<YandexDirectAccount>) => void;
  removeAccount: (id: string) => void;
  toggleAccount: (id: string) => void;
  
  // Действия для UI
  toggleSettingsPanel: () => void;
  setSettingsOpen: (open: boolean) => void;
}

const defaultModelSettings: ModelSettings = {
  modelName: 'anthropic/claude-3-haiku',
  apiKey: '',
  temperature: 0.7,
  maxTokens: 4000
};

export const useSettingsStore = create<SettingsStore>()(
  devtools(
    persist(
      (set: any, get: any) => ({
        // Начальное состояние
        modelSettings: defaultModelSettings,
        accounts: [],
        isSettingsOpen: false,

        // Действия для настроек модели
        updateModelSettings: (settings: Partial<ModelSettings>) => {
          set((state: any) => ({
            modelSettings: { ...state.modelSettings, ...settings }
          }));
        },

        resetModelSettings: () => {
          set({ modelSettings: defaultModelSettings });
        },

        // Действия для аккаунтов
        addAccount: (accountData: Omit<YandexDirectAccount, 'id' | 'createdAt'>) => {
          const newAccount: YandexDirectAccount = {
            ...accountData,
            id: Date.now().toString(),
            createdAt: new Date()
          };
          
          set((state: any) => ({
            accounts: [...state.accounts, newAccount]
          }));
        },

        updateAccount: (id: string, updates: Partial<YandexDirectAccount>) => {
          set((state: any) => ({
            accounts: state.accounts.map((account: YandexDirectAccount) =>
              account.id === id ? { ...account, ...updates } : account
            )
          }));
        },

        removeAccount: (id: string) => {
          set((state: any) => ({
            accounts: state.accounts.filter((account: YandexDirectAccount) => account.id !== id)
          }));
        },

        toggleAccount: (id: string) => {
          set((state: any) => ({
            accounts: state.accounts.map((account: YandexDirectAccount) =>
              account.id === id ? { ...account, isActive: !account.isActive } : account
            )
          }));
        },

        // Действия для UI
        toggleSettingsPanel: () => {
          set((state: any) => ({
            isSettingsOpen: !state.isSettingsOpen
          }));
        },

        setSettingsOpen: (open: boolean) => {
          set({ isSettingsOpen: open });
        }
      }),
      {
        name: 'settings-storage',
        partialize: (state: any) => ({
          modelSettings: state.modelSettings,
          accounts: state.accounts
        })
      }
    ),
    {
      name: 'settings-store'
    }
  )
); 