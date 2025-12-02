import React, { useRef, useEffect, useState, useCallback } from 'react';

/**
 * VoiceVisualizer - A compact pill-shaped audio visualizer component
 * Inspired by Wisprflow's aesthetic with performance-optimized rendering
 * 
 * @param {boolean} isListening - Controls active/idle state
 * @param {function} onError - Callback for mic permission errors
 * @param {string} theme - 'light' | 'dark' | 'auto' (default: 'auto')
 */

// Constants for pill dimensions and frequency analysis
const PILL_WIDTH_IDLE = 120;
const PILL_WIDTH_ACTIVE = 180;
const PILL_HEIGHT = 40;
const CANVAS_WIDTH = 240;
const CANVAS_HEIGHT = 80;
const BASE_FREQUENCY_BANDS = 8;

/**
 * Detects if the device is low-end based on hardware capabilities
 * @returns {boolean} True if device is considered low-end
 */
const isLowEndDevice = () => {
  if (typeof navigator === 'undefined') return false;
  return (
    (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4) ||
    /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  );
};

/**
 * MicOffIcon - Simple microphone off icon component
 */
const MicOffIcon = ({ className }) => (
  <svg 
    className={className} 
    fill="none" 
    viewBox="0 0 24 24" 
    stroke="currentColor"
    aria-hidden="true"
  >
    <path 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      strokeWidth={2} 
      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
    />
    <path 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      strokeWidth={2} 
      d="M3 3l18 18" 
    />
  </svg>
);

