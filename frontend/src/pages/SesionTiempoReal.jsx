// frontend/src/pages/SesionTiempoReal.jsx
// Página principal para sesiones de video/audio en tiempo real

import React, { useState } from 'react';
import WebcamCapture from '../modules/modulo2-interaccion-tiempo-real/components/WebcamCapture';
import AudioRecorder from '../modules/modulo2-interaccion-tiempo-real/components/AudioRecorder';
import videoAudioService from '../modules/modulo2-interaccion-tiempo-real/services/videoAudioService';

const SesionTiempoReal = () => {
  const [sessionId, setSessionId] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [sessionData, setSessionData] = useState({
    emociones: [],
    transcripciones: [],
    atencionPromedio: 0,
    duracion: 0
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const userId = 1; // TODO: Obtener del AuthContext

  const handleStartSession = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await videoAudioService.startSession(userId);
      setSessionId(response.session_id);
      setIsRecording(true);
      
      console.log('Sesión iniciada:', response.session_id);
    } catch (err) {
      setError('Error al iniciar la sesión');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStopSession = async () => {
    if (!sessionId) return;

    try {
      setLoading(true);
      setIsRecording(false);

      // Detener la sesión
      const endResponse = await videoAudioService.endSession(sessionId);
      console.log('✅ Sesión detenida:', endResponse);
      
      // Intentar obtener análisis final (no bloquear si falla)
      try {
        const analysis = await videoAudioService.getSessionAnalysis(sessionId);
        setSessionData({
          emociones: analysis.emotions || [],
          transcripciones: analysis.transcripciones || [],
          atencionPromedio: analysis.atencion_promedio || 0,
          duracion: analysis.duracion || 0
        });
        console.log('✅ Análisis obtenido:', analysis);
      } catch (analysisErr) {
        console.warn('⚠️ No se pudo obtener el análisis:', analysisErr);
      }

      alert('¡Sesión detenida correctamente!');
      
      // Resetear estado
      setSessionId(null);
      setSessionData({
        emociones: [],
        transcripciones: [],
        atencionPromedio: 0,
        duracion: 0
      });
      
    } catch (err) {
      setError('Error al finalizar la sesión: ' + (err.response?.data?.message || err.message));
      console.error('❌ Error:', err);
      setIsRecording(true); // Reactivar grabación si falló
    } finally {
      setLoading(false);
    }
  };

  const handleFrameCapture = async (frameBase64) => {
    if (!sessionId) return;

    try {
      const response = await videoAudioService.analyzeFrame(sessionId, frameBase64);
      
      if (response.emotions && response.emotions.length > 0) {
        setSessionData(prev => ({
          ...prev,
          emociones: [...prev.emociones, ...response.emotions]
        }));
      }

      console.log('Emociones detectadas:', response.emotions);
    } catch (err) {
      console.error('Error analizando frame:', err);
    }
  };

  const handleAudioCapture = async (audioBlob) => {
    if (!sessionId) return;

    try {
      const response = await videoAudioService.transcribeAudio(sessionId, audioBlob);
      
      if (response.transcription) {
        setSessionData(prev => ({
          ...prev,
          transcripciones: [...prev.transcripciones, response.transcription]
        }));
      }

      console.log('Transcripción:', response.transcription);
    } catch (err) {
      console.error('Error transcribiendo audio:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-6">
      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-4 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                Sesión en Tiempo Real
              </h1>
              <p className="text-indigo-300 text-lg">
                Análisis de Video & Audio con IA
              </p>
            </div>
          </div>

          {/* Controles principales */}
          <div className="flex gap-4">
            {!isRecording ? (
              <button
                onClick={handleStartSession}
                disabled={loading}
                className="px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-semibold hover:from-green-700 hover:to-emerald-700 transition shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '⏳ Iniciando...' : '▶️ Iniciar Sesión'}
              </button>
            ) : (
              <button
                onClick={handleStopSession}
                disabled={loading}
                className="px-8 py-4 bg-gradient-to-r from-red-600 to-rose-600 text-white rounded-lg font-semibold hover:from-red-700 hover:to-rose-700 transition shadow-lg hover:shadow-xl transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '⏳ Finalizando...' : '⏹️ Detener Sesión'}
              </button>
            )}
          </div>
        </div>

        {/* Estado de la sesión */}
        {sessionId && (
          <div className="flex items-center gap-3 bg-green-500/10 border border-green-500/30 rounded-lg px-4 py-3 w-fit backdrop-blur-sm">
            <div className="relative">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <div className="absolute inset-0 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
            </div>
            <span className="text-green-300 font-semibold">Sesión Activa</span>
            <span className="text-slate-400">•</span>
            <span className="text-slate-300">ID: {sessionId}</span>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-3 backdrop-blur-sm">
            <span className="text-red-300">⚠️ {error}</span>
          </div>
        )}
      </header>

      <main className="max-w-7xl mx-auto space-y-8">
        {/* Grid de Video y Audio */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Sección de Video */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-white flex items-center gap-3">
              <span className="text-3xl">🎥</span>
              Captura de Video
            </h2>
            <WebcamCapture
              isRecording={isRecording}
              onFrameCapture={handleFrameCapture}
              onError={setError}
            />
          </div>

          {/* Sección de Audio */}
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-white flex items-center gap-3">
              <span className="text-3xl">🎤</span>
              Captura de Audio
            </h2>
            <AudioRecorder
              isRecording={isRecording}
              onAudioCapture={handleAudioCapture}
            />
          </div>
        </div>

        {/* Estadísticas en Tiempo Real */}
        {isRecording && sessionData.emociones.length > 0 && (
          <div className="bg-slate-800/90 backdrop-blur-md rounded-xl border border-indigo-500/30 p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <svg className="w-7 h-7 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Análisis en Tiempo Real
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-slate-700/50 rounded-lg p-6">
                <div className="text-slate-400 text-sm mb-2">Emociones Detectadas</div>
                <div className="text-4xl font-bold text-white">{sessionData.emociones.length}</div>
              </div>

              <div className="bg-slate-700/50 rounded-lg p-6">
                <div className="text-slate-400 text-sm mb-2">Transcripciones</div>
                <div className="text-4xl font-bold text-white">{sessionData.transcripciones.length}</div>
              </div>

              <div className="bg-slate-700/50 rounded-lg p-6">
                <div className="text-slate-400 text-sm mb-2">Duración</div>
                <div className="text-4xl font-bold text-white">
                  {Math.floor((Date.now() - (sessionId ? Date.now() : 0)) / 60000)} min
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Últimas emociones detectadas */}
        {sessionData.emociones.length > 0 && (
          <div className="bg-slate-800/90 backdrop-blur-md rounded-xl border border-slate-700 p-6">
            <h3 className="text-xl font-bold text-white mb-4">Últimas Emociones Detectadas</h3>
            <div className="flex flex-wrap gap-3">
              {sessionData.emociones.slice(-10).map((emocion, index) => (
                <div
                  key={index}
                  className="px-4 py-2 bg-indigo-600/20 border border-indigo-500/30 rounded-lg text-indigo-300 font-semibold"
                >
                  {emocion.emotion || 'Detectando...'}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Últimas transcripciones */}
        {sessionData.transcripciones.length > 0 && (
          <div className="bg-slate-800/90 backdrop-blur-md rounded-xl border border-slate-700 p-6">
            <h3 className="text-xl font-bold text-white mb-4">Transcripciones de Audio</h3>
            <div className="space-y-3">
              {sessionData.transcripciones.slice(-5).map((transcripcion, index) => (
                <div
                  key={index}
                  className="bg-slate-700/50 rounded-lg p-4"
                >
                  <p className="text-slate-300">{transcripcion.text || 'Procesando...'}</p>
                  <span className="text-xs text-slate-500 mt-2 block">
                    Precisión: {((transcripcion.confidence || 0) * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Instrucciones */}
        {!isRecording && (
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-8 backdrop-blur-sm">
            <h3 className="text-2xl font-bold text-white mb-4">📝 Instrucciones</h3>
            <ul className="space-y-3 text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">1.</span>
                <span>Haz clic en <strong>"Iniciar Sesión"</strong> para comenzar el análisis</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">2.</span>
                <span>Permite el acceso a tu cámara y micrófono cuando el navegador lo solicite</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">3.</span>
                <span>El sistema detectará tus emociones y transcribirá el audio automáticamente</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-green-400 font-bold">4.</span>
                <span>Al finalizar, haz clic en <strong>"Detener Sesión"</strong> para ver el análisis completo</span>
              </li>
            </ul>
          </div>
        )}
      </main>
    </div>
  );
};

export default SesionTiempoReal;