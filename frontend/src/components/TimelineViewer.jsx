import React, { useState } from 'react';
import { Calendar, Clock, CheckCircle, Circle, ArrowRight, Loader2, AlertCircle } from 'lucide-react';

/**
 * TimelineViewer - Visualiza líneas de tiempo generadas por IA
 * Soporta dos tipos: 'academic' (fases de un trabajo) y 'course' (temas de un curso)
 */
const TimelineViewer = () => {
  const [topic, setTopic] = useState('');
  const [timelineType, setTimelineType] = useState('academic');
  const [timeline, setTimeline] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateTimeline = async () => {
    if (!topic.trim()) {
      setError('Por favor ingresa un tema');
      return;
    }

    setLoading(true);
    setError(null);
    setTimeline(null);

    try {
      const response = await fetch('/api/academic/tools/timeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: topic,
          type: timelineType
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error al generar línea de tiempo');
      }

      setTimeline(data.timeline);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (index, totalMilestones) => {
    // Simular progreso: primeros hitos completados, uno en progreso, resto pendiente
    if (index === 0) return <CheckCircle className="w-5 h-5 text-green-500" />;
    if (index === 1) return <Circle className="w-5 h-5 text-blue-500 animate-pulse" />;
    return <Circle className="w-5 h-5 text-gray-300" />;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <Calendar className="w-6 h-6 text-indigo-600" />
        Generador de Líneas de Tiempo
      </h2>

      {/* Formulario */}
      <div className="space-y-4 mb-8">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tema del Proyecto o Curso
          </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Ej: Desarrollo de tesis sobre inteligencia artificial"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tipo de Línea de Tiempo
          </label>
          <div className="flex gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                value="academic"
                checked={timelineType === 'academic'}
                onChange={(e) => setTimelineType(e.target.value)}
                className="w-4 h-4 text-indigo-600"
              />
              <span className="text-sm text-gray-700">Trabajo Académico</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                value="course"
                checked={timelineType === 'course'}
                onChange={(e) => setTimelineType(e.target.value)}
                className="w-4 h-4 text-indigo-600"
              />
              <span className="text-sm text-gray-700">Cronología de Curso</span>
            </label>
          </div>
        </div>

        <button
          onClick={generateTimeline}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generando línea de tiempo...
            </>
          ) : (
            <>
              <Calendar className="w-5 h-5" />
              Generar Línea de Tiempo
            </>
          )}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-red-800">Error</p>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      )}

      {/* Timeline Results */}
      {timeline && !timeline.error && (
        <div className="space-y-6">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-2">
              {timeline.title}
            </h3>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Clock className="w-4 h-4" />
              <span>Tiempo total estimado: {timeline.estimated_total_time}</span>
            </div>
          </div>

          {/* Milestones */}
          <div className="relative">
            {/* Línea vertical conectora */}
            <div className="absolute left-6 top-8 bottom-8 w-0.5 bg-gray-200"></div>

            <div className="space-y-8">
              {timeline.milestones.map((milestone, index) => (
                <div key={milestone.id || index} className="relative flex gap-4">
                  {/* Icono de estado */}
                  <div className="relative z-10 flex-shrink-0">
                    <div className="w-12 h-12 rounded-full bg-white border-4 border-gray-100 flex items-center justify-center shadow-md">
                      {getStatusIcon(index, timeline.milestones.length)}
                    </div>
                  </div>

                  {/* Contenido del milestone */}
                  <div className="flex-grow bg-white border border-gray-200 rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h4 className="text-lg font-semibold text-gray-800">
                          {milestone.title}
                        </h4>
                        <p className="text-sm text-indigo-600 font-medium mt-1">
                          {milestone.duration}
                        </p>
                      </div>
                      <span className="text-xs bg-gray-100 text-gray-600 px-3 py-1 rounded-full font-medium">
                        Fase {milestone.order || index + 1}
                      </span>
                    </div>

                    <p className="text-sm text-gray-600 mb-4">
                      {milestone.description}
                    </p>

                    {/* Tareas específicas */}
                    {milestone.tasks && milestone.tasks.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                          Tareas:
                        </p>
                        <ul className="space-y-1">
                          {milestone.tasks.map((task, taskIndex) => (
                            <li key={taskIndex} className="flex items-start gap-2 text-sm text-gray-700">
                              <ArrowRight className="w-4 h-4 text-indigo-400 flex-shrink-0 mt-0.5" />
                              <span>{task}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Dependencias */}
                    {milestone.dependencies && milestone.dependencies.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-100">
                        <p className="text-xs text-gray-500">
                          <span className="font-medium">Depende de:</span>{' '}
                          {milestone.dependencies.join(', ')}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recomendaciones */}
          {timeline.recommendations && timeline.recommendations.length > 0 && (
            <div className="bg-amber-50 border-l-4 border-amber-400 p-5 rounded-r-lg">
              <h4 className="text-sm font-bold text-amber-900 mb-3 uppercase tracking-wide">
                📌 Recomendaciones
              </h4>
              <ul className="space-y-2">
                {timeline.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm text-amber-800">
                    <CheckCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Error de IA */}
      {timeline && timeline.error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-3" />
          <p className="text-red-800 font-medium">No se pudo generar la línea de tiempo</p>
          <p className="text-sm text-red-600 mt-2">{timeline.error}</p>
        </div>
      )}
    </div>
  );
};

export default TimelineViewer;
