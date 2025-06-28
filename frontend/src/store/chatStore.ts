// Store для управления состоянием чата с помощью Zustand
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { Message, ChatState } from '../types';
import { wsClient } from '../api/websocket';

interface ChatStore extends ChatState {
  // Действия
  addMessage: (message: Message) => void;
  setIsConnected: (connected: boolean) => void;
  setIsTyping: (typing: boolean) => void;
  sendMessage: (content: string) => void;
  clearMessages: () => void;
  connectWebSocket: () => Promise<void>;
  disconnectWebSocket: () => void;
}

export const useChatStore = create<ChatStore>()(
  devtools(
    persist(
      (set: any, get: any) => ({
        // Начальное состояние
        messages: [],
        isConnected: false,
        isTyping: false,
        currentChatId: null,

        // Действия
        addMessage: (message: Message) => {
          set((state: any) => ({
            messages: [...state.messages, message]
          }));
        },

        setIsConnected: (connected: boolean) => {
          set({ isConnected: connected });
        },

        setIsTyping: (typing: boolean) => {
          set({ isTyping: typing });
        },

        sendMessage: (content: string) => {
          // Добавляем сообщение пользователя
          const userMessage: Message = {
            id: Date.now().toString(),
            content,
            role: 'user',
            timestamp: new Date()
          };
          
          get().addMessage(userMessage);
          
          // Отправляем через WebSocket
          wsClient.sendMessage(content);
          
          // Показываем индикатор печати
          get().setIsTyping(true);
        },

        clearMessages: () => {
          set({ messages: [] });
        },

        connectWebSocket: async () => {
          try {
            await wsClient.connect();
            
            // Подписываемся на сообщения
            wsClient.onMessage((wsMessage) => {
              const { addMessage, setIsTyping } = get();
              
              switch (wsMessage.type) {
                case 'message':
                  if (wsMessage.data.message) {
                    addMessage({
                      ...wsMessage.data.message,
                      timestamp: new Date(wsMessage.data.message.timestamp)
                    });
                  }
                  setIsTyping(false);
                  break;
                  
                case 'typing':
                  if (wsMessage.data.isTyping !== undefined) {
                    setIsTyping(wsMessage.data.isTyping);
                  }
                  break;
                  
                case 'error':
                  console.error('WebSocket ошибка:', wsMessage.data.error);
                  setIsTyping(false);
                  break;
              }
            });
            
            // Подписываемся на изменения соединения
            wsClient.onConnectionChange((connected) => {
              get().setIsConnected(connected);
            });
            
          } catch (error) {
            console.error('Ошибка подключения WebSocket:', error);
          }
        },

        disconnectWebSocket: () => {
          wsClient.disconnect();
          set({ isConnected: false });
        }
      }),
      {
        name: 'chat-storage',
        partialize: (state: any) => ({ 
          messages: state.messages,
          currentChatId: state.currentChatId 
        })
      }
    ),
    {
      name: 'chat-store'
    }
  )
); 