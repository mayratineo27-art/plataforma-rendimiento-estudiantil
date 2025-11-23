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
  Calendar
} from 'lucide-react';

const InteractiveTimeline = ({ userId, projectId = null, courseId = null }) => {
  const [timelines, setTimelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedTimelineId, setExpandedTimelineId] = useState(null);
  const [showHidden, setShowHidden] = useState(false);

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
      // Actualizar el estado local
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
    if (progress === 100) return 'bg-green-500';
    if (progress >= 70) return 'bg-blue-500';
    if (progress >= 40) return 'bg-yellow-500';
    return 'bg-gray-400';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header con filtros */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">
          Líneas de Tiempo {projectId && '- Proyecto'} {courseId && '- Curso'}
        </h2>
        <button
          onClick={() => setShowHidden(!showHidden)}
          className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition"
        >
          {showHidden ? <Eye size={16} /> : <EyeOff size={16} />}
          {showHidden ? 'Ocultar completadas' : 'Mostrar todas'}
        </button>
      </div>

      {timelines.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <Clock className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <p className="text-gray-600">No hay líneas de tiempo guardadas</p>
        </div>
      ) : (
        <div className="space-y-4">
          {timelines.map((timeline) => (
            <div
              key={timeline.id}
              className={`border rounded-lg overflow-hidden transition-all ${
                timeline.is_visible ? 'border-gray-300' : 'border-gray-200 opacity-60'
              }`}
            >
              {/* Header de la línea de tiempo */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-800 mb-2">
                      {timeline.title}
                    </h3>
                    {timeline.description && (
                      <p className="text-gray-600 text-sm">{timeline.description}</p>
                    )}
                    <div className="flex items-center gap-4 mt-3">
                      <span className="flex items-center gap-1 text-sm text-gray-600">
                        <Calendar size={14} />
                        {new Date(timeline.created_at).toLocaleDateString()}
                      </span>
                      {timeline.project_name && (
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                          {timeline.project_name}
                        </span>
                      )}
                      {timeline.course_name && (
                        <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-medium">
                          {timeline.course_name}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => toggleVisibility(timeline.id)}
                      className="p-2 hover:bg-gray-200 rounded transition"
                      title={timeline.is_visible ? 'Ocultar' : 'Mostrar'}
                    >
                      {timeline.is_visible ? <Eye size={18} /> : <EyeOff size={18} />}
                    </button>
                    <button
                      onClick={() => deleteTimeline(timeline.id)}
                      className="p-2 hover:bg-red-100 text-red-600 rounded transition"
                      title="Eliminar"
                    >
                      <Trash2 size={18} />
                    </button>
                    <button
                      onClick={() =>
                        setExpandedTimelineId(
                          expandedTimelineId === timeline.id ? null : timeline.id
                        )
                      }
                      className="p-2 hover:bg-gray-200 rounded transition"
                    >
                      {expandedTimelineId === timeline.id ? (
                        <ChevronUp size={18} />
                      ) : (
                        <ChevronDown size={18} />
                      )}
                    </button>
                  </div>
                </div>

                {/* Barra de progreso */}
                <div className="mt-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium text-gray-700">
                      Progreso: {timeline.completed_steps}/{timeline.total_steps}
                    </span>
                    <span className="font-bold text-gray-800">{timeline.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all ${getProgressColor(
                        timeline.progress
                      )}`}
                      style={{ width: `${timeline.progress}%` }}
                    ></div>
                  </div>
                </div>

                {timeline.is_completed && (
                  <div className="mt-3 flex items-center gap-2 text-green-600 font-semibold">
                    <CheckCircle size={20} />
                    <span>¡Línea de tiempo completada!</span>
                  </div>
                )}
              </div>

              {/* Pasos de la línea de tiempo (colapsable) */}
              {expandedTimelineId === timeline.id && (
                <div className="p-4 bg-white">
                  {!timeline.is_completed && (
                    <button
                      onClick={() => markAllComplete(timeline.id)}
                      className="mb-4 w-full py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition"
                    >
                      Marcar todas como completadas
                    </button>
                  )}
                  
                  <div className="space-y-3">
                    {timeline.steps.map((step, index) => (
                      <div
                        key={index}
                        className={`flex items-start gap-3 p-4 rounded-lg border-2 transition-all cursor-pointer ${
                          step.completed
                            ? 'bg-green-50 border-green-300'
                            : 'bg-white border-gray-200 hover:border-blue-300'
                        }`}
                        onClick={() => toggleStep(timeline.id, index)}
                      >
                        <div className="mt-1">
                          {step.completed ? (
                            <CheckCircle className="text-green-600" size={24} />
                          ) : (
                            <Circle className="text-gray-400" size={24} />
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-start justify-between">
                            <h4
                              className={`font-semibold ${
                                step.completed
                                  ? 'text-green-800 line-through'
                                  : 'text-gray-800'
                              }`}
                            >
                              Paso {index + 1}: {step.title || step.fase || step.step}
                            </h4>
                            {step.duration && (
                              <span className="text-sm text-gray-500 ml-2 flex items-center gap-1">
                                <Clock size={14} />
                                {step.duration}
                              </span>
                            )}
                          </div>
                          {step.description && (
                            <p className="text-gray-600 text-sm mt-2">
                              {step.description}
                            </p>
                          )}
                          {step.completed && step.completed_at && (
                            <p className="text-xs text-green-600 mt-2">
                              ✓ Completado el{' '}
                              {new Date(step.completed_at).toLocaleString()}
                            </p>
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
  );
};

export default InteractiveTimeline;
