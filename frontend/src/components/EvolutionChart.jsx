import React, { useState, useEffect } from 'react';
import { TrendingUp, Calendar, BarChart3, Loader2, AlertCircle } from 'lucide-react';

/**
 * EvolutionChart - Visualiza la evolución del tiempo de estudio
 * Muestra gráficos y estadísticas de proyectos y sesiones
 */
const EvolutionChart = ({ userId = 1, courses = [] }) => {
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedCourse) {
      loadStats(selectedCourse.id);
    }
  }, [selectedCourse]);

  const loadStats = async (courseId) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`/api/projects/course/${courseId}/stats`);
      const data = await response.json();
      
      if (response.ok) {
        setStats(data);
      } else {
        throw new Error(data.error || 'Error al cargar estadísticas');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  };

  const getBarWidth = (seconds, maxSeconds) => {
    if (maxSeconds === 0) return '0%';
    return `${(seconds / maxSeconds) * 100}%`;
  };

  const getStatusEmoji = (status) => {
    switch (status) {
      case 'completado': return '✅';
      case 'en_progreso': return '⏳';
      case 'pendiente': return '📝';
      default: return '📌';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critica': return 'bg-red-500';
      case 'alta': return 'bg-orange-500';
      case 'media': return 'bg-yellow-500';
      case 'baja': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <TrendingUp className="w-6 h-6 text-teal-600" />
        Evolución de Tiempo de Estudio
      </h2>

      {/* Selector de Curso */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Selecciona un Curso
        </label>
        <select
          value={selectedCourse?.id || ''}
          onChange={(e) => {
            const course = courses.find(c => c.id === parseInt(e.target.value));
            setSelectedCourse(course);
          }}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
        >
          <option value="">-- Selecciona un curso --</option>
          {courses.map(course => (
            <option key={course.id} value={course.id}>
              {course.name}
            </option>
          ))}
        </select>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-teal-600 animate-spin" />
        </div>
      ) : stats ? (
        <div className="space-y-6">
          {/* Tarjetas de Resumen */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
              <div className="flex items-center gap-3 mb-2">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <p className="text-sm font-medium text-blue-800">Total de Proyectos</p>
              </div>
              <p className="text-3xl font-bold text-blue-900">{stats.total_projects}</p>
            </div>

            <div className="bg-gradient-to-br from-teal-50 to-teal-100 rounded-lg p-4 border border-teal-200">
              <div className="flex items-center gap-3 mb-2">
                <Calendar className="w-5 h-5 text-teal-600" />
                <p className="text-sm font-medium text-teal-800">Tiempo Total Invertido</p>
              </div>
              <p className="text-3xl font-bold text-teal-900">
                {formatTime(stats.total_time_seconds)}
              </p>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="w-5 h-5 text-purple-600" />
                <p className="text-sm font-medium text-purple-800">Tiempo Formateado</p>
              </div>
              <p className="text-2xl font-bold text-purple-900">
                {stats.formatted_total_time}
              </p>
            </div>
          </div>

          {/* Gráfico de Barras Horizontal */}
          {stats.projects_data && stats.projects_data.length > 0 ? (
            <div>
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-teal-600" />
                Distribución de Tiempo por Proyecto
              </h3>

              <div className="space-y-4">
                {stats.projects_data.map((project, index) => {
                  const maxSeconds = Math.max(...stats.projects_data.map(p => p.total_time_seconds));
                  const barWidth = getBarWidth(project.total_time_seconds, maxSeconds);

                  return (
                    <div key={project.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2 flex-grow">
                          <span className="text-lg">{getStatusEmoji(project.status)}</span>
                          <h4 className="font-semibold text-gray-800">{project.name}</h4>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className={`w-2 h-2 rounded-full ${getPriorityColor(project.priority)}`}></span>
                          <span className="text-sm font-mono font-bold text-teal-600">
                            {project.formatted_time}
                          </span>
                        </div>
                      </div>

                      {/* Barra de Progreso */}
                      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                        <div
                          className="bg-gradient-to-r from-teal-500 to-blue-500 h-full rounded-full transition-all duration-500 flex items-center justify-end pr-2"
                          style={{ width: barWidth }}
                        >
                          {project.total_time_seconds > 0 && (
                            <span className="text-xs text-white font-medium">
                              {Math.round((project.total_time_seconds / maxSeconds) * 100)}%
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Información Adicional */}
                      <div className="flex items-center justify-between mt-2 text-xs text-gray-600">
                        <div className="flex items-center gap-4">
                          <span>
                            <span className="font-medium">Estado:</span> {project.status}
                          </span>
                          <span>
                            <span className="font-medium">Prioridad:</span> {project.priority}
                          </span>
                        </div>
                        <span>
                          <span className="font-medium">{project.session_count}</span> sesiones registradas
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <BarChart3 className="w-16 h-16 mx-auto mb-4" />
              <p>No hay datos de tiempo para este curso</p>
              <p className="text-sm">Comienza a trabajar en proyectos para ver estadísticas</p>
            </div>
          )}

          {/* Insights */}
          {stats.projects_data && stats.projects_data.length > 0 && (
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-amber-400 p-5 rounded-r-lg">
              <h4 className="text-sm font-bold text-amber-900 mb-3 uppercase tracking-wide">
                📊 Análisis Rápido
              </h4>
              <ul className="space-y-2 text-sm text-amber-800">
                <li className="flex items-start gap-2">
                  <span className="text-amber-600">•</span>
                  <span>
                    <span className="font-semibold">Proyecto con más tiempo:</span>{' '}
                    {stats.projects_data[0]?.name} ({stats.projects_data[0]?.formatted_time})
                  </span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-600">•</span>
                  <span>
                    <span className="font-semibold">Promedio por proyecto:</span>{' '}
                    {formatTime(Math.round(stats.total_time_seconds / stats.total_projects))}
                  </span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-600">•</span>
                  <span>
                    <span className="font-semibold">Total de sesiones:</span>{' '}
                    {stats.projects_data.reduce((acc, p) => acc + p.session_count, 0)} sesiones
                  </span>
                </li>
              </ul>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-400">
          <TrendingUp className="w-16 h-16 mx-auto mb-4" />
          <p>Selecciona un curso para ver estadísticas</p>
        </div>
      )}
    </div>
  );
};

export default EvolutionChart;
