// src/components/HeroCanvas.tsx
// INKSIDE DIGITAL - HERO CANVAS v3.0
// SUPER ADVANCED COGNITIVE NEURAL NETWORK
// 3D Depth, Mouse Interaction, Dynamic Colors, Glow Effects

import React, { useEffect, useRef, useCallback, memo, useState } from 'react';

// ============================================================
// TYPES
// ============================================================

interface Particle {
  x: number;
  y: number;
  z: number; // Depth for 3D effect
  vx: number;
  vy: number;
  vz: number;
  radius: number;
  targetRadius: number;
  color: string;
  hue: number;
  alpha: number;
  targetAlpha: number;
  pulsePhase: number;
  pulseSpeed: number;
  trail: { x: number; y: number; alpha: number }[];
  connections: Set<number>;
}

interface HeroCanvasProps {
  className?: string;
  opacity?: number;
  blur?: string;
  particleCount?: number;
  connectionDistance?: number;
  colors?: string[];
  speed?: number;
  mouseInteraction?: boolean;
  enable3D?: boolean;
  enableTrails?: boolean;
  enableGlow?: boolean;
  showFPS?: boolean;
  backgroundColor?: string;
}

// ============================================================
// LOGGER
// ============================================================

const LOG_PREFIX = '[HeroCanvas]';

const log = {
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
    if (process.env.NODE_ENV === 'development') {
      console.debug(`${LOG_PREFIX} ${message}`, data || '');
    }
  }
};

// ============================================================
// ERROR BOUNDARY
// ============================================================

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class HeroCanvasErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode; fallback?: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    log.error('Error Boundary caught error:', error);
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    log.error('Component Error:', { error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="absolute inset-0 bg-gradient-to-b from-[#0B0F14] to-[#131A22] flex items-center justify-center">
          <p className="text-[#5F6B78] text-xs">Background unavailable</p>
        </div>
      );
    }

    return this.props.children;
  }
}

// ============================================================
// MAIN COMPONENT
// ============================================================

