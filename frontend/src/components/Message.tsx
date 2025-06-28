// Компонент для отображения сообщения в чате
import React from 'react';
import { Message as MessageType } from '../types';
import { User, Bot, Clock } from 'lucide-react';

interface MessageProps {
  message: MessageType;
}

/**
 * Компонент для отображения одного сообщения в чате
 */
export const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const formattedTime = message.timestamp.toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`flex gap-3 p-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Аватар */}
      <div className={`
        flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
        ${isUser ? 'bg-primary-500 text-white' : 'bg-gray-200 text-gray-600'}
      `}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Контент сообщения */}
      <div className={`
        flex flex-col max-w-[70%]
        ${isUser ? 'items-end' : 'items-start'}
      `}>
        {/* Облачко сообщения */}
        <div className={`
          px-4 py-2 rounded-lg break-words
          ${isUser 
            ? 'bg-primary-500 text-white rounded-br-sm' 
            : 'bg-gray-100 text-gray-900 rounded-bl-sm'
          }
        `}>
          {/* Основной текст */}
          <div className="whitespace-pre-wrap">{message.content}</div>
          
          {/* Изображение (если есть) */}
          {message.imageData && (
            <div className="mt-3">
              <img 
                src={`data:image/png;base64,${message.imageData}`}
                alt="График"
                className="max-w-full h-auto rounded-lg border border-gray-200"
              />
            </div>
          )}
        </div>

        {/* Время */}
        <div className={`
          flex items-center gap-1 mt-1 text-xs text-gray-500
          ${isUser ? 'flex-row-reverse' : 'flex-row'}
        `}>
          <Clock size={12} />
          <span>{formattedTime}</span>
        </div>
      </div>
    </div>
  );
}; 