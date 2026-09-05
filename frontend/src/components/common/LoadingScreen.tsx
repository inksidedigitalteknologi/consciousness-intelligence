import React from 'react';

// ============================================================
// LOADING SCREEN PROPS
// ============================================================

interface LoadingScreenProps {
  message?: string;
  subtitle?: string;
  showSpinner?: boolean;
}

// ============================================================
// LOADING SCREEN COMPONENT
// ============================================================

export const LoadingScreen: React.FC<LoadingScreenProps> = ({
  message = 'Loading Inkside Digital...',
  subtitle = 'Connecting to backend...',
  showSpinner = true,
}) => {
  return (
    <div className="flex h-screen w-screen bg-[#0B0F14] items-center justify-center">
      <div className="text-center">
        {/* Icon */}
        <div className="text-5xl mb-4 animate-pulse">🧠</div>
        
        {/* Title */}
        <h1 className="text-2xl font-light text-white mb-1">{message}</h1>
        
        {/* Subtitle */}
        <p className="text-gray-500 text-sm animate-pulse">{subtitle}</p>
        
        {/* Spinner */}
        {showSpinner && (
          <div className="mt-6 flex justify-center">
            <div className="w-10 h-10 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin" />
          </div>
        )}
        
        {/* Loading Dots */}
        <div className="mt-4 flex justify-center gap-2">
          <div className="w-2 h-2 bg-blue-500/50 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-blue-500/50 rounded-full animate-bounce" style={{ animationDelay: '200ms' }} />
          <div className="w-2 h-2 bg-blue-500/50 rounded-full animate-bounce" style={{ animationDelay: '400ms' }} />
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen;
