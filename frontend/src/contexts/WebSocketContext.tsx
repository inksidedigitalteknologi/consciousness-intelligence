// src/contexts/WebSocketContext.tsx
// INKSIDE DIGITAL - WEBSOCKET CONTEXT v2.1
// FIX: Hoisting issue (Cannot access 'M' before initialization)
// FIX: useCallback order, heartbeat reference

import React, { 
  createContext, 
  useContext, 
  useEffect, 
  useState, 
  useRef, 
  useCallback, 
  useMemo,
  ReactNode 
} from 'react';
import io, { Socket, ManagerOptions, SocketOptions } from 'socket.io-client';

// ============================================================
// TYPES
// ============================================================

type ConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'reconnecting' | 'failed';

interface WebSocketContextType {
  isConnected: boolean;
  isConnecting: boolean;
  status: ConnectionStatus;
  lastMessage: any | null;
  lastError: string | null;
  reconnectAttempts: number;
  pingLatency: number | null;
  sendMessage: (data: any) => boolean;
  subscribe: <T = any>(channel: string, callback: (data: T) => void) => () => void;
  unsubscribe: (channel: string, callback: (data: any) => void) => void;
  reconnect: () => void;
  disconnect: () => void;
  getConnectionStatus: () => string;
  ping: () => Promise<number>;
}

interface WebSocketProviderProps {
  children: ReactNode;
  url?: string;
  autoConnect?: boolean;
  debug?: boolean;
  heartbeatInterval?: number;
  maxReconnectionAttempts?: number;
}

// ============================================================
// LOGGER
// ============================================================

const LOG_PREFIX = '[WebSocket]';

const createLogger = (debug: boolean) => ({
  info: (message: string, data?: any) => {
    console.info(`${LOG_PREFIX} ${message}`, data || '');
  },
  warn: (message: string, data?: any) => {
    console.warn(`${LOG_PREFIX} ⚠️ ${message}`, data || '');
  },
  error: (message: string, error?: any) => {
    console.error(`${LOG_PREFIX} ❌ ${message}`, error || '');
  },
  debug: (message: string, data?: any) => {
    if (debug) {
      console.debug(`${LOG_PREFIX} ${message}`, data || '');
    }
  }
});

