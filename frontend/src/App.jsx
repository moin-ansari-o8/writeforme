/**
 * Main App Component - Wisprflow Clone
 * Professional voice-to-text application with real-time transcription
 */
import React, { useState, useEffect } from 'react';
import VoiceVisualizer from './components/VoiceVisualizer';
import { useAudioRecorder } from './hooks/useAudioRecorder';
import './App.css';

function App() {
  const {
    isRecording,
    isProcessing,
    transcription,
    error,
    isConnected,
    startRecording,
    stopRecording,
    cancelRecording,
  } = useAudioRecorder();

  const [theme, setTheme] = useState('auto');
  const [showTranscription, setShowTranscription] = useState(false);

  // Show transcription when available
  useEffect(() => {
    if (transcription) {
      setShowTranscription(true);
      // Auto-hide after 5 seconds
      const timer = setTimeout(() => setShowTranscription(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [transcription]);

  const handleStartStop = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleCancel = () => {
    cancelRecording();
    setShowTranscription(false);
  };

  const copyToClipboard = () => {
    if (transcription) {
      navigator.clipboard.writeText(transcription);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <svg className="logo-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              <h1 className="logo-text">Wisprflow</h1>
            </div>
            
            <div className="header-actions">
              <button
                className="theme-toggle"
                onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
                aria-label="Toggle theme"
              >
                {theme === 'light' ? '🌙' : '☀️'}
              </button>
              
              <div className="status-indicator">
                <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`} />
                <span className="status-text">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          <div className="content-wrapper">
            
            {/* Instructions */}
            {!isRecording && !isProcessing && !showTranscription && (
              <div className="instructions">
                <h2 className="instructions-title">Voice to Text</h2>
                <p className="instructions-text">
                  Click the microphone button to start recording. Speak clearly and press stop when done.
                </p>
              </div>
            )}

            {/* Visualizer Section */}
            <div className="visualizer-section">
              <VoiceVisualizer
                isListening={isRecording}
                onError={(err) => console.error('Visualizer error:', err)}
                theme={theme}
              />
              
              {isProcessing && (
                <div className="processing-status">
                  <div className="spinner" />
                  <span>Processing audio...</span>
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="controls">
              {isRecording && (
                <button
                  className="btn btn-secondary"
                  onClick={handleCancel}
                >
                  <svg className="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  Cancel
                </button>
              )}
              
              <button
                className={`btn ${isRecording ? 'btn-stop' : 'btn-primary'}`}
                onClick={handleStartStop}
                disabled={isProcessing || !isConnected}
              >
                {isRecording ? (
                  <>
                    <svg className="btn-icon" fill="currentColor" viewBox="0 0 24 24">
                      <rect x="6" y="6" width="12" height="12" rx="2" />
                    </svg>
                    Stop Recording
                  </>
                ) : (
                  <>
                    <svg className="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                    </svg>
                    Start Recording
                  </>
                )}
              </button>
            </div>

            {/* Transcription Result */}
            {showTranscription && transcription && (
              <div className="transcription-card">
                <div className="transcription-header">
                  <h3 className="transcription-title">Transcription</h3>
                  <button
                    className="btn-icon-only"
                    onClick={copyToClipboard}
                    title="Copy to clipboard"
                  >
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                  </button>
                </div>
                <p className="transcription-text">{transcription}</p>
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="error-card">
                <svg className="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="error-text">{error}</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p className="footer-text">
            Powered by Whisper AI • Real-time transcription
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
