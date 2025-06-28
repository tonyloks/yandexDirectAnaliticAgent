import React, { useEffect, useRef } from 'react';
import { Settings, Trash2 } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import { useSettings } from '../hooks/useSettings';
import { Message } from '../components/Message';
import { ChatInput } from '../components/ChatInput';
import { SettingsPanel } from '../components/SettingsPanel';

export const ChatPage: React.FC = () => {
  const { messages, isConnected, isTyping, sendMessage, clearMessages } = useChat();
  const { isSettingsOpen, toggleSettingsPanel, setSettingsOpen } = useSettings();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Автоскролл к последнему сообщению
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Шапка */}
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Yandex Direct Analytics Agent</h1>
          <p className="text-sm text-gray-500">Аналитический помощник для рекламных кампаний</p>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={clearMessages}
            className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors"
            title="Очистить чат"
          >
            <Trash2 size={20} />
          </button>
          
          <button
            onClick={toggleSettingsPanel}
            className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors"
            title="Настройки"
          >
            <Settings size={20} />
          </button>
        </div>
      </header>

      {/* Область сообщений */}
      <main className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-md mx-auto px-4">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Добро пожаловать!
              </h2>
              <p className="text-gray-600 mb-6">
                Я ваш аналитический помощник для работы с данными Яндекс.Директ. 
                Могу помочь с анализом кампаний, построением отчетов и визуализацией данных.
              </p>
              <div className="bg-gray-100 rounded-lg p-4 text-sm text-gray-700">
                <p className="font-medium mb-2">Примеры запросов:</p>
                <ul className="space-y-1 text-left">
                  <li>• Покажи баланс аккаунта</li>
                  <li>• Загрузи статистику за последний месяц</li>
                  <li>• Построй график расходов по кампаниям</li>
                  <li>• Какие ключевые слова самые эффективные?</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="pb-4">
            {messages.map((message) => (
              <Message key={message.id} message={message} />
            ))}
            
            {/* Индикатор печати */}
            {isTyping && (
              <div className="flex gap-3 p-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                  <div className="flex gap-1">
                    <div className="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-1 h-1 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
                <div className="flex items-center">
                  <span className="text-sm text-gray-500">Агент печатает...</span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      {/* Поле ввода */}
      <ChatInput
        onSendMessage={sendMessage}
        isConnected={isConnected}
        isTyping={isTyping}
      />

      {/* Панель настроек */}
      <SettingsPanel
        isOpen={isSettingsOpen}
        onClose={() => setSettingsOpen(false)}
      />
    </div>
  );
}; 