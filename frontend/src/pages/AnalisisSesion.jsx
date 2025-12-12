import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { videoAudioService } from '../services/videoAudioService';

export default function AnalisisSesion() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [transcriptions, setTranscriptions] = useState(null);
  const [attentionMetrics, setAttentionMetrics] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(false);

  useEffect(() => {
    loadAnalysis();
  }, [sessionId]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);

      // Cargar análisis de sesión
      const analysisData = await videoAudioService.getSessionAnalysis(sessionId);
      setAnalysis(analysisData);

      // Cargar métricas de atención
      const metricsData = await videoAudioService.getAttentionMetrics(sessionId);
      setAttentionMetrics(metricsData);

      // Cargar transcripciones
      try {
        const transcriptData = await videoAudioService.getTranscriptions(sessionId);
        setTranscriptions(transcriptData);
      } catch (err) {
        console.warn('No hay transcripciones disponibles');
      }

    } catch (error) {
      console.error('Error al cargar análisis:', error);
      alert('Error al cargar el análisis de la sesión');
    } finally {
      setLoading(false);
    }
  };

  const generateSummary = async () => {
    try {
      setLoadingSummary(true);
      const summaryData = await videoAudioService.generateSummary(sessionId);
      setSummary(summaryData.summary);
      alert('✅ Resumen generado exitosamente');
    } catch (error) {
      console.error('Error al generar resumen:', error);
      alert('Error al generar resumen: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoadingSummary(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600 text-lg">Cargando análisis...</p>
        </div>
      </div>
    );
  }

  const avgAttention = attentionMetrics?.avg_attention_score || 0;
  const attentionColor = avgAttention >= 70 ? 'text-green-600' : avgAttention >= 50 ? 'text-yellow-600' : 'text-red-600';
  const attentionBg = avgAttention >= 70 ? 'bg-green-100' : avgAttention >= 50 ? 'bg-yellow-100' : 'bg-red-100';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/sesion')}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-800 mb-4 transition-colors"
          >
            <span className="text-xl">←</span>
            Volver a Stream Multimedia
          </button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                📊 Análisis Completo de Sesión
              </h1>
              <p className="text-slate-600 mt-2">Sesión #{sessionId}</p>
            </div>
            
            {transcriptions && transcriptions.total > 0 && (
              <button
                onClick={generateSummary}
                disabled={loadingSummary}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:shadow-lg transition-all disabled:opacity-50"
              >
                <span className="text-xl">✨</span>
                {loadingSummary ? 'Generando...' : 'Generar Resumen IA'}
              </button>
            )}
          </div>
        </div>

        {/* Score de Atención Principal */}
        <div className={`${attentionBg} border-2 ${attentionColor.replace('text', 'border')} rounded-2xl p-8 mb-6 backdrop-blur-sm`}>
          <div className="text-center">
            <div className="text-6xl mb-4">👁️</div>
            <h2 className="text-2xl font-bold text-slate-800 mb-2">Nivel de Atención Promedio</h2>
            <div className={`text-7xl font-black ${attentionColor} mb-2`}>
              {avgAttention.toFixed(1)}
            </div>
            <p className="text-slate-700 text-lg">
              {avgAttention >= 80 ? '🌟 Excelente Concentración' :
               avgAttention >= 70 ? '✅ Muy Buena Atención' :
               avgAttention >= 50 ? '⚠️ Atención Moderada' :
               '❌ Baja Concentración'}
            </p>
          </div>
        </div>

        {/* Grid de Métricas */}
        <div className="grid md:grid-cols-3 gap-6 mb-6">
          {/* Duración */}
          <div className="bg-white rounded-xl shadow-md p-6 border-2 border-slate-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 bg-blue-100 rounded-lg text-2xl">
                ⏱️
              </div>
              <h3 className="font-semibold text-slate-800">Duración Total</h3>
            </div>
            <div className="text-3xl font-bold text-blue-600">
              {Math.floor((analysis?.session?.duration_seconds || 0) / 60)}m {Math.floor((analysis?.session?.duration_seconds || 0) % 60)}s
            </div>
          </div>

          {/* Frames Analizados */}
          <div className="bg-white rounded-xl shadow-md p-6 border-2 border-slate-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 bg-purple-100 rounded-lg text-2xl">
                😊
              </div>
              <h3 className="font-semibold text-slate-800">Frames Analizados</h3>
            </div>
            <div className="text-3xl font-bold text-purple-600">
              {analysis?.total_frames || 0}
            </div>
            <p className="text-sm text-slate-500 mt-1">
              {analysis?.emotion_statistics?.detection_rate?.toFixed(1)}% con rostro detectado
            </p>
          </div>

          {/* Intervalos de Atención */}
          <div className="bg-white rounded-xl shadow-md p-6 border-2 border-slate-200">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 bg-green-100 rounded-lg text-2xl">
                📊
              </div>
              <h3 className="font-semibold text-slate-800">Intervalos</h3>
            </div>
            <div className="text-3xl font-bold text-green-600">
              {attentionMetrics?.total_metrics || 0}
            </div>
            <p className="text-sm text-slate-500 mt-1">
              Análisis cada 30 segundos
            </p>
          </div>
        </div>

        {/* Métricas de Atención por Intervalos */}
        {attentionMetrics && attentionMetrics.metrics && attentionMetrics.metrics.length > 0 && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6 border-2 border-slate-200">
            <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">📈</span>
              Evolución de la Atención
            </h3>
            <div className="space-y-3">
              {attentionMetrics.metrics.map((metric, idx) => {
                const score = metric.attention_score || 0;
                const barColor = score >= 70 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500';
                const startMin = Math.floor(metric.time_interval_start / 60);
                const startSec = Math.floor(metric.time_interval_start % 60);
                const endMin = Math.floor(metric.time_interval_end / 60);
                const endSec = Math.floor(metric.time_interval_end % 60);

                return (
                  <div key={idx} className="space-y-1">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600 font-medium">
                        {startMin}:{startSec.toString().padStart(2, '0')} - {endMin}:{endSec.toString().padStart(2, '0')}
                      </span>
                      <span className="font-bold text-slate-800">{score.toFixed(1)}</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-3">
                      <div 
                        className={`${barColor} h-3 rounded-full transition-all duration-500`}
                        style={{ width: `${score}%` }}
                      ></div>
                    </div>
                    {metric.predominant_emotions && Object.keys(metric.predominant_emotions).length > 0 && (
                      <div className="flex gap-2 flex-wrap mt-1">
                        {Object.entries(metric.predominant_emotions).slice(0, 3).map(([emotion, percentage]) => (
                          <span key={emotion} className="text-xs px-2 py-1 bg-slate-100 rounded-full text-slate-600">
                            {emotion}: {percentage}%
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Resumen IA */}
        {summary && (
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-lg p-6 mb-6 border-2 border-purple-200">
            <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">✨</span>
              Resumen Inteligente (IA)
            </h3>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Temas Principales */}
              {summary.temas_principales && summary.temas_principales.length > 0 && (
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <span className="text-xl">💡</span>
                    Temas Principales
                  </h4>
                  <ul className="space-y-2">
                    {summary.temas_principales.map((tema, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-blue-600 font-bold">•</span>
                        <span className="text-slate-700">{tema}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Puntos Clave */}
              {summary.puntos_clave && summary.puntos_clave.length > 0 && (
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <span className="text-xl">✅</span>
                    Puntos Clave
                  </h4>
                  <ul className="space-y-2">
                    {summary.puntos_clave.map((punto, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-green-600 font-bold">✓</span>
                        <span className="text-slate-700">{punto}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Dudas */}
              {summary.dudas && summary.dudas.length > 0 && (
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <span className="text-xl">⚠️</span>
                    Dudas Identificadas
                  </h4>
                  <ul className="space-y-2">
                    {summary.dudas.map((duda, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-orange-600 font-bold">?</span>
                        <span className="text-slate-700">{duda}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Recomendaciones */}
              {summary.recomendaciones && summary.recomendaciones.length > 0 && (
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    <span className="text-xl">🎯</span>
                    Recomendaciones
                  </h4>
                  <ul className="space-y-2">
                    {summary.recomendaciones.map((rec, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-purple-600 font-bold">→</span>
                        <span className="text-slate-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Nivel de Comprensión */}
            {summary.nivel_comprension && (
              <div className="mt-4 p-4 bg-white rounded-lg">
                <span className="text-slate-600 font-medium">Nivel de Comprensión: </span>
                <span className={`font-bold ${
                  summary.nivel_comprension === 'alto' ? 'text-green-600' :
                  summary.nivel_comprension === 'medio' ? 'text-yellow-600' :
                  'text-red-600'
                }`}>
                  {summary.nivel_comprension.toUpperCase()}
                </span>
              </div>
            )}
          </div>
        )}

        {/* Transcripciones */}
        {transcriptions && transcriptions.total > 0 && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6 border-2 border-slate-200">
            <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">🎤</span>
              Transcripciones ({transcriptions.total})
            </h3>
            <div className="bg-slate-50 rounded-lg p-4 max-h-96 overflow-y-auto">
              <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
                {transcriptions.full_text || 'No hay texto transcrito'}
              </p>
            </div>
            <div className="mt-3 text-sm text-slate-500">
              Total de palabras: {transcriptions.word_count || 0}
            </div>
          </div>
        )}

        {/* Distribución de Emociones */}
        {analysis?.emotion_statistics?.contextual_distribution && (
          <div className="bg-white rounded-xl shadow-md p-6 border-2 border-slate-200">
            <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">😊</span>
              Emociones Detectadas
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(analysis.emotion_statistics.contextual_distribution)
                .sort((a, b) => b[1] - a[1])
                .map(([emotion, count]) => {
                  const percentage = ((count / analysis.total_frames) * 100).toFixed(1);
                  return (
                    <div key={emotion} className="bg-slate-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium text-slate-700 capitalize">{emotion}</span>
                        <span className="text-slate-500 text-sm">{count} veces</span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                      <div className="text-right text-sm text-slate-600 mt-1">{percentage}%</div>
                    </div>
                  );
                })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
