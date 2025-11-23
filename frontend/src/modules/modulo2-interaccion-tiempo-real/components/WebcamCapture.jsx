// frontend/src/modules/modulo2-interaccion-tiempo-real/components/WebcamCapture.jsx
// Componente para captura de video y análisis facial

import React, { useRef, useEffect, useState } from 'react';

const WebcamCapture = ({ isRecording, onFrameCapture, onError }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [capturing, setCapturing] = useState(false);
  const [lastEmotion, setLastEmotion] = useState(null);
  const [frameCount, setFrameCount] = useState(0);

  useEffect(() => {
    if (isRecording) {
      startWebcam();
    } else {
      stopWebcam();
    }

    return () => {
      stopWebcam();
    };
  }, [isRecording]);

  const startWebcam = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        },
        audio: false
      });

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        setStream(mediaStream);
        setCapturing(true);
        
        // Capturar frames cada 2 segundos
        startFrameCapture();
      }
    } catch (err) {
      console.error('Error accediendo a la webcam:', err);
      if (onError) {
        onError('No se pudo acceder a la cámara. Verifica los permisos.');
      }
    }
  };

  const stopWebcam = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setCapturing(false);
    }
  };

  const startFrameCapture = () => {
    let intervalId = setInterval(() => {
      if (!isRecording) {
        clearInterval(intervalId);
        return;
      }
      captureFrame();
    }, 2000); // Capturar cada 2 segundos
  };

  const captureFrame = async () => {
    if (!videoRef.current || !canvasRef.current || !isRecording) return;

    try {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      // Configurar canvas
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Dibujar frame actual
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Convertir a base64
      const frameBase64 = canvas.toDataURL('image/jpeg', 0.8);

      // Enviar al backend
      if (onFrameCapture) {
        const response = await onFrameCapture(frameBase64);
        
        if (response && response.emotion) {
          setLastEmotion(response.emotion);
          setFrameCount(prev => prev + 1);
        }
      }
    } catch (err) {
      console.error('Error capturando frame:', err);
    }
  };

  return (
    <div className="space-y-4">
      {/* Video Preview */}
      <div className="relative bg-slate-800 rounded-xl overflow-hidden shadow-2xl border border-indigo-500/30">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-auto"
          style={{ maxHeight: '500px', objectFit: 'cover' }}
        />
        
        {/* Canvas oculto para capturar frames */}
        <canvas ref={canvasRef} className="hidden" />

        {/* Overlay de estado */}
        {capturing && (
          <div className="absolute top-4 right-4 flex items-center gap-2 bg-green-500/20 backdrop-blur-sm border border-green-500/30 rounded-lg px-3 py-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-green-300 text-sm font-semibold">Capturando</span>
          </div>
        )}

        {/* Última emoción detectada */}
        {lastEmotion && (
          <div className="absolute bottom-4 left-4 bg-indigo-600/90 backdrop-blur-sm rounded-lg px-4 py-2">
            <div className="text-white text-sm">
              <span className="font-semibold">Última emoción:</span> {lastEmotion}
            </div>
          </div>
        )}

        {/* Contador de frames */}
        <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur-sm rounded-lg px-3 py-2">
          <div className="text-slate-300 text-xs">
            Frames: <span className="font-bold text-white">{frameCount}</span>
          </div>
        </div>
      </div>

      {/* Estado */}
      <div className="bg-slate-800/50 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <span className="text-slate-300 text-sm">
              {capturing ? 'Analizando emociones en tiempo real' : 'Cámara inactiva'}
            </span>
          </div>
          
          {capturing && (
            <div className="text-indigo-400 text-xs">
              Captura cada 2 segundos
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WebcamCapture;