// Хук для управления чатом
import { useEffect } from 'react';
import { useChatStore } from '../store/chatStore';

/**
 * Хук для работы с чатом
 * Автоматически подключается к WebSocket при монтировании
 */
export const useChat = () => {
  const {
    messages,
    isConnected,
    isTyping,
    sendMessage,
    clearMessages,
    connectWebSocket,
    disconnectWebSocket
  } = useChatStore();

  // Автоматическое подключение при монтировании компонента
  useEffect(() => {
    if (!isConnected) {
      connectWebSocket();
    }

    // Отключение при размонтировании
    return () => {
      disconnectWebSocket();
    };
  }, [connectWebSocket, disconnectWebSocket, isConnected]);

  return {
    // Состояние
    messages,
    isConnected,
    isTyping,
    
    // Методы
    sendMessage,
    clearMessages,
    
    // Вычисляемые значения
    hasMessages: messages.length > 0,
    lastMessage: messages[messages.length - 1] || null
  };
}; 