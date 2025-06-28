// Хук для управления настройками
import { useSettingsStore } from '../store/settingsStore';
import { ModelSettings, YandexDirectAccount } from '../types';

/**
 * Хук для работы с настройками приложения
 */
export const useSettings = () => {
  const {
    modelSettings,
    accounts,
    isSettingsOpen,
    updateModelSettings,
    resetModelSettings,
    addAccount,
    updateAccount,
    removeAccount,
    toggleAccount,
    toggleSettingsPanel,
    setSettingsOpen
  } = useSettingsStore();

  // Утилитарные функции
  const getActiveAccounts = () => accounts.filter((account: YandexDirectAccount) => account.isActive);
  
  const getAccountById = (id: string) => accounts.find((account: YandexDirectAccount) => account.id === id);
  
  const hasValidApiKey = () => modelSettings.apiKey.trim().length > 0;
  
  const validateAccount = (account: Omit<YandexDirectAccount, 'id' | 'createdAt'>) => {
    const errors: string[] = [];
    
    if (!account.name.trim()) {
      errors.push('Название аккаунта обязательно');
    }
    
    if (!account.token.trim()) {
      errors.push('Токен доступа обязателен');
    }
    
    if (!account.clientId.trim()) {
      errors.push('ID клиента обязателен');
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
  };

  const addAccountWithValidation = (accountData: Omit<YandexDirectAccount, 'id' | 'createdAt'>) => {
    const validation = validateAccount(accountData);
    
    if (!validation.isValid) {
      throw new Error(validation.errors.join(', '));
    }
    
    addAccount(accountData);
    return true;
  };

  return {
    // Состояние
    modelSettings,
    accounts,
    isSettingsOpen,
    
    // Методы для настроек модели
    updateModelSettings,
    resetModelSettings,
    
    // Методы для аккаунтов
    addAccount: addAccountWithValidation,
    updateAccount,
    removeAccount,
    toggleAccount,
    
    // Методы для UI
    toggleSettingsPanel,
    setSettingsOpen,
    
    // Утилитарные функции
    getActiveAccounts,
    getAccountById,
    hasValidApiKey,
    validateAccount,
    
    // Вычисляемые значения
    hasAccounts: accounts.length > 0,
    activeAccountsCount: getActiveAccounts().length,
    isConfigured: hasValidApiKey() && getActiveAccounts().length > 0
  };
}; 