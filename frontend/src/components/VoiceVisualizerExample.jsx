/**
 * Example usage of VoiceVisualizer component
 * 
 * This file demonstrates how to integrate the VoiceVisualizer
 * component into a React application.
 */
import React, { useState } from 'react';
import VoiceVisualizer from './VoiceVisualizer';

/**
 * Example App component demonstrating VoiceVisualizer usage
 */
function VoiceVisualizerExample() {
  const [isRecording, setIsRecording] = useState(false);

  const handleError = (err) => {
    console.error('Visualizer error:', err);
    // Handle error appropriately (e.g., show notification)
  };

  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
        Voice Visualizer Demo
      </h1>
      
      <VoiceVisualizer
        isListening={isRecording}
        onError={handleError}
        theme="auto"
      />
      
      <button
        onClick={() => setIsRecording(!isRecording)}
        className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        {isRecording ? 'Stop' : 'Start'} Recording
      </button>

      <p className="text-sm text-gray-500 dark:text-gray-400 max-w-md text-center">
        Click the button to start recording. The visualizer will respond to your voice
        with a dynamic blob animation. When idle, a gentle breathing pulse is displayed.
      </p>
    </div>
  );
}

export default VoiceVisualizerExample;