// ============================================================
// ERROR BOUNDARY
// ============================================================

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class WebSocketErrorBoundary extends React.Component<
  { children: ReactNode; fallback?: ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: ReactNode; fallback?: ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    console.error(`${LOG_PREFIX} ❌ Error Boundary caught error:`, error);
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error(`${LOG_PREFIX} ❌ Component Error:`, { error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl text-rose-400 text-sm">
          <p className="font-bold">WebSocket Error</p>
          <p className="text-xs text-rose-300/70">{this.state.error?.message || 'Unknown error'}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-2 px-3 py-1 bg-rose-500/20 hover:bg-rose-500/30 rounded-lg text-xs transition"
          >
            Retry
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// ============================================================
// CONTEXT
// ============================================================

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

// ============================================================
// PROVIDER
// ============================================================

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
  url: propUrl,
  autoConnect = true,
  debug = false,
  heartbeatInterval = 25000,
  maxReconnectionAttempts = 10,
}) => {
  // ============================================================
  // LOGGER
  // ============================================================
  
  const log = useMemo(() => createLogger(debug), [debug]);

  // ============================================================
  // STATE
  // ============================================================
  
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const [lastMessage, setLastMessage] = useState<any | null>(null);
  const [lastError, setLastError] = useState<string | null>(null);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const [pingLatency, setPingLatency] = useState<number | null>(null);

  // ============================================================
  // REFS
  // ============================================================
  
  const socketRef = useRef<Socket | null>(null);
  const subscribers = useRef<Map<string, Set<(data: any) => void>>>(new Map());
  const isIntentionalDisconnect = useRef(false);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const heartbeatTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const pingStartTimeRef = useRef<number | null>(null);
  const isMounted = useRef(true);
  const heartbeatFnRef = useRef<(() => void) | null>(null);

  // ============================================================
  // CONFIG
  // ============================================================
  
  const SOCKET_URL = propUrl || import.meta.env.VITE_WS_URL || 'http://45.41.204.21';

  // ============================================================
  // SOCKET OPTIONS
  // ============================================================
  
  const getSocketOptions = useCallback((): Partial<ManagerOptions & SocketOptions> => ({
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionAttempts: maxReconnectionAttempts,
    reconnectionDelay: 3000,
    reconnectionDelayMax: 10000,
    timeout: 15000,
    autoConnect: true,
    forceNew: true,
    path: '/socket.io/',
    withCredentials: false,
  }), [maxReconnectionAttempts]);

  // ============================================================
  // PING - DEFINED FIRST (sebelum dipanggil)
  // ============================================================
  
  const ping = useCallback((): Promise<number> => {
    return new Promise((resolve, reject) => {
      if (!socketRef.current || !socketRef.current.connected) {
        reject(new Error('Socket not connected'));
        return;
      }

      pingStartTimeRef.current = performance.now();
      
      const timeout = setTimeout(() => {
        reject(new Error('Ping timeout'));
      }, 5000);

      socketRef.current.emit('ping', (response: any) => {
        clearTimeout(timeout);
        const latency = performance.now() - (pingStartTimeRef.current || 0);
        setPingLatency(latency);
        log.debug(`Ping latency: ${latency.toFixed(2)}ms`);
        resolve(latency);
      });
    });
  }, [log]);

  // ============================================================
  // HEARTBEAT - DEFINED KEDUA (menggunakan ping)
  // ============================================================
  
  const startHeartbeat = useCallback(() => {
    if (heartbeatTimeoutRef.current) {
      clearTimeout(heartbeatTimeoutRef.current);
      heartbeatTimeoutRef.current = null;
    }

    if (!isConnected || !socketRef.current) return;

    heartbeatTimeoutRef.current = setTimeout(() => {
      // Panggil ping menggunakan ref agar tidak hoisting issue
      ping().catch(() => {
        log.warn('Heartbeat ping failed, checking connection...');
        if (socketRef.current && !socketRef.current.connected) {
          log.info('Connection lost, attempting to reconnect...');
          setStatus('reconnecting');
          if (!isIntentionalDisconnect.current) {
            socketRef.current.connect();
          }
        }
      });
      // Schedule next heartbeat
      startHeartbeat();
    }, heartbeatInterval);
  }, [isConnected, heartbeatInterval, log, ping]);

  // Simpan heartbeat ke ref
  useEffect(() => {
    heartbeatFnRef.current = startHeartbeat;
  }, [startHeartbeat]);

  // ============================================================
  // CONNECT
  // ============================================================
  
  const connect = useCallback(() => {
    if (isIntentionalDisconnect.current) {
      log.debug('Intentional disconnect, skipping connect');
      return;
    }

    if (socketRef.current && socketRef.current.connected) {
      log.debug('Already connected');
      return;
    }

    setIsConnecting(true);
    setStatus('connecting');
    setLastError(null);
    log.info('Connecting to Socket.IO server...');

    try {
      const socket = io(SOCKET_URL, getSocketOptions());
      socketRef.current = socket;

      socket.on('connect', () => {
        log.info(`Connected to: ${SOCKET_URL}`);
        setIsConnected(true);
        setIsConnecting(false);
        setStatus('connected');
        setReconnectAttempts(0);
        setLastError(null);
        isIntentionalDisconnect.current = false;
        
        // Gunakan ref untuk heartbeat
        if (heartbeatFnRef.current) {
          heartbeatFnRef.current();
        }
      });

      socket.on('disconnect', (reason) => {
        log.warn(`Disconnected: ${reason}`);
        setIsConnected(false);
        setIsConnecting(false);
        
        if (reason === 'io server disconnect' || reason === 'transport error') {
          setStatus('reconnecting');
          if (!isIntentionalDisconnect.current) {
            log.info('Attempting to reconnect...');
            setTimeout(() => {
              if (socketRef.current && !socketRef.current.connected && !isIntentionalDisconnect.current) {
                socketRef.current.connect();
              }
            }, 3000);
          }
        } else {
          setStatus('disconnected');
        }
      });

      socket.on('connect_error', (error) => {
        log.error('Connection error:', error.message);
        setLastError(`Connection error: ${error.message}`);
        setIsConnecting(false);
        setReconnectAttempts(prev => prev + 1);
        setStatus('reconnecting');
      });

      socket.on('reconnect', (attemptNumber) => {
        log.info(`Reconnected after ${attemptNumber} attempts`);
        setIsConnected(true);
        setIsConnecting(false);
        setStatus('connected');
        setReconnectAttempts(0);
        setLastError(null);
        if (heartbeatFnRef.current) {
          heartbeatFnRef.current();
        }
      });

      socket.on('reconnect_attempt', (attemptNumber) => {
        log.debug(`Reconnection attempt ${attemptNumber}`);
        setReconnectAttempts(attemptNumber);
        setIsConnecting(true);
        setStatus('reconnecting');
      });

      socket.on('reconnect_error', (error) => {
        log.error('Reconnection error:', error.message);
        setLastError(`Reconnection error: ${error.message}`);
      });

      socket.on('reconnect_failed', () => {
        log.error('Reconnection failed after maximum attempts');
        setLastError('Reconnection failed after maximum attempts');
        setIsConnecting(false);
        setStatus('failed');
      });

      socket.on('pong', () => {
        if (pingStartTimeRef.current) {
          const latency = performance.now() - pingStartTimeRef.current;
          setPingLatency(latency);
          log.debug(`Pong received, latency: ${latency.toFixed(2)}ms`);
          pingStartTimeRef.current = null;
        }
      });

      socket.onAny((event, data) => {
        const internalEvents = ['connect', 'disconnect', 'connect_error', 'reconnect', 'reconnect_attempt', 'reconnect_error', 'reconnect_failed', 'ping', 'pong'];
        if (internalEvents.includes(event)) return;
        
        setLastMessage(data);
        log.debug(`Received event: ${event}`, data);

        if (data?.channel) {
          const callbacks = subscribers.current.get(data.channel);
          if (callbacks && callbacks.size > 0) {
            callbacks.forEach(cb => {
              try {
                cb(data.payload || data.data);
              } catch (err) {
                log.error('Subscriber callback error:', err);
              }
            });
          }
        } else if (event) {
          const callbacks = subscribers.current.get(event);
          if (callbacks && callbacks.size > 0) {
            callbacks.forEach(cb => {
              try {
                cb(data);
              } catch (err) {
                log.error('Subscriber callback error:', err);
              }
            });
          }
        }
      });

    } catch (error) {
      log.error('Connection failed:', error);
      setLastError(error instanceof Error ? error.message : 'Connection failed');
      setIsConnecting(false);
      setStatus('failed');
      
      if (!isIntentionalDisconnect.current && isMounted.current) {
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, 5000);
      }
    }
  }, [SOCKET_URL, getSocketOptions, log]);

  // ============================================================
  // DISCONNECT
  // ============================================================
  
  const disconnect = useCallback(() => {
    log.info('Disconnecting...');
    isIntentionalDisconnect.current = true;
    setStatus('disconnected');
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (heartbeatTimeoutRef.current) {
      clearTimeout(heartbeatTimeoutRef.current);
      heartbeatTimeoutRef.current = null;
    }
    
    if (socketRef.current) {
      try {
        socketRef.current.disconnect();
      } catch (error) {
        log.error('Disconnect error:', error);
      }
      socketRef.current = null;
    }
    
    setIsConnected(false);
    setIsConnecting(false);
    setLastError(null);
    setReconnectAttempts(0);
  }, [log]);

  // ============================================================
  // RECONNECT
  // ============================================================
  
  const reconnect = useCallback(() => {
    log.info('Manual reconnect requested');
    disconnect();
    isIntentionalDisconnect.current = false;
    setReconnectAttempts(0);
    setLastError(null);
    setStatus('connecting');
    
    setTimeout(() => {
      if (isMounted.current) {
        connect();
      }
    }, 500);
  }, [disconnect, connect, log]);

  // ============================================================
  // SEND MESSAGE
  // ============================================================
  
  const sendMessage = useCallback((data: any): boolean => {
    if (socketRef.current && socketRef.current.connected) {
      try {
        const message = typeof data === 'string' ? data : JSON.stringify(data);
        socketRef.current.emit('message', message);
        log.debug('Message sent:', message);
        return true;
      } catch (error) {
        log.error('Failed to send message:', error);
        return false;
      }
    }
    log.warn('Socket not connected, message not sent');
    return false;
  }, [log]);

  // ============================================================
  // SUBSCRIBE / UNSUBSCRIBE
  // ============================================================
  
  const subscribe = useCallback(<T = any>(channel: string, callback: (data: T) => void): () => void => {
    if (!subscribers.current.has(channel)) {
      subscribers.current.set(channel, new Set());
    }
    subscribers.current.get(channel)?.add(callback);
    log.debug(`Subscribed to channel: ${channel}`);

    return () => {
      unsubscribe(channel, callback);
    };
  }, [log]);

  const unsubscribe = useCallback((channel: string, callback: (data: any) => void) => {
    const callbacks = subscribers.current.get(channel);
    if (callbacks) {
      callbacks.delete(callback);
      if (callbacks.size === 0) {
        subscribers.current.delete(channel);
        log.debug(`Unsubscribed from channel: ${channel}`);
      }
    }
  }, [log]);

  // ============================================================
  // GET STATUS
  // ============================================================
  
  const getConnectionStatus = useCallback((): string => {
    if (isConnected) return 'connected';
    if (isConnecting) return 'connecting';
    if (reconnectAttempts > 0) return `reconnecting (${reconnectAttempts}/${maxReconnectionAttempts})`;
    return 'disconnected';
  }, [isConnected, isConnecting, reconnectAttempts, maxReconnectionAttempts]);

  // ============================================================
  // EFFECTS
  // ============================================================
  
  useEffect(() => {
    isMounted.current = true;
    
    if (autoConnect) {
      connect();
    }
    
    return () => {
      isMounted.current = false;
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  // ============================================================
  // CONTEXT VALUE
  // ============================================================
  
  const value = useMemo<WebSocketContextType>(() => ({
    isConnected,
    isConnecting,
    status,
    lastMessage,
    lastError,
    reconnectAttempts,
    pingLatency,
    sendMessage,
    subscribe,
    unsubscribe,
    reconnect,
    disconnect,
    getConnectionStatus,
    ping,
  }), [
    isConnected,
    isConnecting,
    status,
    lastMessage,
    lastError,
    reconnectAttempts,
    pingLatency,
    sendMessage,
    subscribe,
    unsubscribe,
    reconnect,
    disconnect,
    getConnectionStatus,
    ping,
  ]);

  // ============================================================
  // RENDER
  // ============================================================
  
  return (
    <WebSocketErrorBoundary>
      <WebSocketContext.Provider value={value}>
        {children}
      </WebSocketContext.Provider>
    </WebSocketErrorBoundary>
  );
};

// ============================================================
// HOOKS
// ============================================================

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};

export const useWebSocketChannel = <T = any>(
  channel: string,
  callback: (data: T) => void,
  dependencies: React.DependencyList = []
) => {
  const { subscribe, unsubscribe } = useWebSocket();
  
  useEffect(() => {
    const unsubscribeFn = subscribe<T>(channel, callback);
    return unsubscribeFn;
  }, [channel, subscribe, unsubscribe, ...dependencies]);
};

export const useWebSocketStatus = () => {
  const { isConnected, isConnecting, status, pingLatency, lastError } = useWebSocket();
  return {
    isConnected,
    isConnecting,
    status,
    pingLatency,
    lastError,
    isReady: isConnected && !isConnecting,
  };
};

// ============================================================
// EXPORT
// ============================================================

export default WebSocketProvider;