export const HeroCanvas: React.FC<HeroCanvasProps> = memo(({
  className = 'absolute inset-0 pointer-events-none z-0',
  opacity = 0.8,
  blur = 'blur(0.5px)',
  particleCount: propParticleCount,
  connectionDistance = 150,
  colors: propColors,
  speed = 0.8,
  mouseInteraction = true,
  enable3D = true,
  enableTrails = true,
  enableGlow = true,
  showFPS = false,
  backgroundColor = 'rgba(11, 15, 20, 0.3)',
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationFrameId = useRef<number | null>(null);
  const resizeTimeout = useRef<NodeJS.Timeout | null>(null);
  const isMounted = useRef<boolean>(true);
  const mouseRef = useRef<{ x: number; y: number; targetX: number; targetY: number }>({
    x: -1000, y: -1000, targetX: -1000, targetY: -1000
  });
  const fpsRef = useRef<{ frames: number; lastTime: number; fps: number }>({
    frames: 0, lastTime: 0, fps: 0
  });
  const timeRef = useRef<number>(0);

  // ============================================================
  // STATE
  // ============================================================
  
  const [fps, setFps] = useState<number>(0);

  // ============================================================
  // LOGGING
  // ============================================================
  
  useEffect(() => {
    log.info('HeroCanvas v3.0 mounted', { 
      mouseInteraction, enable3D, enableTrails, enableGlow 
    });
    return () => {
      log.debug('HeroCanvas unmounted');
    };
  }, []);

  // ============================================================
  // COLOR UTILITIES
  // ============================================================
  
  const hslToRgb = (h: number, s: number, l: number): string => {
    h /= 360;
    s /= 100;
    l /= 100;
    let r, g, b;
    if (s === 0) {
      r = g = b = l;
    } else {
      const hue2rgb = (p: number, q: number, t: number) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      };
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }
    return `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`;
  };

  // ============================================================
  // RENDER FUNCTION
  // ============================================================
  
  const renderCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      log.warn('Canvas ref is null');
      return;
    }

    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) {
      log.warn('Canvas context is null');
      return;
    }

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    log.debug(`Canvas initialized: ${width}x${height}`);

    // ============================================================
    // PARTICLE CONFIG
    // ============================================================
    
    const defaultColors = ['#00D4FF', '#00F0FF', '#F5A623', '#FFC837', '#6366F1', '#EC4899', '#8B5CF6'];
    const colors = propColors || defaultColors;
    
    const baseParticleCount = propParticleCount || Math.min(
      window.innerWidth > 768 ? 80 : 40,
      100
    );
    
    // Density scaling based on screen size
    const densityScale = Math.min(1, (window.innerWidth * window.innerHeight) / (1920 * 1080));
    const particleCount = Math.max(20, Math.floor(baseParticleCount * densityScale));

    const particles: Particle[] = [];

    for (let i = 0; i < particleCount; i++) {
      const hue = Math.random() * 360;
      const color = colors[Math.floor(Math.random() * colors.length)];
      const alpha = Math.random() * 0.6 + 0.2;
      
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        z: Math.random() * 100 - 50,
        vx: (Math.random() - 0.5) * speed,
        vy: (Math.random() - 0.5) * speed,
        vz: (Math.random() - 0.5) * 0.2,
        radius: Math.random() * 2.5 + 0.5,
        targetRadius: Math.random() * 2.5 + 0.5,
        color: color,
        hue: hue,
        alpha: alpha,
        targetAlpha: alpha,
        pulsePhase: Math.random() * Math.PI * 2,
        pulseSpeed: 0.01 + Math.random() * 0.02,
        trail: [],
        connections: new Set(),
      });
    }

    // ============================================================
    // MOUSE HANDLER
    // ============================================================
    
    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current.targetX = e.clientX;
      mouseRef.current.targetY = e.clientY;
    };

    const handleMouseLeave = () => {
      mouseRef.current.targetX = -1000;
      mouseRef.current.targetY = -1000;
    };

    const handleTouchMove = (e: TouchEvent) => {
      const touch = e.touches[0];
      if (touch) {
        mouseRef.current.targetX = touch.clientX;
        mouseRef.current.targetY = touch.clientY;
      }
    };

    const handleTouchEnd = () => {
      mouseRef.current.targetX = -1000;
      mouseRef.current.targetY = -1000;
    };

    if (mouseInteraction) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseleave', handleMouseLeave);
      window.addEventListener('touchmove', handleTouchMove);
      window.addEventListener('touchend', handleTouchEnd);
    }

    // ============================================================
    // RESIZE HANDLER
    // ============================================================
    
    const handleResize = useCallback(() => {
      if (resizeTimeout.current) {
        clearTimeout(resizeTimeout.current);
      }

      resizeTimeout.current = setTimeout(() => {
        if (!canvas || !isMounted.current) return;
        
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        
        log.debug(`Canvas resized: ${width}x${height}`);
      }, 150);
    }, [canvas]);

    window.addEventListener('resize', handleResize);

    // ============================================================
    // RENDER LOOP
    // ============================================================
    
    const render = () => {
      if (!isMounted.current) {
        log.debug('Render loop stopped - component unmounted');
        return;
      }

      try {
        // ============================================================
        // FPS CALCULATION
        // ============================================================
        if (showFPS) {
          const now = performance.now();
          fpsRef.current.frames++;
          if (now - fpsRef.current.lastTime > 1000) {
            fpsRef.current.fps = fpsRef.current.frames;
            fpsRef.current.frames = 0;
            fpsRef.current.lastTime = now;
            setFps(fpsRef.current.fps);
          }
        }

        // Smooth mouse following
        mouseRef.current.x += (mouseRef.current.targetX - mouseRef.current.x) * 0.08;
        mouseRef.current.y += (mouseRef.current.targetY - mouseRef.current.y) * 0.08;

        // ============================================================
        // BACKGROUND
        // ============================================================
        ctx.clearRect(0, 0, width, height);
        
        // Gradient background
        const grad = ctx.createRadialGradient(
          width/2, height/2, 0,
          width/2, height/2, Math.max(width, height) * 0.7
        );
        grad.addColorStop(0, 'rgba(20, 30, 50, 0.4)');
        grad.addColorStop(1, backgroundColor);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, width, height);

        // ============================================================
        // SUBTLE GRID (with perspective effect)
        // ============================================================
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.015)';
        ctx.lineWidth = 1;
        const gridSize = 60;
        const perspectiveOffset = enable3D ? Math.sin(timeRef.current * 0.0001) * 10 : 0;
        
        for (let x = 0; x < width + gridSize; x += gridSize) {
          ctx.beginPath();
          const offsetX = x + perspectiveOffset;
          ctx.moveTo(offsetX, 0);
          ctx.lineTo(offsetX, height);
          ctx.stroke();
        }
        for (let y = 0; y < height + gridSize; y += gridSize) {
          ctx.beginPath();
          const offsetY = y + perspectiveOffset * 0.5;
          ctx.moveTo(0, offsetY);
          ctx.lineTo(width, offsetY);
          ctx.stroke();
        }

        // ============================================================
        // UPDATE PARTICLES
        // ============================================================
        timeRef.current += 1;
        const mouseX = mouseRef.current.x;
        const mouseY = mouseRef.current.y;

        for (let i = 0; i < particles.length; i++) {
          const p = particles[i];
          
          // ============================================================
          // PULSE EFFECT
          // ============================================================
          p.pulsePhase += p.pulseSpeed;
          const pulse = Math.sin(p.pulsePhase) * 0.3 + 0.7;
          p.radius = p.targetRadius * pulse;
          p.alpha = p.targetAlpha * (0.7 + 0.3 * Math.sin(p.pulsePhase * 0.7 + 1));

          // ============================================================
          // MOUSE INTERACTION - Attraction/Repulsion
          // ============================================================
          if (mouseInteraction && mouseX > 0 && mouseY > 0) {
            const dx = p.x - mouseX;
            const dy = p.y - mouseY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < 200) {
              const force = (1 - dist / 200) * 0.5;
              const angle = Math.atan2(dy, dx);
              // Attraction with slight repulsion at very close distance
              if (dist > 30) {
                p.vx -= Math.cos(angle) * force * 0.05;
                p.vy -= Math.sin(angle) * force * 0.05;
              } else {
                p.vx += Math.cos(angle) * force * 0.1;
                p.vy += Math.sin(angle) * force * 0.1;
              }
            }
          }

          // ============================================================
          // 3D DEPTH EFFECT
          // ============================================================
          if (enable3D) {
            const depthScale = 1 + (p.z / 100) * 0.3;
            p.radius = p.targetRadius * pulse * depthScale;
          }

          // ============================================================
          // UPDATE POSITION
          // ============================================================
          p.x += p.vx;
          p.y += p.vy;
          if (enable3D) {
            p.z += p.vz;
            if (Math.abs(p.z) > 100) p.vz *= -1;
          }

          // ============================================================
          // WRAP AROUND
          // ============================================================
          if (p.x < -10) p.x = width + 10;
          if (p.x > width + 10) p.x = -10;
          if (p.y < -10) p.y = height + 10;
          if (p.y > height + 10) p.y = -10;

          // ============================================================
          // TRAIL
          // ============================================================
          if (enableTrails) {
            p.trail.push({ x: p.x, y: p.y, alpha: 0.3 });
            if (p.trail.length > 6) {
              p.trail.shift();
            }
          }

          // ============================================================
          // CONNECTIONS
          // ============================================================
          p.connections.clear();
        }

        // ============================================================
        // DRAW TRAILS
        // ============================================================
        if (enableTrails) {
          for (const p of particles) {
            for (let t = 0; t < p.trail.length; t++) {
              const trail = p.trail[t];
              const alpha = (t / p.trail.length) * 0.15 * p.alpha;
              ctx.beginPath();
              ctx.arc(trail.x, trail.y, p.radius * (t / p.trail.length) * 0.5, 0, Math.PI * 2);
              ctx.fillStyle = p.color;
              ctx.globalAlpha = alpha;
              ctx.fill();
            }
          }
          ctx.globalAlpha = 1;
        }

        // ============================================================
        // DRAW CONNECTIONS (NEURAL NETWORK)
        // ============================================================
        const connectionDistSq = connectionDistance * connectionDistance;
        
        // Sort particles by x for spatial optimization
        const sortedParticles = [...particles].sort((a, b) => a.x - b.x);
        
        for (let i = 0; i < sortedParticles.length; i++) {
          const p = sortedParticles[i];
          
          // Only check nearby particles (spatial optimization)
          for (let j = i + 1; j < sortedParticles.length; j++) {
            const p2 = sortedParticles[j];
            
            // Quick X-axis rejection
            if (p2.x - p.x > connectionDistance) break;
            
            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const distSq = dx * dx + dy * dy;

            if (distSq < connectionDistSq) {
              const dist = Math.sqrt(distSq);
              const lineAlpha = (1 - dist / connectionDistance) * 0.2;
              
              // ============================================================
              // GLOW EFFECT
              // ============================================================
              if (enableGlow) {
                // Outer glow
                const glowWidth = 4;
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = p.color;
                ctx.globalAlpha = lineAlpha * 0.2;
                ctx.lineWidth = glowWidth;
                ctx.shadowColor = p.color;
                ctx.shadowBlur = 10;
                ctx.stroke();
                ctx.shadowBlur = 0;
              }

              // Main line
              ctx.beginPath();
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(p2.x, p2.y);
              ctx.strokeStyle = p.color;
              ctx.globalAlpha = lineAlpha;
              ctx.lineWidth = 0.8;
              ctx.stroke();
            }
          }
        }
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;

        // ============================================================
        // DRAW PARTICLES
        // ============================================================
        for (const p of particles) {
          // Glow
          if (enableGlow) {
            const glow = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius * 4);
            glow.addColorStop(0, p.color);
            glow.addColorStop(1, 'transparent');
            ctx.fillStyle = glow;
            ctx.globalAlpha = p.alpha * 0.15;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius * 4, 0, Math.PI * 2);
            ctx.fill();
          }

          // Particle
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = p.alpha;
          ctx.shadowColor = p.color;
          ctx.shadowBlur = enableGlow ? 8 : 0;
          ctx.fill();
        }
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;

        // ============================================================
        // FPS DISPLAY
        // ============================================================
        if (showFPS && fps > 0) {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
          ctx.font = '10px monospace';
          ctx.fillText(`FPS: ${fps} | Particles: ${particles.length}`, 10, 20);
        }

        // ============================================================
        // REQUEST NEXT FRAME
        // ============================================================
        if (isMounted.current) {
          animationFrameId.current = requestAnimationFrame(render);
        }

      } catch (error) {
        log.error('Render loop error:', error);
        if (animationFrameId.current) {
          cancelAnimationFrame(animationFrameId.current);
          animationFrameId.current = null;
        }
      }
    };

    // Start render loop
    try {
      render();
      log.debug('Render loop started');
    } catch (error) {
      log.error('Failed to start render loop:', error);
    }

    // ============================================================
    // CLEANUP
    // ============================================================
    
    return () => {
      isMounted.current = false;
      
      window.removeEventListener('resize', handleResize);
      if (mouseInteraction) {
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseleave', handleMouseLeave);
        window.removeEventListener('touchmove', handleTouchMove);
        window.removeEventListener('touchend', handleTouchEnd);
      }
      
      if (resizeTimeout.current) {
        clearTimeout(resizeTimeout.current);
        resizeTimeout.current = null;
      }
      
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
        animationFrameId.current = null;
      }
      
      ctx.clearRect(0, 0, width, height);
      
      log.debug('Canvas cleanup complete');
    };

  }, [connectionDistance, propColors, propParticleCount, speed, mouseInteraction, enable3D, enableTrails, enableGlow, showFPS, backgroundColor]);

  // ============================================================
  // EFFECT
  // ============================================================
  
  useEffect(() => {
    isMounted.current = true;
    
    const cleanup = renderCanvas();
    
    return () => {
      isMounted.current = false;
      if (cleanup) cleanup();
    };
  }, [renderCanvas]);

  // ============================================================
  // RENDER
  // ============================================================
  
  return (
    <HeroCanvasErrorBoundary>
      <canvas
        ref={canvasRef}
        className={className}
        style={{ 
          filter: blur,
          opacity: opacity,
        }}
        aria-label="Cognitive neural network background with 3D depth, mouse interaction, and dynamic particles"
        role="img"
      />
    </HeroCanvasErrorBoundary>
  );
});

// ============================================================
// EXPORT
// ============================================================

HeroCanvas.displayName = 'HeroCanvas';

export default HeroCanvas;
