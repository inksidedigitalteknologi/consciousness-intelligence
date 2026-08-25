/**
 * WebSocket Hook - v1.0.0
 * Real-time data streaming for PredictionView
 */

import { useEffect, useState, useRef, useCallback } from 'react';

// ============================================================
// TYPES
// ============================================================

interface WebSocketOptions {
  autoReconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  onMessage?: (data: any) => void;
}

interface WebSocketState {
  isConnected: boolean;
  lastMessage: string | null;
  lastError: Event | null;
  reconnectAttempts: number;
}

// ============================================================
// HOOK
// ============================================================

const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://localhost:5001';

export function useWebSocket(
  path: string,
  options: WebSocketOptions = {}
) {
  const {
    autoReconnect = true,
    reconnectInterval = 3000,
    maxReconnectAttempts = 10,
    onOpen,
    onClose,
    onError,
    onMessage,
  } = options;

  // ============================================================
  // STATE
  // ============================================================
  
  const [state, setState] = useState<WebSocketState>({
    isConnected: false,
    lastMessage: null,
    lastError: null,
    reconnectAttempts: 0,
  });

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const isMountedRef = useRef(true);

  // ============================================================
  // CONNECT / DISCONNECT
  // ============================================================
  
  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(`${WS_BASE}${path}`);
      wsRef.current = ws;

      ws.onopen = () => {
        if (!isMountedRef.current) return;
        
        setState(prev => ({
          ...prev,
          isConnected: true,
          lastError: null,
          reconnectAttempts: 0,
        }));
        
        console.log(`🔗 WebSocket connected: ${path}`);
        if (onOpen) onOpen();
      };

      ws.onmessage = (event) => {
        if (!isMountedRef.current) return;
        
        setState(prev => ({
          ...prev,
          lastMessage: event.data,
        }));
        
        // Parse and call onMessage callback
        try {
          const data = JSON.parse(event.data);
          if (onMessage) onMessage(data);
        } catch {
          // Jika bukan JSON, kirim raw
          if (onMessage) onMessage(event.data);
        }
      };

      ws.onclose = (event) => {
        if (!isMountedRef.current) return;
        
        setState(prev => ({
          ...prev,
          isConnected: false,
        }));
        
        console.log(`🔌 WebSocket disconnected: ${path}`, event.code, event.reason);
        if (onClose) onClose();

        // Auto-reconnect
        if (autoReconnect && isMountedRef.current) {
          const attempts = state.reconnectAttempts + 1;
          setState(prev => ({
            ...prev,
            reconnectAttempts: attempts,
          }));

          if (attempts <= maxReconnectAttempts) {
            console.log(`🔄 WebSocket reconnecting... (${attempts}/${maxReconnectAttempts})`);
            reconnectTimeoutRef.current = setTimeout(() => {
              connect();
            }, reconnectInterval);
          } else {
            console.log(`❌ WebSocket max reconnect attempts reached: ${path}`);
          }
        }
      };

      ws.onerror = (error) => {
        if (!isMountedRef.current) return;
        
        setState(prev => ({
          ...prev,
          lastError: error,
        }));
        
        console.error(`❌ WebSocket error: ${path}`, error);
        if (onError) onError(error);
      };
    } catch (error) {
      console.error(`❌ WebSocket connection failed: ${path}`, error);
      // Retry connection
      if (autoReconnect && isMountedRef.current) {
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, reconnectInterval);
      }
    }
  }, [path, autoReconnect, reconnectInterval, maxReconnectAttempts, onOpen, onClose, onError, onMessage]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (wsRef.current) {
      if (wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.close(1000, 'Normal closure');
      }
      wsRef.current = null;
    }

    setState(prev => ({
      ...prev,
      isConnected: false,
    }));
  }, []);

  // ============================================================
  // SEND MESSAGE
  // ============================================================
  
  const sendMessage = useCallback((data: string | object) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.warn('⚠️ WebSocket not connected, cannot send message');
      return false;
    }

    try {
      const message = typeof data === 'string' ? data : JSON.stringify(data);
      wsRef.current.send(message);
      return true;
    } catch (error) {
      console.error('❌ Failed to send WebSocket message:', error);
      return false;
    }
  }, []);

  // ============================================================
  // EFFECTS
  // ============================================================
  
  useEffect(() => {
    isMountedRef.current = true;
    connect();

    return () => {
      isMountedRef.current = false;
      disconnect();
    };
  }, [path, connect, disconnect]);

  // ============================================================
  // RETURN
  // ============================================================
  
  return {
    isConnected: state.isConnected,
    lastMessage: state.lastMessage,
    lastError: state.lastError,
    reconnectAttempts: state.reconnectAttempts,
    sendMessage,
    connect,
    disconnect,
    reconnect: connect,
  };
}

export default useWebSocket;