const VoiceVisualizer = ({ 
  isListening = false, 
  onError = null, 
  theme = 'auto' 
}) => {
  // Audio state
  const [audioContext, setAudioContext] = useState(null);
  const [analyser, setAnalyser] = useState(null);
  const [micPermission, setMicPermission] = useState('prompt'); // 'granted' | 'denied' | 'prompt'
  const [isSupported, setIsSupported] = useState(true);
  
  // Refs for canvas and animation
  const canvasRef = useRef(null);
  const animationFrameRef = useRef(null);
  const streamRef = useRef(null);
  const sourceRef = useRef(null);
  
  // Performance optimization settings
  const frequencyBands = useRef(BASE_FREQUENCY_BANDS);
  const prefersReducedMotion = useRef(false);

  // Check browser support and reduced motion preference
  useEffect(() => {
    // Check for getUserMedia support
    if (typeof navigator === 'undefined' || !navigator.mediaDevices?.getUserMedia) {
      setIsSupported(false);
      return;
    }

    // Check for reduced motion preference
    if (typeof window !== 'undefined' && window.matchMedia) {
      const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
      prefersReducedMotion.current = motionQuery.matches;
      
      const handleMotionChange = (e) => {
        prefersReducedMotion.current = e.matches;
      };
      
      motionQuery.addEventListener('change', handleMotionChange);
      return () => motionQuery.removeEventListener('change', handleMotionChange);
    }
  }, []);

  // Optimize for low-end devices
  useEffect(() => {
    if (isLowEndDevice()) {
      frequencyBands.current = 4;
    }
  }, []);

  /**
   * Initialize audio pipeline with Web Audio API
   */
  const initAudio = useCallback(async () => {
    if (!isSupported) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });

      streamRef.current = stream;

      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioContextClass();
      
      // Handle iOS Safari suspended state
      if (ctx.state === 'suspended') {
        await ctx.resume();
      }

      const analyserNode = ctx.createAnalyser();
      
      // Optimized FFT settings for performance
      // Using 64 for all devices (32 frequency bins) - provides adequate resolution
      const fftSize = 64;
      analyserNode.fftSize = fftSize;
      analyserNode.smoothingTimeConstant = 0.7;
      analyserNode.minDecibels = -90;
      analyserNode.maxDecibels = -10;

      const source = ctx.createMediaStreamSource(stream);
      source.connect(analyserNode);
      sourceRef.current = source;

      setAudioContext(ctx);
      setAnalyser(analyserNode);
      setMicPermission('granted');
    } catch (err) {
      console.error('Mic access error:', err);
      setMicPermission('denied');
      onError?.(err);
    }
  }, [isSupported, onError]);

  /**
   * Draw idle pulse animation (breathing circle)
   */
  const drawIdlePulse = useCallback((ctx, centerX, centerY, styles) => {
    const time = Date.now() / 1000;
    
    // If reduced motion is preferred, use static circle
    let radius;
    if (prefersReducedMotion.current) {
      radius = 11;
    } else {
      const pulse = Math.sin(time * 2) * 0.5 + 0.5; // 0-1 sine wave
      radius = 10 + pulse * 3; // 10-13px breathing
    }

    ctx.fillStyle = styles.waveIdle;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fill();
  }, []);

  /**
   * Draw audio-reactive blob using frequency data
   */
  const drawAudioBlob = useCallback((ctx, dataArray, centerX, centerY, styles) => {
    // Ensure we don't exceed dataArray bounds
    const numPoints = Math.min(frequencyBands.current, dataArray.length);
    const baseRadius = 12;
    const points = [];

    // Generate radial points based on frequency data
    for (let i = 0; i < numPoints; i++) {
      const angle = (Math.PI * 2 * i) / numPoints;
      const amplitude = dataArray[i] / 255; // Normalize 0-1
      const radius = baseRadius + amplitude * 8; // Scale 12-20px

      points.push({
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius
      });
    }

    // Need at least 2 points to draw
    if (points.length < 2) return;

    // Draw smooth blob using quadratic curves
    ctx.fillStyle = styles.waveActive;
    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (let i = 0; i < points.length; i++) {
      const p1 = points[i];
      const p2 = points[(i + 1) % points.length];
      const xc = (p1.x + p2.x) / 2;
      const yc = (p1.y + p2.y) / 2;
      ctx.quadraticCurveTo(p1.x, p1.y, xc, yc);
    }

    ctx.closePath();
    ctx.fill();
  }, []);

  /**
   * Get computed styles for theming
   */
  const getStyles = useCallback(() => {
    let isDark = false;
    
    if (theme === 'dark') {
      isDark = true;
    } else if (theme === 'auto' && typeof window !== 'undefined' && window.matchMedia) {
      isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    return {
      pillBg: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(15, 23, 42, 0.05)',
      waveIdle: isDark ? 'rgba(129, 140, 248, 0.4)' : 'rgba(99, 102, 241, 0.3)',
      waveActive: isDark ? 'rgba(129, 140, 248, 1)' : 'rgba(99, 102, 241, 0.8)'
    };
  }, [theme]);

  /**
   * Main draw function for canvas rendering
   */
  const draw = useCallback(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const styles = getStyles();
    
    // Get frequency data if analyser is available
    let dataArray = null;
    
    if (analyser && isListening) {
      dataArray = new Uint8Array(analyser.frequencyBinCount);
      analyser.getByteFrequencyData(dataArray);
    }

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Calculate current pill width with smooth transition
    const currentWidth = isListening ? PILL_WIDTH_ACTIVE : PILL_WIDTH_IDLE;
    const pillX = (canvas.width - currentWidth) / 2;
    const pillY = (canvas.height - PILL_HEIGHT) / 2;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Draw pill background
    ctx.fillStyle = styles.pillBg;
    ctx.beginPath();
    
    // Draw rounded rectangle (pill shape)
    const radius = PILL_HEIGHT / 2;
    ctx.moveTo(pillX + radius, pillY);
    ctx.lineTo(pillX + currentWidth - radius, pillY);
    ctx.arcTo(pillX + currentWidth, pillY, pillX + currentWidth, pillY + radius, radius);
    ctx.lineTo(pillX + currentWidth, pillY + PILL_HEIGHT - radius);
    ctx.arcTo(pillX + currentWidth, pillY + PILL_HEIGHT, pillX + currentWidth - radius, pillY + PILL_HEIGHT, radius);
    ctx.lineTo(pillX + radius, pillY + PILL_HEIGHT);
    ctx.arcTo(pillX, pillY + PILL_HEIGHT, pillX, pillY + PILL_HEIGHT - radius, radius);
    ctx.lineTo(pillX, pillY + radius);
    ctx.arcTo(pillX, pillY, pillX + radius, pillY, radius);
    ctx.closePath();
    ctx.fill();

    // Draw visualization
    if (isListening && dataArray) {
      drawAudioBlob(ctx, dataArray, centerX, centerY, styles);
    } else {
      drawIdlePulse(ctx, centerX, centerY, styles);
    }

    animationFrameRef.current = requestAnimationFrame(draw);
  }, [analyser, isListening, getStyles, drawAudioBlob, drawIdlePulse]);

  // Initialize audio when listening starts
  useEffect(() => {
    if (isListening && !audioContext && isSupported) {
      initAudio();
    }
  }, [isListening, audioContext, isSupported, initAudio]);

  // Start/stop animation based on listening state and analyser availability
  useEffect(() => {
    if (canvasRef.current) {
      // Always start animation for idle pulse
      draw();
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
    };
  }, [draw]);

  // Handle visibility change (pause when tab is hidden)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
          animationFrameRef.current = null;
        }
      } else if (canvasRef.current) {
        draw();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [draw]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      // Cancel animation frame
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      
      // Disconnect audio source
      if (sourceRef.current) {
        sourceRef.current.disconnect();
      }
      
      // Close audio context
      if (audioContext) {
        audioContext.close().catch(console.error);
      }
      
      // Stop media stream tracks
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, [audioContext]);

  // Browser compatibility check
  if (!isSupported) {
    return (
      <div className="text-sm text-gray-500 dark:text-gray-400">
        Audio visualization not supported
      </div>
    );
  }

  // Microphone permission denied
  if (micPermission === 'denied') {
    return (
      <div className="flex items-center gap-2 px-4 py-2 bg-red-50 dark:bg-red-900/20 rounded-full">
        <MicOffIcon className="w-4 h-4 text-red-600 dark:text-red-400" />
        <span className="text-sm text-red-600 dark:text-red-400">Mic access denied</span>
      </div>
    );
  }

  return (
    <div className="relative flex items-center justify-center">
      <canvas
        ref={canvasRef}
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        className="rounded-full"
        aria-label={isListening ? "Audio visualizer - listening" : "Audio visualizer - idle"}
        role="img"
      />
    </div>
  );
};

export default VoiceVisualizer;
