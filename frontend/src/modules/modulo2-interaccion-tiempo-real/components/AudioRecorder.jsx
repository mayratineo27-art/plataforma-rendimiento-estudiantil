// frontend/src/modules/modulo2-interaccion-tiempo-real/components/AudioRecorder.jsx
// Componente para grabación de audio y transcripción

import React, { useState, useRef, useEffect } from 'react';

const AudioRecorder = ({ isRecording, onAudioCapture }) => {
  const [audioLevel, setAudioLevel] = useState(0);
  const [transcriptionCount, setTranscriptionCount] = useState(0);
  const [lastTranscription, setLastTranscription] = useState('');
  const [recording, setRecording] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (isRecording) {
      startRecording();
    } else {
      stopRecording();
    }

    return () => {
      stopRecording();
    };
  }, [isRecording]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      // Configurar analizador de audio para nivel visual
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const analyser = audioContext.createAnalyser();
      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);
      analyser.fftSize = 256;

      audioContextRef.current = audioContext;
      analyserRef.current = analyser;

      // Actualizar nivel de audio
      updateAudioLevel();

      // Configurar MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });

      mediaRecorderRef.current = mediaRecorder;
      const chunks = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        
        // Enviar para transcripción
        if (onAudioCapture && audioBlob.size > 0) {
          try {
            const response = await onAudioCapture(audioBlob);
            if (response && response.transcription) {
              setLastTranscription(response.transcription.text || '');
              setTranscriptionCount(prev => prev + 1);
            }
          } catch (err) {
            console.error('Error enviando audio:', err);
          }
        }

        chunks.length = 0;

        // Reiniciar grabación si aún está activo
        if (isRecording) {
          setTimeout(() => startRecording(), 100);
        }
      };

      mediaRecorder.start();
      setRecording(true);

      // Detener después de 10 segundos y enviar
      setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
        }
      }, 10000);

    } catch (err) {
      console.error('Error iniciando grabación de audio:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }

    setRecording(false);
    setAudioLevel(0);
  };

  const updateAudioLevel = () => {
    if (!analyserRef.current || !isRecording) return;

    const analyser = analyserRef.current;
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    
    const update = () => {
      if (!isRecording) return;

      analyser.getByteFrequencyData(dataArray);
      const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
      setAudioLevel(Math.min((average / 128) * 100, 100));

      requestAnimationFrame(update);
    };

    update();
  };

  return (
    <div className="space-y-4">
      {/* Visualizador de Audio */}
      <div className="bg-slate-800 rounded-xl p-6 border border-indigo-500/30 shadow-2xl">
        <div className="flex items-center justify-center mb-6">
          <div className={`w-20 h-20 rounded-full flex items-center justify-center ${
            recording ? 'bg-gradient-to-r from-red-600 to-rose-600 animate-pulse' : 'bg-slate-700'
          }`}>
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
        </div>

        {/* Nivel de Audio */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-slate-300">
            <span>Nivel de Audio</span>
            <span className="font-semibold">{audioLevel.toFixed(0)}%</span>
          </div>
          <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-500 to-emerald-500 transition-all duration-100"
              style={{ width: `${audioLevel}%` }}
            />
          </div>
        </div>

        {/* Barras visuales */}
        <div className="flex items-end justify-center gap-1 h-24 mt-6">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="w-2 bg-gradient-to-t from-indigo-600 to-purple-600 rounded-t transition-all duration-100"
              style={{
                height: `${Math.random() * audioLevel}%`,
                opacity: recording ? 1 : 0.3
              }}
            />
          ))}
        </div>
      </div>

      {/* Información */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-800/50 rounded-lg p-4">
          <div className="text-slate-400 text-xs mb-1">Transcripciones</div>
          <div className="text-white text-2xl font-bold">{transcriptionCount}</div>
        </div>

        <div className="bg-slate-800/50 rounded-lg p-4">
          <div className="text-slate-400 text-xs mb-1">Estado</div>
          <div className={`text-sm font-semibold ${recording ? 'text-green-400' : 'text-slate-500'}`}>
            {recording ? '🎤 Grabando' : '⏸️ En pausa'}
          </div>
        </div>
      </div>

      {/* Última transcripción */}
      {lastTranscription && (
        <div className="bg-slate-800/50 rounded-lg p-4">
          <div className="text-slate-400 text-xs mb-2">Última transcripción:</div>
          <div className="text-slate-200 text-sm italic">
            "{lastTranscription.substring(0, 150)}{lastTranscription.length > 150 ? '...' : ''}"
          </div>
        </div>
      )}

      {/* Info técnica */}
      <div className="bg-slate-800/50 rounded-lg p-4">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Formato: WebM</span>
          <span>•</span>
          <span>Segmentos: 10s</span>
          <span>•</span>
          <span>Motor: Speech Recognition</span>
        </div>
      </div>
    </div>
  );
};

export default AudioRecorder;