/**
 * useAudioRecorder - Custom hook for real-time audio recording with WebSocket streaming
 * 
 * Handles:
 * - MediaRecorder setup and audio capture
 * - WebSocket connection management
 * - Audio chunk streaming to backend
 * - Transcription result handling
 */
import { useState, useRef, useCallback, useEffect } from 'react';

const WS_URL = 'ws://localhost:8000/ws/transcribe';

export const useAudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const mediaRecorderRef = useRef(null);
  const websocketRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);

  /**
   * Initialize WebSocket connection
   */
  const connectWebSocket = useCallback(() => {
    return new Promise((resolve, reject) => {
      try {
        const ws = new WebSocket(WS_URL);

        ws.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
          setError(null);
          resolve(ws);
        };

        ws.onerror = (err) => {
          console.error('WebSocket error:', err);
          setError('Failed to connect to transcription service');
          setIsConnected(false);
          reject(err);
        };

        ws.onclose = () => {
          console.log('WebSocket closed');
          setIsConnected(false);
        };

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            handleWebSocketMessage(message);
          } catch (err) {
            console.error('Error parsing WebSocket message:', err);
          }
        };

        websocketRef.current = ws;
      } catch (err) {
        console.error('WebSocket connection error:', err);
        setError('Failed to connect to server');
        reject(err);
      }
    });
  }, []);

  /**
   * Handle incoming WebSocket messages
   */
  const handleWebSocketMessage = useCallback((message) => {
    switch (message.type) {
      case 'chunk_received':
        // Acknowledgment from server
        console.log('Chunk received, buffer size:', message.buffer_size);
        break;

      case 'transcription_result':
        // Final transcription result
        setTranscription(message.text);
        setIsProcessing(false);
        console.log('Transcription:', message.text);
        break;

      case 'error':
        setError(message.message);
        setIsProcessing(false);
        console.error('Server error:', message.message);
        break;

      case 'pong':
        // Keep-alive response
        break;

      default:
        console.warn('Unknown message type:', message.type);
    }
  }, []);

  /**
   * Start recording audio
   */
  const startRecording = useCallback(async () => {
    try {
      setError(null);
      setTranscription('');
      chunksRef.current = [];

      // Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      streamRef.current = stream;

      // Connect WebSocket if not connected
      if (!websocketRef.current || websocketRef.current.readyState !== WebSocket.OPEN) {
        await connectWebSocket();
      }

      // Setup MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus',
      });

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
          
          // Send chunk to server
          if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
            const reader = new FileReader();
            reader.onloadend = () => {
              const base64Audio = reader.result?.split(',')[1]; // Remove data:audio/webm;base64,
              if (!base64Audio) {
                console.warn('Failed to encode audio chunk');
                return;
              }
              websocketRef.current.send(JSON.stringify({
                type: 'audio_chunk',
                data: base64Audio,
              }));
            };
            reader.readAsDataURL(event.data);
          }
        }
      };

      mediaRecorder.onstop = () => {
        console.log('Recording stopped');
        setIsRecording(false);
        setIsProcessing(true);

        // Send end signal
        if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
          websocketRef.current.send(JSON.stringify({
            type: 'audio_end',
          }));
        }
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start(100); // Capture in 100ms chunks
      setIsRecording(true);

    } catch (err) {
      console.error('Error starting recording:', err);
      setError(err.message || 'Failed to start recording');
      setIsRecording(false);
    }
  }, [connectWebSocket]);

  /**
   * Stop recording audio
   */
  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }

    // Stop all tracks
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
  }, []);

  /**
   * Cancel recording without processing
   */
  const cancelRecording = useCallback(() => {
    stopRecording();
    chunksRef.current = [];
    setIsRecording(false);
    setIsProcessing(false);
    setTranscription('');
  }, [stopRecording]);

  /**
   * Cleanup on unmount
   */
  useEffect(() => {
    return () => {
      // Stop recording
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }

      // Stop stream
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }

      // Close WebSocket
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  return {
    isRecording,
    isProcessing,
    transcription,
    error,
    isConnected,
    startRecording,
    stopRecording,
    cancelRecording,
  };
};
