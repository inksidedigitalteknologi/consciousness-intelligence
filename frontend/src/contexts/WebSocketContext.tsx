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

  const connect = useCallback(() => {
    if (isIntentionalDisconnect.current) return;
    
    setIsConnecting(true);
    
    try {
      const socket = io(SOCKET_URL, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionAttempts: 10,
        reconnectionDelay: 3000,
        timeout: 10000,
      });
      
      socketRef.current = socket;

      socket.on('connect', () => {
        setIsConnected(true);
        setIsConnecting(false);
        setReconnectAttempts(0);
        setLastError(null);
        console.log('🔗 Socket.IO connected');
      });

      socket.on('disconnect', () => {
        setIsConnected(false);
        setIsConnecting(false);
        console.log('🔌 Socket.IO disconnected');
      });

      socket.on('connect_error', (error) => {
        console.error('Socket.IO connection error:', error);
        setLastError(error.message);
        setIsConnecting(false);
      });

      // Listen untuk semua channel
      socket.onAny((event, data) => {
        setLastMessage(data);
        
        // Broadcast ke subscribers
        if (data?.channel) {
          const callbacks = subscribers.current.get(data.channel);
          if (callbacks) {
            callbacks.forEach(cb => cb(data.payload));
          }
        }
      });

    } catch (error) {
      console.error('Socket.IO connection failed:', error);
      setLastError('Connection failed');
      setIsConnecting(false);
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      isIntentionalDisconnect.current = true;
      if (socketRef.current) {
        socketRef.current.disconnect();
        socketRef.current = null;
      }
    };
  }, [connect]);

  const sendMessage = useCallback((data: any): boolean => {
    if (socketRef.current && socketRef.current.connected) {
      socketRef.current.emit('message', data);
      return true;
    }
    return false;
  }, []);

  const subscribe = useCallback((channel: string, callback: (data: any) => void) => {
    if (!subscribers.current.has(channel)) {
      subscribers.current.set(channel, new Set());
    }
    subscribers.current.get(channel)?.add(callback);
    return () => unsubscribe(channel, callback);
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
    setTimeout(connect, 500);
  }, [connect]);

  const disconnect = useCallback(() => {
    isIntentionalDisconnect.current = true;
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
    }
    setIsConnected(false);
    setIsConnecting(false);
  }, []);

  const getConnectionStatus = useCallback(() => {
    if (isConnected) return 'connected';
    if (isConnecting) return 'connecting';
    if (reconnectAttempts > 0) return 'reconnecting';
    return 'disconnected';
  }, [isConnected, isConnecting, reconnectAttempts]);

  return (
    <WebSocketContext.Provider value={{
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
    }}>
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
  return { isConnected, isConnecting, status: getConnectionStatus() };
};
