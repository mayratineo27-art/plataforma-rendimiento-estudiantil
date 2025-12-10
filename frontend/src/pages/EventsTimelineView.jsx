import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { History, Plus, Calendar, Clock, CheckCircle2, Circle, Trash2, Eye, EyeOff } from 'lucide-react';
import CreateEventsTimeline from '../components/CreateEventsTimeline';

/**
 * Vista completa para gestionar Líneas de Tiempo de EVENTOS
 * Separada de proyectos - Para eventos históricos y educativos
 */
const EventsTimelineView = ({ userId = 1 }) => {
  const [timelines, setTimelines] = useState([]);
  const [selectedTimeline, setSelectedTimeline] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all'); // 'all', 'active', 'completed'

  useEffect(() => {
    loadTimelines();
  }, []);

  const loadTimelines = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/timeline/user/${userId}`);
      
      // Filtrar solo timelines tipo 'free' sin course_id ni project_id
      const eventsTimelines = response.data.timelines?.filter(
        t => t.timeline_type === 'free' && !t.course_id && !t.project_id
      ) || [];
      
      setTimelines(eventsTimelines);
    } catch (error) {
      console.error('Error cargando líneas de tiempo:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTimelineCreated = (data) => {
    setShowCreateModal(false);
    loadTimelines();
    if (data.timeline) {
      setSelectedTimeline(data.timeline);
    }
  };

  const toggleEventComplete = async (timelineId, stepId) => {
    try {
      const response = await axios.put(
        `http://localhost:5000/api/timeline/${timelineId}/step/${stepId}/toggle`
      );
      
      if (selectedTimeline?.id === timelineId) {
        setSelectedTimeline(response.data.timeline);
      }
      loadTimelines();
    } catch (error) {
      console.error('Error actualizando evento:', error);
    }
  };

  const deleteTimeline = async (timelineId) => {
    if (!window.confirm('¿Eliminar esta línea de tiempo de eventos?')) return;

    try {
      await axios.delete(`http://localhost:5000/api/timeline/${timelineId}`);
      loadTimelines();
      if (selectedTimeline?.id === timelineId) {
        setSelectedTimeline(null);
      }
    } catch (error) {
      console.error('Error eliminando:', error);
    }
  };

  const calculateProgress = (timeline) => {
    if (!timeline.steps || timeline.steps.length === 0) return 0;
    const completed = timeline.steps.filter(s => s.completed).length;
    return Math.round((completed / timeline.steps.length) * 100);
  };

  const getProgressColor = (progress) => {
    if (progress === 100) return 'from-green-500 to-emerald-500';
    if (progress >= 70) return 'from-blue-500 to-indigo-500';
    if (progress >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-purple-500 to-pink-500';
  };

  const filteredTimelines = timelines.filter(t => {
    if (filter === 'completed') return t.is_completed;
    if (filter === 'active') return !t.is_completed;
    return true;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl">
                <History size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  Líneas de Tiempo de Eventos
                </h1>
                <p className="text-gray-600 mt-1">Organiza cronológicamente eventos históricos y educativos 📅</p>
              </div>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all"
            >
              <Plus size={20} />
              <span className="font-semibold">Nueva Línea de Tiempo</span>
            </button>
          </div>

          {/* Filtros */}
          <div className="mt-6 flex gap-3">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                filter === 'all'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Todas ({timelines.length})
            </button>
            <button
              onClick={() => setFilter('active')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                filter === 'active'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Activas ({timelines.filter(t => !t.is_completed).length})
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                filter === 'completed'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Completadas ({timelines.filter(t => t.is_completed).length})
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Lista de Líneas de Tiempo */}
          <div className="lg:col-span-1 bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Calendar className="text-indigo-600" size={24} />
              Mis Líneas de Tiempo
            </h2>

            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
              </div>
            ) : filteredTimelines.length === 0 ? (
              <div className="text-center py-12">
                <History className="mx-auto h-16 w-16 text-gray-300 mb-3" />
                <p className="text-gray-500 text-sm">
                  {filter === 'all' 
                    ? 'Aún no tienes líneas de tiempo de eventos'
                    : `No hay líneas ${filter === 'completed' ? 'completadas' : 'activas'}`}
                </p>
                {filter === 'all' && (
                  <button
                    onClick={() => setShowCreateModal(true)}
                    className="mt-4 text-indigo-600 hover:text-indigo-700 font-semibold text-sm"
                  >
                    Crea tu primera línea 🚀
                  </button>
                )}
              </div>
            ) : (
              <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {filteredTimelines.map(timeline => {
                  const progress = calculateProgress(timeline);
                  return (
                    <div
                      key={timeline.id}
                      className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
                        selectedTimeline?.id === timeline.id
                          ? 'border-indigo-500 bg-indigo-50'
                          : 'border-gray-200 hover:border-indigo-300'
                      }`}
                      onClick={() => setSelectedTimeline(timeline)}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-800 text-sm">
                            {timeline.title}
                          </h3>
                          <p className="text-xs text-gray-500 mt-1">
                            {timeline.steps?.length || 0} eventos
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteTimeline(timeline.id);
                          }}
                          className="text-red-400 hover:text-red-600"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>

                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-gray-600">Progreso</span>
                          <span className="font-bold text-indigo-600">{progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor(progress)} transition-all`}
                            style={{ width: `${progress}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Panel de Detalles */}
          <div className="lg:col-span-2">
            {!selectedTimeline ? (
              <div className="bg-white rounded-2xl shadow-lg p-12 text-center h-full flex flex-col items-center justify-center">
                <History className="h-20 w-20 text-indigo-300 mb-4" />
                <h3 className="text-2xl font-bold text-gray-800 mb-2">
                  Selecciona una línea de tiempo
                </h3>
                <p className="text-gray-600 mb-6">
                  O crea una nueva para organizar eventos cronológicamente
                </p>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all"
                >
                  Crear Nueva Línea de Tiempo
                </button>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="mb-6">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h2 className="text-2xl font-bold text-gray-800">
                        {selectedTimeline.title}
                      </h2>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-indigo-600">
                        {calculateProgress(selectedTimeline)}%
                      </div>
                      <div className="text-xs text-gray-500">Revisado</div>
                    </div>
                  </div>

                  {selectedTimeline.description && (
                    <p className="text-gray-600 mt-4">
                      {selectedTimeline.description}
                    </p>
                  )}
                </div>

                {/* Eventos */}
                <div>
                  <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <Clock size={20} className="text-indigo-600" />
                    Eventos ({selectedTimeline.steps?.length || 0})
                  </h3>

                  {!selectedTimeline.steps || selectedTimeline.steps.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">
                      Esta línea de tiempo no tiene eventos definidos
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {selectedTimeline.steps
                        .sort((a, b) => a.order - b.order)
                        .map((event, index) => (
                          <div
                            key={event.id}
                            className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
                              event.completed
                                ? 'bg-green-50 border-green-300'
                                : 'bg-white border-gray-200 hover:border-indigo-300'
                            }`}
                            onClick={() => toggleEventComplete(selectedTimeline.id, event.id)}
                          >
                            <div className="flex items-start gap-3">
                              <div className="flex flex-col items-center">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                                  event.completed
                                    ? 'bg-green-500 text-white'
                                    : 'bg-indigo-100 text-indigo-600'
                                }`}>
                                  {event.completed ? <CheckCircle2 size={18} /> : index + 1}
                                </div>
                                {index < selectedTimeline.steps.length - 1 && (
                                  <div className={`w-0.5 h-8 mt-2 ${
                                    event.completed ? 'bg-green-300' : 'bg-gray-300'
                                  }`}></div>
                                )}
                              </div>

                              <div className="flex-1">
                                <h4 className={`font-semibold ${
                                  event.completed ? 'text-green-800' : 'text-gray-800'
                                }`}>
                                  {event.title}
                                </h4>
                                {event.description && (
                                  <p className="text-sm text-gray-600 mt-2">
                                    {event.description}
                                  </p>
                                )}
                                {event.completed && event.completed_at && (
                                  <p className="text-xs text-green-600 mt-2">
                                    ✓ Revisado el {new Date(event.completed_at).toLocaleDateString()}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal de Creación */}
      {showCreateModal && (
        <CreateEventsTimeline
          userId={userId}
          onTimelineCreated={handleTimelineCreated}
          onCancel={() => setShowCreateModal(false)}
        />
      )}
    </div>
  );
};

export default EventsTimelineView;
