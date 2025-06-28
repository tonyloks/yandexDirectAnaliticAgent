// WebSocket клиент для общения с backend
import { WebSocketMessage, Message } from '../types';

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectInterval: number = 5000;
  private maxReconnectAttempts: number = 5;
  private reconnectAttempts: number = 0;
  private messageHandlers: Set<(message: WebSocketMessage) => void> = new Set();
  private connectionHandlers: Set<(connected: boolean) => void> = new Set();

  constructor(url: string = 'ws://localhost:8000/ws/chat') {
    this.url = url;
  }

  /**
   * Подключается к WebSocket серверу
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);
        
        this.ws.onopen = () => {
          console.log('WebSocket соединение установлено');
          this.reconnectAttempts = 0;
          this.notifyConnectionHandlers(true);
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.notifyMessageHandlers(message);
          } catch (error) {
            console.error('Ошибка парсинга WebSocket сообщения:', error);
          }
        };

        this.ws.onclose = () => {
          console.log('WebSocket соединение закрыто');
          this.notifyConnectionHandlers(false);
          this.handleReconnect();
        };

        this.ws.onerror = (error) => {
          console.error('Ошибка WebSocket:', error);
          reject(error);
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Закрывает WebSocket соединение
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Отправляет сообщение через WebSocket
   */
  sendMessage(content: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const message: WebSocketMessage = {
        type: 'message',
        data: {
          message: {
            id: Date.now().toString(),
            content,
            role: 'user',
            timestamp: new Date()
          }
        }
      };
      this.ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket не подключен');
    }
  }

  /**
   * Подписывается на сообщения
   */
  onMessage(handler: (message: WebSocketMessage) => void): () => void {
    this.messageHandlers.add(handler);
    return () => this.messageHandlers.delete(handler);
  }

  /**
   * Подписывается на изменения соединения
   */
  onConnectionChange(handler: (connected: boolean) => void): () => void {
    this.connectionHandlers.add(handler);
    return () => this.connectionHandlers.delete(handler);
  }

  /**
   * Проверяет состояние соединения
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  private notifyMessageHandlers(message: WebSocketMessage): void {
    this.messageHandlers.forEach(handler => handler(message));
  }

  private notifyConnectionHandlers(connected: boolean): void {
    this.connectionHandlers.forEach(handler => handler(connected));
  }

  private handleReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Попытка переподключения ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      
      setTimeout(() => {
        this.connect().catch(error => {
          console.error('Ошибка переподключения:', error);
        });
      }, this.reconnectInterval);
    } else {
      console.error('Превышено максимальное количество попыток переподключения');
    }
  }
}

// Экспорт singleton instance
export const wsClient = new WebSocketClient(); 