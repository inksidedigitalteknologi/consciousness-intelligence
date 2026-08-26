import React, { createContext, useContext, useEffect, useState, useRef, useCallback } from 'react';
import io, { Socket } from 'socket.io-client';

interface WebSocketContextType {
  isConnected: boolean;
  isConnecting: boolean;
  lastMessage: any | null;
  lastError: string | null;
  reconnectAttempts: number;
  sendMessage: (data: any) => boolean;
  subscribe: (channel: string, callback: (data: any) => void) => () => void;
  unsubscribe: (channel: string, callback: (data: any) => void) => void;
  reconnect: () => void;
  disconnect: () => void;
  getConnectionStatus: () => string;
}

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

// Gunakan HTTP (bukan WS) untuk Socket.IO
const SOCKET_URL = import.meta.env.VITE_WS_URL || 'http://45.41.204.21';

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [lastMessage, setLastMessage] = useState<any | null>(null);
  const [lastError, setLastError] = useState<string | null>(null);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  const socketRef = useRef<Socket | null>(null);
  const subscribers = useRef<Map<string, Set<(data: any) => void>>>(new Map());
  const isIntentionalDisconnect = useRef(false);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    if (isIntentionalDisconnect.current) return;
    
    setIsConnecting(true);
    setLastError(null);
    
    try {
      // Socket.IO dengan fallback polling jika websocket gagal
      const socket = io(SOCKET_URL, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: 10,
        reconnectionDelay: 3000,
        reconnectionDelayMax: 10000,
        timeout: 15000,
        autoConnect: true,
        forceNew: true,
      });
      
      socketRef.current = socket;

      socket.on('connect', () => {
        setIsConnected(true);
        setIsConnecting(false);
        setReconnectAttempts(0);
        setLastError(null);
        console.log('🔗 Socket.IO connected to:', SOCKET_URL);
      });

      socket.on('disconnect', (reason) => {
        setIsConnected(false);
        setIsConnecting(false);
        console.log('🔌 Socket.IO disconnected:', reason);
        
        // Jika disconnect karena error, coba reconnect
        if (reason === 'io server disconnect' || reason === 'transport error') {
          if (!isIntentionalDisconnect.current) {
            setTimeout(() => {
              if (socketRef.current && !socketRef.current.connected) {
                socketRef.current.connect();
              }
            }, 3000);
          }
        }
      });

      socket.on('connect_error', (error) => {
        console.error('Socket.IO connection error:', error.message);
        setLastError(`Connection error: ${error.message}`);
        setIsConnecting(false);
        setReconnectAttempts(prev => prev + 1);
      });

      socket.on('reconnect', (attemptNumber) => {
        console.log(`🔄 Socket.IO reconnected after ${attemptNumber} attempts`);
        setIsConnected(true);
        setIsConnecting(false);
        setReconnectAttempts(0);
        setLastError(null);
      });

      socket.on('reconnect_attempt', (attemptNumber) => {
        console.log(`🔄 Socket.IO reconnection attempt ${attemptNumber}`);
        setReconnectAttempts(attemptNumber);
        setIsConnecting(true);
      });

      socket.on('reconnect_error', (error) => {
        console.error('Socket.IO reconnection error:', error.message);
        setLastError(`Reconnection error: ${error.message}`);
      });

      socket.on('reconnect_failed', () => {
        console.error('❌ Socket.IO reconnection failed');
        setLastError('Reconnection failed after maximum attempts');
        setIsConnecting(false);
      });

      // Listen untuk semua channel
      socket.onAny((event, data) => {
        if (event === 'connect' || event === 'disconnect' || event === 'connect_error') {
          return; // Skip internal events
        }
        
        setLastMessage(data);
        
        // Broadcast ke subscribers
        if (data?.channel) {
          const callbacks = subscribers.current.get(data.channel);
          if (callbacks && callbacks.size > 0) {
            callbacks.forEach(cb => {
              try {
                cb(data.payload || data.data);
              } catch (err) {
                console.error('Subscriber callback error:', err);
              }
            });
          }
        } else if (event) {
          // Jika tidak ada channel, broadcast ke semua subscribers yang cocok dengan event name
          const callbacks = subscribers.current.get(event);
          if (callbacks && callbacks.size > 0) {
            callbacks.forEach(cb => {
              try {
                cb(data);
              } catch (err) {
                console.error('Subscriber callback error:', err);
              }
            });
          }
        }
      });

    } catch (error) {
      console.error('Socket.IO connection failed:', error);
      setLastError(error instanceof Error ? error.message : 'Connection failed');
      setIsConnecting(false);
      
      // Retry connection after delay
      if (!isIntentionalDisconnect.current) {
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, 5000);
      }
    }
  }, []);

  useEffect(() => {
    connect();
    
    return () => {
      isIntentionalDisconnect.current = true;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
        reconnectTimeoutRef.current = null;
      }
      if (socketRef.current) {
        socketRef.current.disconnect();
        socketRef.current = null;
      }
    };
  }, [connect]);

  const sendMessage = useCallback((data: any): boolean => {
    if (socketRef.current && socketRef.current.connected) {
      try {
        const message = typeof data === 'string' ? data : JSON.stringify(data);
        socketRef.current.emit('message', message);
        return true;
      } catch (error) {
        console.error('Failed to send message:', error);
        return false;
      }
    }
    console.warn('Socket.IO not connected, message not sent');
    return false;
  }, []);

  const subscribe = useCallback((channel: string, callback: (data: any) => void) => {
    if (!subscribers.current.has(channel)) {
      subscribers.current.set(channel, new Set());
    }
    subscribers.current.get(channel)?.add(callback);
    
    // Return unsubscribe function
    return () => {
      unsubscribe(channel, callback);
    };
  }, []);

  const unsubscribe = useCallback((channel: string, callback: (data: any) => void) => {
    const callbacks = subscribers.current.get(channel);
    if (callbacks) {
      callbacks.delete(callback);
      if (callbacks.size === 0) {
        subscribers.current.delete(channel);
      }
    }
  }, []);

  const reconnect = useCallback(() => {
    disconnect();
    isIntentionalDisconnect.current = false;
    setReconnectAttempts(0);
    setLastError(null);
    setTimeout(() => {
      connect();
    }, 500);
  }, [connect]);

  const disconnect = useCallback(() => {
    isIntentionalDisconnect.current = true;
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    if (socketRef.current) {
      try {
        socketRef.current.disconnect();
      } catch (error) {
        console.error('Disconnect error:', error);
      }
      socketRef.current = null;
    }
    setIsConnected(false);
    setIsConnecting(false);
    setLastError(null);
  }, []);

  const getConnectionStatus = useCallback(() => {
    if (isConnected) return 'connected';
    if (isConnecting) return 'connecting';
    if (reconnectAttempts > 0) return `reconnecting (${reconnectAttempts}/10)`;
    return 'disconnected';
  }, [isConnected, isConnecting, reconnectAttempts]);

  const value: WebSocketContextType = {
    isConnected,
    isConnecting,
    lastMessage,
    lastError,
    reconnectAttempts,
    sendMessage,
    subscribe,
    unsubscribe,
    reconnect,
    disconnect,
    getConnectionStatus,
  };

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within WebSocketProvider');
  }
  return context;
};

export const useWebSocketChannel = (channel: string, callback: (data: any) => void) => {
  const { subscribe, unsubscribe } = useWebSocket();
  useEffect(() => {
    const unsubscribeFn = subscribe(channel, callback);
    return unsubscribeFn;
  }, [channel, callback, subscribe, unsubscribe]);
};

export const useWebSocketStatus = () => {
  const { isConnected, isConnecting, getConnectionStatus } = useWebSocket();
  return { 
    isConnected, 
    isConnecting, 
    status: getConnectionStatus(),
    isReady: isConnected && !isConnecting,
  };
};

export default WebSocketProvider;
