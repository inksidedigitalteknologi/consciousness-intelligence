import React from 'react';

// ============================================================
// ERROR SCREEN PROPS
// ============================================================

interface ErrorScreenProps {
  error: string;
  onRetry: () => void;
  reconnectAttempts?: number;
  isWsConnected?: boolean;
  onReconnectWs?: () => void;
}

// ============================================================
// ERROR SCREEN COMPONENT
// ============================================================

export const ErrorScreen: React.FC<ErrorScreenProps> = ({
  error,
  onRetry,
  reconnectAttempts = 0,
  isWsConnected = false,
  onReconnectWs,
}) => {
  return (
    <div className="flex h-screen w-screen bg-[#0B0F14] items-center justify-center p-4">
      <div className="text-center max-w-md w-full p-8 rounded-2xl bg-red-500/10 border border-red-500/30">
        <div className="text-5xl mb-4">🚫</div>
        <h2 className="text-xl font-semibold text-red-400 mb-2">Connection Error</h2>
        <p className="text-gray-400 text-sm mb-4 leading-relaxed">{error}</p>
        
        <div className="flex flex-col gap-3">
          {/* Retry Button */}
          <button
            onClick={onRetry}
            className="px-6 py-3 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-200 flex items-center justify-center gap-2"
          >
            <span>🔄</span>
            <span>Retry Connection</span>
          </button>
          
          {/* WebSocket Status */}
          {onReconnectWs && (
            <button
              onClick={onReconnectWs}
              className="px-6 py-3 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 text-sm"
            >
              <span>🔌</span>
              <span>
                {isWsConnected ? 'WebSocket Connected' : 'Reconnect WebSocket'}
              </span>
              {reconnectAttempts > 0 && (
                <span className="text-gray-500 text-xs">
                  (Attempts: {reconnectAttempts})
                </span>
              )}
            </button>
          )}
          
          {/* Help Text */}
          <p className="text-gray-500 text-xs mt-2">
            Make sure the backend server is running on port 5001
          </p>
        </div>
      </div>
    </div>
  );
};

export default ErrorScreen;
