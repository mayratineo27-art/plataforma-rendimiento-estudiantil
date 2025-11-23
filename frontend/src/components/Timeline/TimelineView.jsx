import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  CheckCircle,
  Circle,
  Clock,
  Eye,
  EyeOff,
  Trash2,
  ChevronDown,
  ChevronUp,
  Calendar,
  Target,
  TrendingUp,
  Sparkles,
  AlertCircle,
  Award,
  PlayCircle,
  Filter
} from 'lucide-react';

const TimelineView = ({ userId, projectId = null, courseId = null }) => {
  const [timelines, setTimelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);
  const [showHidden, setShowHidden] = useState(false);
  const [filterStatus, setFilterStatus] = useState('all'); // all, active, completed

  useEffect(() => {
    fetchTimelines();
  }, [userId, projectId, courseId, showHidden]);

  const fetchTimelines = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (!showHidden) params.append('visible_only', 'true');
      if (projectId) params.append('project_id', projectId);
      if (courseId) params.append('course_id', courseId);

      const response = await axios.get(
        `http://localhost:5000/api/timelines/user/${userId}?${params.toString()}`
      );
      setTimelines(response.data.timelines);
    } catch (error) {
      console.error('Error cargando líneas de tiempo:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleStep = async (timelineId, stepIndex) => {
    try {
      const response = await axios.put(
        `http://localhost:5000/api/timelines/${timelineId}/step/${stepIndex}/toggle`
      );
      setTimelines(prevTimelines =>
        prevTimelines.map(t =>
          t.id === timelineId ? response.data.timeline : t
        )
      );
    } catch (error) {
      console.error('Error marcando paso:', error);
    }
  };

  const toggleVisibility = async (timelineId) => {
    try {
      await axios.put(
        `http://localhost:5000/api/timelines/${timelineId}/visibility`
      );
      fetchTimelines();
    } catch (error) {
      console.error('Error cambiando visibilidad:', error);
    }
  };

  const deleteTimeline = async (timelineId) => {
    if (!window.confirm('¿Estás seguro de eliminar esta línea de tiempo?')) return;
    
    try {
      await axios.delete(`http://localhost:5000/api/timelines/${timelineId}`);
      fetchTimelines();
    } catch (error) {
      console.error('Error eliminando línea de tiempo:', error);
    }
  };

  const markAllComplete = async (timelineId) => {
    try {
      const response = await axios.put(
        `http://localhost:5000/api/timelines/${timelineId}/complete`
      );
      setTimelines(prevTimelines =>
        prevTimelines.map(t =>
          t.id === timelineId ? response.data.timeline : t
        )
      );
    } catch (error) {
      console.error('Error completando línea de tiempo:', error);
    }
  };

  const getProgressColor = (progress) => {
    if (progress === 100) return 'from-green-500 to-emerald-500';
    if (progress >= 70) return 'from-blue-500 to-indigo-500';
    if (progress >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-gray-400 to-gray-500';
  };

  const getProgressIcon = (progress) => {
    if (progress === 100) return <Award className="text-green-600" size={20} />;
    if (progress >= 70) return <TrendingUp className="text-blue-600" size={20} />;
    if (progress >= 40) return <Target className="text-yellow-600" size={20} />;
    return <PlayCircle className="text-gray-600" size={20} />;
  };

  const filteredTimelines = timelines.filter(t => {
    if (filterStatus === 'completed') return t.is_completed;
    if (filterStatus === 'active') return !t.is_completed;
    return true;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center py-16 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Cargando tus líneas de tiempo...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header con filtros mejorados */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-xl">
                <Sparkles size={28} className="text-white" />
              </div>
              <div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  Líneas de Tiempo IA
                </h2>
                <p className="text-gray-600 text-sm mt-1">
                  {filteredTimelines.length} {filteredTimelines.length === 1 ? 'línea de tiempo' : 'líneas de tiempo'}
                </p>
              </div>
            </div>
            
            <div className="flex gap-3">
              {/* Filtro de estado */}
              <div className="flex bg-gray-100 rounded-xl p-1">
                <button
                  onClick={() => setFilterStatus('all')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    filterStatus === 'all'
                      ? 'bg-white shadow-md text-gray-800'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Todas
                </button>
                <button
                  onClick={() => setFilterStatus('active')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    filterStatus === 'active'
                      ? 'bg-white shadow-md text-gray-800'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Activas
                </button>
                <button
                  onClick={() => setFilterStatus('completed')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    filterStatus === 'completed'
                      ? 'bg-white shadow-md text-gray-800'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Completadas
                </button>
              </div>

              {/* Mostrar/Ocultar */}
              <button
                onClick={() => setShowHidden(!showHidden)}
                className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-xl transition font-medium"
              >
                {showHidden ? <Eye size={18} /> : <EyeOff size={18} />}
                {showHidden ? 'Ocultar invisibles' : 'Mostrar todas'}
              </button>
            </div>
          </div>
        </div>

        {filteredTimelines.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-lg p-16 text-center border-2 border-dashed border-gray-300">
            <Sparkles className="mx-auto h-20 w-20 text-gray-400 mb-4" />
            <h3 className="text-2xl font-semibold text-gray-800 mb-2">
              {filterStatus === 'completed' ? '¡Aún no has completado ninguna línea de tiempo!' : 'No hay líneas de tiempo guardadas'}
            </h3>
            <p className="text-gray-600">
              {filterStatus === 'completed' 
                ? 'Completa tus primeros pasos para ver tus logros aquí'
                : 'Crea tu primera línea de tiempo con IA para organizar tu estudio'}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {filteredTimelines.map((timeline) => (
              <div
                key={timeline.id}
                className={`bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden ${
                  timeline.is_visible ? 'border-2 border-transparent' : 'opacity-60 border-2 border-gray-300'
                }`}
              >
                {/* Header de la línea de tiempo con gradiente */}
                <div className={`bg-gradient-to-r ${
                  timeline.is_completed 
                    ? 'from-green-500 to-emerald-500' 
                    : 'from-purple-500 to-indigo-500'
                } p-6 text-white`}>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        {getProgressIcon(timeline.progress)}
                        <h3 className="text-2xl font-bold">
                          {timeline.title}
                        </h3>
                      </div>
                      {timeline.description && (
                        <p className="text-white/90 text-sm mb-3">{timeline.description}</p>
                      )}
                      <div className="flex flex-wrap items-center gap-3">
                        <span className="flex items-center gap-2 text-sm bg-white/20 px-3 py-1 rounded-full backdrop-blur-sm">
                          <Calendar size={14} />
                          {new Date(timeline.created_at).toLocaleDateString()}
                        </span>
                        {timeline.project_name && (
                          <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
                            📁 {timeline.project_name}
                          </span>
                        )}
                        {timeline.course_name && (
                          <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
                            📚 {timeline.course_name}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => toggleVisibility(timeline.id)}
                        className="p-2 hover:bg-white/20 rounded-lg transition backdrop-blur-sm"
                        title={timeline.is_visible ? 'Ocultar' : 'Mostrar'}
                      >
                        {timeline.is_visible ? <Eye size={20} /> : <EyeOff size={20} />}
                      </button>
                      <button
                        onClick={() => deleteTimeline(timeline.id)}
                        className="p-2 hover:bg-red-500/80 rounded-lg transition backdrop-blur-sm"
                        title="Eliminar"
                      >
                        <Trash2 size={20} />
                      </button>
                      <button
                        onClick={() => setExpandedId(expandedId === timeline.id ? null : timeline.id)}
                        className="p-2 hover:bg-white/20 rounded-lg transition backdrop-blur-sm"
                      >
                        {expandedId === timeline.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                      </button>
                    </div>
                  </div>

                  {/* Barra de progreso mejorada */}
                  <div className="mt-6">
                    <div className="flex justify-between text-sm mb-2 font-semibold">
                      <span>
                        {timeline.completed_steps} de {timeline.total_steps} pasos completados
                      </span>
                      <span className="text-lg">{timeline.progress}%</span>
                    </div>
                    <div className="w-full bg-white/30 rounded-full h-4 overflow-hidden backdrop-blur-sm">
                      <div
                        className={`h-4 bg-gradient-to-r ${getProgressColor(timeline.progress)} transition-all duration-500 shadow-lg`}
                        style={{ width: `${timeline.progress}%` }}
                      ></div>
                    </div>
                  </div>

                  {timeline.is_completed && (
                    <div className="mt-4 flex items-center gap-3 bg-white/20 backdrop-blur-sm rounded-xl p-3">
                      <Award size={24} />
                      <span className="font-bold text-lg">¡Línea de tiempo completada! 🎉</span>
                    </div>
                  )}
                </div>

                {/* Pasos de la línea de tiempo (colapsable) */}
                {expandedId === timeline.id && (
                  <div className="p-6 bg-gradient-to-br from-gray-50 to-white">
                    {!timeline.is_completed && (
                      <button
                        onClick={() => markAllComplete(timeline.id)}
                        className="mb-6 w-full py-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all transform hover:scale-[1.02] flex items-center justify-center gap-2"
                      >
                        <CheckCircle size={20} />
                        Marcar todas como completadas
                      </button>
                    )}
                    
                    <div className="space-y-4">
                      {timeline.steps.map((step, index) => (
                        <div
                          key={index}
                          className={`flex items-start gap-4 p-5 rounded-xl border-2 transition-all cursor-pointer transform hover:scale-[1.01] ${
                            step.completed
                              ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-300 shadow-md'
                              : 'bg-white border-gray-200 hover:border-purple-300 hover:shadow-lg'
                          }`}
                          onClick={() => toggleStep(timeline.id, index)}
                        >
                          <div className="mt-1">
                            {step.completed ? (
                              <CheckCircle className="text-green-600" size={28} />
                            ) : (
                              <Circle className="text-gray-400 hover:text-purple-500 transition" size={28} />
                            )}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-start justify-between">
                              <h4 className={`font-bold text-lg ${
                                step.completed
                                  ? 'text-green-800 line-through'
                                  : 'text-gray-800'
                              }`}>
                                <span className="text-purple-600 mr-2">#{index + 1}</span>
                                {step.title || step.fase || step.step}
                              </h4>
                              {step.duration && (
                                <span className="text-sm text-gray-600 ml-3 flex items-center gap-2 bg-gray-100 px-3 py-1 rounded-full">
                                  <Clock size={14} />
                                  {step.duration}
                                </span>
                              )}
                            </div>
                            {step.description && (
                              <p className="text-gray-700 text-sm mt-2 leading-relaxed">
                                {step.description}
                              </p>
                            )}
                            {step.completed && step.completed_at && (
                              <div className="flex items-center gap-2 text-xs text-green-700 mt-3 bg-green-100 px-3 py-1 rounded-full inline-flex">
                                <CheckCircle size={12} />
                                Completado el {new Date(step.completed_at).toLocaleString()}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TimelineView;
