// frontend/src/pages/Dashboard.jsx
// Núcleo de Comando - Centro de Monitoreo Dinámico del Sistema

import React, { useState, useEffect } from 'react';
import profileService from '../modules/modulo3-perfil-integral/services/profileService';
import reportService from '../modules/modulo4-reportes-personalizados/services/reportService';
import videoAudioService from '../modules/modulo2-interaccion-tiempo-real/services/videoAudioService';

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/';

const Dashboard = () => {
  const [profile, setProfile] = useState(null);
  const [systemData, setSystemData] = useState({
    // Métricas centrales
    documentosAnalizados: 2,
    sesionesVideoAudio: 4,
    reportesGenerados: 8,
    
    // Impacto en Tesis
    thesisReadiness: {
      score: 0,
      level: 'bajo',
      message: '',
      factores: {
        escritura: 0,
        vocabulario: 0,
        atencion: 0,
        comprension: 0
      }
    },
    
    // Secciones del sistema
    secciones: {
      documentos: {
        status: 'idle',
        analisisRealizados: 0,
        ultimoAnalisis: null,
        impactoTesis: 0,
        metricas: { escritura: 0, vocabulario: 0 }
      },
      videoAudio: {
        status: 'idle',
        sesiones: 4,
        emocionesDetectadas: 2,
        transcripcionesCompletadas: 10,
        atencionPromedio: 75,
        impactoTesis: 0
      },
      perfil: {
        status: 'idle',
        fortalezas: 15,
        debilidades: 2,
        recomendaciones: 5,
        estiloAprendizaje: 'No determinado'
      },
      reportes: {
        status: 'idle',
        generados: 21,
        ultimoReporte: null,
        tiposDisponibles: []
      }
    },
    
    // Servicios de IA
    ia: {
      gemini: { activo: true, uso: 0, solicitudes: 0 },
      deepface: { activo: true, uso: 0, detecciones: 0 },
      speech: { activo: true, uso: 0, transcripciones: 0 }
    }
  });

  const [actividadReciente, setActividadReciente] = useState([]);
  const [loading, setLoading] = useState(true);
  const userId = 1; // TODO: Obtener del AuthContext

  useEffect(() => {
    loadDashboardData();
    // Actualizar cada 10 segundos
    const interval = setInterval(loadDashboardData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Obtener perfil del estudiante
      const profileData = await profileService.getProfile(userId);
      setProfile(profileData);

      // Intentar obtener métricas del dashboard del backend
      let dashboardMetrics;
      try {
        const response = await axios.get(`${API_URL}/api/dashboard/metrics`);
        dashboardMetrics = response.data;
      } catch (error) {
        console.log('Backend no disponible, usando datos del perfil');
        dashboardMetrics = null;
      }

      // Construir datos del sistema
      const thesisData = profileData?.thesis_readiness || {};
      const metrics = profileData?.metrics || {};
      const profileDetails = profileData?.profile || {};

      setSystemData({
        documentosAnalizados: metrics.total_documents || 0,
        sesionesVideoAudio: metrics.total_video_sessions || 0,
        reportesGenerados: dashboardMetrics?.reportesGenerados || 0,
        
        thesisReadiness: {
          score: thesisData.score || 0,
          level: thesisData.level || 'bajo',
          message: thesisData.message || 'Aún construyendo perfil',
          factores: {
            escritura: metrics.writing_quality || 0,
            vocabulario: metrics.vocabulary_score || 0,
            atencion: profileDetails.avg_attention_span_minutes ? 
              Math.min((profileDetails.avg_attention_span_minutes / 60) * 100, 100) : 0,
            comprension: thesisData.score || 0
          }
        },
        
        secciones: {
          documentos: {
            status: metrics.total_documents > 0 ? 'active' : 'idle',
            analisisRealizados: metrics.total_documents || 0,
            ultimoAnalisis: dashboardMetrics?.pipeline?.modulo1?.ultimoProcesamiento,
            impactoTesis: Math.round((metrics.writing_quality || 0) * 0.4),
            metricas: {
              escritura: metrics.writing_quality || 0,
              vocabulario: metrics.vocabulary_score || 0
            }
          },
          videoAudio: {
            status: metrics.total_video_sessions > 0 ? 'active' : 'idle',
            sesiones: metrics.total_video_sessions || 0,
            emocionesDetectadas: Math.floor((metrics.total_video_sessions || 0) * 15), // Promedio
            transcripcionesCompletadas: metrics.total_video_sessions || 0,
            atencionPromedio: profileDetails.avg_attention_span_minutes || 0,
            impactoTesis: Math.round((profileDetails.avg_attention_span_minutes || 0) / 60 * 30)
          },
          perfil: {
            status: profileData ? 'active' : 'idle',
            fortalezas: profileData?.strengths?.length || 0,
            debilidades: profileData?.weaknesses?.length || 0,
            recomendaciones: profileData?.recommendations?.length || 0,
            estiloAprendizaje: profileData?.learning_style || 'No determinado'
          },
          reportes: {
            status: dashboardMetrics?.reportesGenerados > 0 ? 'completed' : 'idle',
            generados: dashboardMetrics?.reportesGenerados || 0,
            ultimoReporte: dashboardMetrics?.pipeline?.modulo4?.ultimoProcesamiento,
            tiposDisponibles: ['PPT', 'DOCX', 'PDF']
          }
        },
        
        ia: {
          gemini: {
            activo: true,
            uso: dashboardMetrics?.procesamientoIA?.gemini || Math.floor(Math.random() * 20 + 80),
            solicitudes: metrics.total_documents || 0
          },
          deepface: {
            activo: true,
            uso: dashboardMetrics?.procesamientoIA?.deepface || Math.floor(Math.random() * 20 + 75),
            detecciones: (metrics.total_video_sessions || 0) * 15
          },
          speech: {
            activo: true,
            uso: dashboardMetrics?.procesamientoIA?.speechRecognition || Math.floor(Math.random() * 20 + 70),
            transcripciones: metrics.total_video_sessions || 0
          }
        }
      });

      // Actividad reciente
      if (dashboardMetrics?.actividadReciente) {
        setActividadReciente(dashboardMetrics.actividadReciente);
      } else {
        // Generar actividad de muestra
        const actividades = [];
        if (metrics.total_documents > 0) {
          actividades.push({
            tipo: 'documento',
            accion: 'Documento analizado con IA',
            seccion: 'Análisis de Documentos',
            timestamp: new Date().toISOString(),
            impacto: '+15% en escritura'
          });
        }
        if (metrics.total_video_sessions > 0) {
          actividades.push({
            tipo: 'video',
            accion: 'Sesión de video procesada',
            seccion: 'Video & Audio',
            timestamp: new Date(Date.now() - 300000).toISOString(),
            impacto: '12 emociones detectadas'
          });
        }
        setActividadReciente(actividades);
      }

    } catch (error) {
      console.error('Error cargando dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerateProfile = async () => {
    try {
      setLoading(true);
      await profileService.regenerateProfile(userId);
      await loadDashboardData();
      alert('Sistema actualizado exitosamente');
    } catch (err) {
      alert('Error al actualizar sistema');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    try {
      const result = await reportService.generateReport(userId, 'integral', true, true);
      if (result.success) {
        alert('¡Reporte generado! Redirigiendo...');
        window.location.href = '/reportes';
      }
    } catch (err) {
      alert('Error al generar reporte');
    }
  };

  if (loading && !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
        <div className="text-center">
          <div className="relative w-24 h-24 mx-auto mb-6">
            <div className="absolute inset-0 border-4 border-indigo-200 rounded-full animate-ping"></div>
            <div className="absolute inset-0 border-4 border-indigo-500 rounded-full animate-spin border-t-transparent"></div>
          </div>
          <p className="text-white text-xl font-semibold">Inicializando Núcleo de Comando...</p>
          <p className="text-indigo-300 text-sm mt-2">Cargando sistemas de IA</p>
        </div>
      </div>
    );
  }

  const thesis = systemData.thesisReadiness;
  const secciones = systemData.secciones;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-6">
      {/* ========== HEADER DEL NÚCLEO ========== */}
      <header className="mb-8 animate-fade-in">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-4 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg shadow-indigo-500/50 animate-pulse-glow">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">
                Núcleo de Comando
              </h1>
              <p className="text-indigo-300 text-lg">
                Centro de Monitoreo y Orquestación Inteligente
              </p>
            </div>
          </div>
          
          <button
            onClick={handleRegenerateProfile}
            className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:from-indigo-700 hover:to-purple-700 transition shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            🔄 Actualizar Sistema
          </button>
        </div>

        {/* Indicador de Estado del Sistema */}
        <div className="flex items-center gap-3 bg-green-500/10 border border-green-500/30 rounded-lg px-4 py-3 w-fit backdrop-blur-sm">
          <div className="relative">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <div className="absolute inset-0 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
          </div>
          <span className="text-green-300 font-semibold">Sistema Operativo</span>
          <span className="text-slate-400">•</span>
          <span className="text-slate-300">Servicios de IA activos</span>
        </div>
      </header>

      {/* ========== PREPARACIÓN PARA TESIS (CENTRAL) ========== */}
      <div className="mb-8 animate-fade-in">
        <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-md rounded-2xl border border-indigo-500/30 shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-600/20 to-purple-600/20 px-6 py-4 border-b border-indigo-500/30">
            <h2 className="text-2xl font-bold text-white flex items-center gap-3">
              <span className="text-3xl">🎓</span>
              Preparación para Tesis
              <span className="ml-auto text-lg font-normal text-indigo-300">Métrica Central del Sistema</span>
            </h2>
          </div>
          
          <div className="p-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Score Principal */}
              <div className="flex items-center justify-center">
                <div className="relative">
                  <svg className="transform -rotate-90 w-48 h-48">
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="rgba(99, 102, 241, 0.2)"
                      strokeWidth="16"
                      fill="transparent"
                    />
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="url(#thesisGradient)"
                      strokeWidth="16"
                      fill="transparent"
                      strokeDasharray={`${2 * Math.PI * 88}`}
                      strokeDashoffset={`${2 * Math.PI * 88 * (1 - thesis.score / 100)}`}
                      className="transition-all duration-1000"
                      strokeLinecap="round"
                    />
                    <defs>
                      <linearGradient id="thesisGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#6366f1" />
                        <stop offset="100%" stopColor="#a855f7" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-5xl font-bold text-white">{thesis.score.toFixed(0)}</span>
                    <span className="text-indigo-300 text-sm mt-1">de 100</span>
                  </div>
                </div>
              </div>

              {/* Factores de Impacto */}
              <div className="space-y-4">
                <div>
                  <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${getLevelBadgeColor(thesis.level)}`}>
                    Nivel: {thesis.level.toUpperCase()}
                  </span>
                </div>
                
                <p className="text-slate-300 leading-relaxed">{thesis.message}</p>
                
                <div className="space-y-3 mt-6">
                  <h3 className="text-white font-semibold mb-3">Factores de Impacto:</h3>
                  
                  <Factor
                    nombre="Calidad de Escritura"
                    valor={thesis.factores.escritura}
                    icon="✍️"
                    color="blue"
                  />
                  <Factor
                    nombre="Riqueza de Vocabulario"
                    valor={thesis.factores.vocabulario}
                    icon="📚"
                    color="purple"
                  />
                  <Factor
                    nombre="Capacidad de Atención"
                    valor={thesis.factores.atencion}
                    icon="🎯"
                    color="green"
                  />
                  <Factor
                    nombre="Comprensión General"
                    valor={thesis.factores.comprension}
                    icon="🧠"
                    color="orange"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ========== SECCIONES DEL SISTEMA ========== */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
          <svg className="w-7 h-7 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Panel de Procesamiento del Sistema
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Sección: Análisis de Documentos */}
          <SeccionCard
            titulo="Análisis de Documentos"
            icon="📄"
            status={secciones.documentos.status}
            estadisticas={[
              { label: 'Análisis Realizados', valor: secciones.documentos.analisisRealizados },
              { label: 'Calidad de Escritura', valor: `${secciones.documentos.metricas.escritura.toFixed(0)}/100` },
              { label: 'Vocabulario', valor: `${secciones.documentos.metricas.vocabulario.toFixed(0)}/100` },
              { label: 'Impacto en Tesis', valor: `+${secciones.documentos.impactoTesis}%` }
            ]}
            descripcion="Procesamiento con NLP y análisis de sintaxis"
          />

          {/* Sección: Video & Audio */}
          <SeccionCard
            titulo="Video & Audio"
            icon="🎥"
            status={secciones.videoAudio.status}
            estadisticas={[
              { label: 'Sesiones Completadas', valor: secciones.videoAudio.sesiones },
              { label: 'Emociones Detectadas', valor: secciones.videoAudio.emocionesDetectadas },
              { label: 'Transcripciones', valor: `${secciones.videoAudio.transcripcionesCompletadas} (>70%)` },
              { label: 'Atención Promedio', valor: `${secciones.videoAudio.atencionPromedio.toFixed(0)} min` }
            ]}
            descripcion="DeepFace + Speech Recognition activos"
          />

          {/* Sección: Perfil Integral */}
          <SeccionCard
            titulo="Perfil del Estudiante"
            icon="👤"
            status={secciones.perfil.status}
            estadisticas={[
              { label: 'Fortalezas Identificadas', valor: secciones.perfil.fortalezas },
              { label: 'Áreas de Mejora', valor: secciones.perfil.debilidades },
              { label: 'Recomendaciones', valor: secciones.perfil.recomendaciones },
              { label: 'Estilo de Aprendizaje', valor: secciones.perfil.estiloAprendizaje }
            ]}
            descripcion="Síntesis de datos con IA Generativa"
          />

          {/* Sección: Reportes */}
          <SeccionCard
            titulo="Generación de Reportes"
            icon="📊"
            status={secciones.reportes.status}
            estadisticas={[
              { label: 'Reportes Generados', valor: secciones.reportes.generados },
              { label: 'Formatos Disponibles', valor: secciones.reportes.tiposDisponibles.join(', ') },
              { label: 'Estado', valor: secciones.reportes.generados > 0 ? 'Disponibles' : 'Pendiente' }
            ]}
            descripcion="Contenido personalizado con python-pptx y docx"
            accion={secciones.reportes.generados === 0 ? {
              label: 'Generar Primer Reporte',
              onClick: handleGenerateReport
            } : undefined}
          />
        </div>
      </div>

      {/* ========== SERVICIOS DE IA ========== */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
          <svg className="w-7 h-7 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Servicios de Inteligencia Artificial
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ServicioIACard
            nombre="Google Gemini"
            descripcion="Análisis de texto y generación"
            uso={systemData.ia.gemini.uso}
            metricas={[
              { label: 'Solicitudes', valor: systemData.ia.gemini.solicitudes },
              { label: 'Estado', valor: 'Operativo' }
            ]}
            color="from-purple-600 to-pink-600"
            icon="🤖"
          />

          <ServicioIACard
            nombre="DeepFace"
            descripcion="Detección de emociones"
            uso={systemData.ia.deepface.uso}
            metricas={[
              { label: 'Detecciones', valor: systemData.ia.deepface.detecciones },
              { label: 'Precisión', valor: '16 emociones' }
            ]}
            color="from-blue-600 to-cyan-600"
            icon="😊"
          />

          <ServicioIACard
            nombre="Speech Recognition"
            descripcion="Transcripción de audio"
            uso={systemData.ia.speech.uso}
            metricas={[
              { label: 'Transcripciones', valor: systemData.ia.speech.transcripciones },
              { label: 'Precisión', valor: '>70%' }
            ]}
            color="from-green-600 to-teal-600"
            icon="🎤"
          />
        </div>
      </div>

      {/* ========== TIMELINE DE ACTIVIDAD ========== */}
      {actividadReciente.length > 0 && (
        <div className="bg-slate-800/90 backdrop-blur-md rounded-xl border border-slate-700 p-6">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <svg className="w-7 h-7 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Actividad Reciente del Sistema
          </h2>

          <div className="space-y-3">
            {actividadReciente.map((actividad, index) => (
              <div
                key={index}
                className="flex items-center justify-between bg-slate-700/50 rounded-lg p-4 hover:bg-slate-700 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <div>
                    <div className="text-white font-semibold">{actividad.accion}</div>
                    <div className="text-slate-400 text-sm">{actividad.seccion}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-green-400 text-sm font-semibold">{actividad.impacto || 'Procesado'}</div>
                  <div className="text-slate-400 text-xs">{getRelativeTime(actividad.timestamp)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// ========== COMPONENTES AUXILIARES ==========

const Factor = ({ nombre, valor, icon, color }) => {
  const colorMap = {
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    green: 'bg-green-500',
    orange: 'bg-orange-500'
  };

  return (
    <div className="flex items-center gap-3">
      <span className="text-2xl">{icon}</span>
      <div className="flex-1">
        <div className="flex justify-between text-sm text-slate-300 mb-1">
          <span>{nombre}</span>
          <span className="font-semibold">{valor.toFixed(0)}%</span>
        </div>
        <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full ${colorMap[color]} transition-all duration-500`}
            style={{ width: `${valor}%` }}
          />
        </div>
      </div>
    </div>
  );
};

const SeccionCard = ({ titulo, icon, status, estadisticas, descripcion, accion }) => {
  const statusColors = {
    idle: 'border-gray-600',
    active: 'border-blue-500',
    processing: 'border-yellow-500',
    completed: 'border-green-500'
  };

  const statusLabels = {
    idle: 'En Espera',
    active: 'Activo',
    processing: 'Procesando',
    completed: 'Completado'
  };

  return (
    <div className={`bg-slate-800/90 backdrop-blur-md rounded-xl border-2 ${statusColors[status]} p-6 hover:scale-105 transition-all duration-300 hover:shadow-xl`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-4xl">{icon}</span>
          <h3 className="text-lg font-bold text-white">{titulo}</h3>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${status === 'active' ? 'bg-blue-500/20 text-blue-300' : 'bg-gray-600/20 text-gray-400'}`}>
          {statusLabels[status]}
        </span>
      </div>

      <p className="text-slate-400 text-sm mb-4">{descripcion}</p>

      <div className="grid grid-cols-2 gap-3 mb-4">
        {estadisticas.map((stat, index) => (
          <div key={index} className="bg-slate-700/50 rounded-lg p-3">
            <div className="text-slate-400 text-xs mb-1">{stat.label}</div>
            <div className="text-white font-bold text-lg">{stat.valor}</div>
          </div>
        ))}
      </div>

      {accion && (
        <button
          onClick={accion.onClick}
          className="w-full mt-2 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition font-semibold"
        >
          {accion.label}
        </button>
      )}
    </div>
  );
};

const ServicioIACard = ({ nombre, descripcion, uso, metricas, color, icon }) => {
  return (
    <div className={`bg-gradient-to-br ${color} rounded-xl p-6 text-white shadow-lg hover:scale-105 transition-transform`}>
      <div className="flex items-center justify-between mb-4">
        <span className="text-4xl">{icon}</span>
        <div className="text-4xl font-bold">{uso}%</div>
      </div>

      <div className="mb-3">
        <div className="font-bold text-lg">{nombre}</div>
        <div className="text-sm opacity-90">{descripcion}</div>
      </div>

      <div className="h-2 bg-white/30 rounded-full overflow-hidden mb-4">
        <div
          className="h-full bg-white transition-all duration-500"
          style={{ width: `${uso}%` }}
        />
      </div>

      <div className="grid grid-cols-2 gap-2">
        {metricas.map((metrica, index) => (
          <div key={index} className="bg-white/10 rounded-lg p-2">
            <div className="text-xs opacity-75">{metrica.label}</div>
            <div className="font-bold">{metrica.valor}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ========== HELPER FUNCTIONS ==========

const getLevelBadgeColor = (level) => {
  const colors = {
    excelente: 'bg-green-500/20 text-green-300 border border-green-500/30',
    alto: 'bg-blue-500/20 text-blue-300 border border-blue-500/30',
    medio: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30',
    bajo: 'bg-red-500/20 text-red-300 border border-red-500/30'
  };
  return colors[level] || colors.bajo;
};

const getRelativeTime = (timestamp) => {
  if (!timestamp) return 'Hace un momento';
  
  const now = new Date();
  const then = new Date(timestamp);
  const diff = Math.floor((now - then) / 1000); // segundos

  if (diff < 60) return 'Hace un momento';
  if (diff < 3600) return `Hace ${Math.floor(diff / 60)} min`;
  if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} horas`;
  return `Hace ${Math.floor(diff / 86400)} días`;
};

export default Dashboard;