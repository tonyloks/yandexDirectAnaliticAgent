// Компонент для ввода сообщений в чат
import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isConnected: boolean;
  isTyping: boolean;
}

/**
 * Компонент для ввода и отправки сообщений
 */
export const ChatInput: React.FC<ChatInputProps> = ({ 
  onSendMessage, 
  isConnected, 
  isTyping 
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Автофокус при монтировании
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  }, []);

  // Автоматическое изменение высоты textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedMessage = message.trim();
    if (!trimmedMessage || !isConnected || isTyping) return;
    
    onSendMessage(trimmedMessage);
    setMessage('');
    
    // Сброс высоты textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const canSend = message.trim().length > 0 && isConnected && !isTyping;

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <form onSubmit={handleSubmit} className="flex gap-3">
        {/* Поле ввода */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              !isConnected 
                ? "Подключение..." 
                : isTyping 
                  ? "Агент печатает..." 
                  : "Введите ваше сообщение..."
            }
            disabled={!isConnected || isTyping}
            className={`
              w-full px-4 py-3 rounded-lg border resize-none
              min-h-[48px] max-h-[120px] overflow-y-auto
              focus:ring-2 focus:ring-primary-500 focus:border-transparent
              disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed
              ${!isConnected ? 'border-red-300' : 'border-gray-300'}
            `}
            rows={1}
          />
          
          {/* Индикатор печати */}
          {isTyping && (
            <div className="absolute right-3 top-3 text-gray-500">
              <Loader2 size={16} className="animate-spin" />
            </div>
          )}
        </div>

        {/* Кнопка отправки */}
        <button
          type="submit"
          disabled={!canSend}
          className={`
            flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center
            transition-all duration-200
            ${canSend
              ? 'bg-primary-500 hover:bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }
          `}
        >
          {isTyping ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </form>

      {/* Статус подключения */}
      <div className="mt-2 flex items-center gap-2 text-xs">
        <div className={`
          w-2 h-2 rounded-full
          ${isConnected ? 'bg-green-500' : 'bg-red-500'}
        `} />
        <span className="text-gray-600">
          {isConnected ? 'Подключено' : 'Отключено'}
        </span>
      </div>
    </div>
  );
}; 