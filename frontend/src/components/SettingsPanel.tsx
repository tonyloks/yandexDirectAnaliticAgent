import React, { useState } from 'react';
import { X, Plus, Trash2, Eye, EyeOff, Save } from 'lucide-react';
import { useSettings } from '../hooks/useSettings';
import { ModelSettings, YandexDirectAccount } from '../types';

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SettingsPanel: React.FC<SettingsPanelProps> = ({ isOpen, onClose }) => {
  const {
    modelSettings,
    accounts,
    updateModelSettings,
    addAccount,
    removeAccount,
    toggleAccount
  } = useSettings();

  const [localModelSettings, setLocalModelSettings] = useState<ModelSettings>(modelSettings);
  const [showApiKey, setShowApiKey] = useState(false);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Настройки</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg">
            <X size={20} />
          </button>
        </div>
        
        <div className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Настройки LLM модели</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">API ключ</label>
              <div className="relative">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  value={localModelSettings.apiKey}
                  onChange={(e) => setLocalModelSettings(prev => ({ ...prev, apiKey: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
                <button
                  type="button"
                  onClick={() => setShowApiKey(!showApiKey)}
                  className="absolute right-3 top-2.5"
                >
                  {showApiKey ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            
            <button
              onClick={() => updateModelSettings(localModelSettings)}
              className="flex items-center gap-2 px-4 py-2 bg-primary-500 text-white rounded-lg"
            >
              <Save size={16} />
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}; 