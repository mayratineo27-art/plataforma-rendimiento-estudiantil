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
  BookOpen,
  Award,
  PlayCircle,
  Filter,
  Lightbulb
} from 'lucide-react';

/**
 * Vista de líneas de tiempo de temas con interacción completa
 * Permite ver, marcar pasos completos y gestionar timelines de temas
 */
const TopicTimelineView = ({ userId, courseId = null }) => {
  const [timelines, setTimelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);
  const [showHidden, setShowHidden] = useState(false);
  const [filterStatus, setFilterStatus] = useState('all'); // all, active, completed

  useEffect(() => {
    fetchTimelines();
  }, [userId, courseId, showHidden]);

  const fetchTimelines = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (!showHidden) params.append('visible_only', 'true');
      if (courseId) params.append('course_id', courseId);

      const response = await axios.get(
        `http://localhost:5000/api/timeline/user/${userId}?${params.toString()}`
      );
      
      // Filtrar solo líneas de tiempo de tipo 'free'
      const topicTimelines = response.data.timelines.filter(t => t.timeline_type === 'free');
      setTimelines(topicTimelines);
    } catch (error) {
      console.error('Error cargando líneas de tiempo:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleStep = async (timelineId, stepIndex) => {
    try {
      const response = await axios.put(
        `http://localhost:5000/api/timeline/${timelineId}/step/${stepIndex}/toggle`
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
        `http://localhost:5000/api/timeline/${timelineId}/visibility`
      );
      fetchTimelines();
    } catch (error) {
      console.error('Error cambiando visibilidad:', error);
    }
  };

  const deleteTimeline = async (timelineId) => {
    if (!window.confirm('¿Estás seguro de eliminar esta línea de tiempo?')) return;
    
    try {
      await axios.delete(`http://localhost:5000/api/timeline/${timelineId}`);
      fetchTimelines();
    } catch (error) {
      console.error('Error eliminando línea de tiempo:', error);
    }
  };

  const markAllComplete = async (timelineId) => {
    try {
      const response = await axios.put(
        `http://localhost:5000/api/timeline/${timelineId}/complete`
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
    if (progress >= 70) return 'from-blue-500 to-cyan-500';
    if (progress >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-purple-500 to-pink-500';
  };

  const getFilteredTimelines = () => {
    if (filterStatus === 'completed') {
      return timelines.filter(t => t.is_completed);
    }
    if (filterStatus === 'active') {
      return timelines.filter(t => !t.is_completed && t.progress > 0);
    }
    return timelines;
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const filteredTimelines = getFilteredTimelines();

  return (
    <div className="p-6 space-y-6">
      {/* Header con filtros */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-lg">
            <Lightbulb className="text-white" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Líneas de Tiempo de Temas</h2>
            <p className="text-gray-600 text-sm">{timelines.length} temas en seguimiento</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Filtro de estado */}
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="all">Todos</option>
            <option value="active">En progreso</option>
            <option value="completed">Completados</option>
          </select>

          {/* Toggle mostrar ocultos */}
          <button
            onClick={() => setShowHidden(!showHidden)}
            className={`px-4 py-2 rounded-lg transition flex items-center gap-2 ${
              showHidden
                ? 'bg-purple-100 text-purple-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {showHidden ? <Eye size={18} /> : <EyeOff size={18} />}
            <span>{showHidden ? 'Mostrando ocultos' : 'Solo visibles'}</span>
          </button>
        </div>
      </div>

      {/* Lista de timelines */}
      {filteredTimelines.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-2xl shadow">
          <Lightbulb className="mx-auto text-gray-400 mb-3" size={48} />
          <p className="text-gray-600">No hay líneas de tiempo de temas que mostrar</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTimelines.map(timeline => (
            <div
              key={timeline.id}
              className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition"
            >
              {/* Header */}
              <div className={`p-6 bg-gradient-to-r ${getProgressColor(timeline.progress)} text-white`}>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen size={18} />
                      <span className="text-sm font-medium opacity-90">
                        {timeline.course_name}
                      </span>
                      {timeline.course_topic && (
                        <>
                          <span className="opacity-50">•</span>
                          <span className="text-sm opacity-90 flex items-center gap-1">
                            <Target size={16} />
                            {timeline.course_topic}
                          </span>
                        </>
                      )}
                    </div>
                    <h3 className="text-2xl font-bold mb-2">{timeline.title}</h3>
                    {timeline.description && (
                      <p className="text-sm opacity-90">{timeline.description}</p>
                    )}
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

                {/* Progress bar */}
                <div className="mt-4">
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="font-medium">Progreso de estudio</span>
                    <span className="font-bold">{timeline.progress}%</span>
                  </div>
                  <div className="h-3 bg-white/30 rounded-full overflow-hidden backdrop-blur-sm">
                    <div
                      className="h-full bg-white transition-all duration-500 flex items-center justify-end pr-2"
                      style={{ width: `${timeline.progress}%` }}
                    >
                      {timeline.progress === 100 && <Award size={12} />}
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-xs mt-1 opacity-90">
                    <span>{timeline.completed_steps} de {timeline.total_steps} pasos completados</span>
                    {timeline.end_date && (
                      <span className="flex items-center gap-1">
                        <Calendar size={12} />
                        {formatDate(timeline.end_date)}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Contenido expandible */}
              {expandedId === timeline.id && (
                <div className="p-6 bg-gray-50">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-lg font-semibold text-gray-800">Pasos de Estudio</h4>
                    {timeline.progress < 100 && (
                      <button
                        onClick={() => markAllComplete(timeline.id)}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition text-sm"
                      >
                        <CheckCircle size={16} />
                        Marcar todos completos
                      </button>
                    )}
                  </div>

                  <div className="space-y-3">
                    {timeline.steps && timeline.steps.length > 0 ? (
                      timeline.steps.map((step, index) => (
                        <div
                          key={index}
                          onClick={() => toggleStep(timeline.id, index)}
                          className={`p-4 rounded-xl cursor-pointer transition ${
                            step.completed
                              ? 'bg-green-50 border-2 border-green-200'
                              : 'bg-white border-2 border-gray-200 hover:border-purple-300'
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <div className="mt-1">
                              {step.completed ? (
                                <CheckCircle className="text-green-500" size={24} />
                              ) : (
                                <Circle className="text-gray-400" size={24} />
                              )}
                            </div>
                            <div className="flex-1">
                              <h5 className={`font-semibold ${
                                step.completed ? 'text-green-700 line-through' : 'text-gray-800'
                              }`}>
                                {step.title}
                              </h5>
                              {step.description && (
                                <p className={`text-sm mt-1 ${
                                  step.completed ? 'text-green-600' : 'text-gray-600'
                                }`}>
                                  {step.description}
                                </p>
                              )}
                              {step.completed_at && (
                                <p className="text-xs text-green-600 mt-2 flex items-center gap-1">
                                  <CheckCircle size={12} />
                                  Completado el {formatDate(step.completed_at)}
                                </p>
                              )}
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-center text-gray-500 py-8">
                        No hay pasos definidos para esta línea de tiempo
                      </p>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TopicTimelineView;
