import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Plus,
  Clock,
  Calendar,
  Sparkles,
  Target,
  BookOpen,
  ArrowRight,
  Trash2,
  Save,
  X,
  PlayCircle,
  CheckCircle2,
  Circle,
  TrendingUp,
  Lightbulb
} from 'lucide-react';

/**
 * 🆕 COMPONENTE: Creador de Líneas de Tiempo para Temas de Curso
 * - Crear líneas de tiempo sobre temas específicos de cualquier curso
 * - No está vinculado a proyectos, solo a temas de estudio
 * - Generar pasos automáticamente con IA
 * - Seguimiento de progreso por tema
 */
const TopicTimelineCreator = ({ userId = 1 }) => {
  const [timelines, setTimelines] = useState([]);
  const [courses, setCourses] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [loading, setLoading] = useState(false);

  // Form states
  const [formData, setFormData] = useState({
    course_id: '',
    course_topic: '',
    title: '',
    description: '',
    end_date: '',
    generate_with_ai: true
  });

  const [manualSteps, setManualSteps] = useState([
    { title: '', description: '', order: 1 }
  ]);

  useEffect(() => {
    loadCourses();
    loadTopicTimelines();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/academic/user/${userId}/dashboard`);
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error('Error cargando cursos:', error);
    }
  };

  const loadTopicTimelines = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/timeline/user/${userId}`);
      // Filtrar solo las líneas de tiempo de tipo 'free'
      const topicTimelines = response.data.timelines.filter(t => t.timeline_type === 'free');
      setTimelines(topicTimelines);
    } catch (error) {
      console.error('Error cargando líneas de tiempo:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTopicTimeline = async () => {
    console.log('🎯 Creando línea de tiempo de tema');
    
    if (!formData.course_id || !formData.course_topic) {
      alert('Por favor completa el curso y el tema');
      return;
    }

    try {
      setLoading(true);

      const payload = {
        user_id: parseInt(userId),
        course_id: parseInt(formData.course_id),
        course_topic: formData.course_topic,
        title: formData.title || `Línea de tiempo: ${formData.course_topic}`,
        description: formData.description || `Estudio del tema: ${formData.course_topic}`,
        end_date: formData.end_date || null,
        generate_with_ai: formData.generate_with_ai,
        steps: formData.generate_with_ai 
          ? [] 
          : manualSteps.filter(s => s.title.trim()).map((s, i) => ({
              title: s.title,
              description: s.description,
              order: i + 1
            }))
      };

      console.log('📤 Enviando payload:', payload);

      const response = await axios.post('http://localhost:5000/api/timeline/topic/create', payload);

      console.log('✅ Respuesta recibida:', response.data);
      alert(`✅ Línea de tiempo de tema creada: ${response.data.timeline.title}`);
      setShowCreateModal(false);
      resetForm();
      loadTopicTimelines();
    } catch (error) {
      console.error('❌ Error:', error);
      const errorMsg = error.response?.data?.error || error.message || 'Error desconocido';
      alert(`❌ Error al crear la línea de tiempo: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const deleteTimeline = async (timelineId) => {
    if (!window.confirm('¿Eliminar esta línea de tiempo?')) return;

    try {
      await axios.delete(`http://localhost:5000/api/timeline/${timelineId}`);
      loadTopicTimelines();
    } catch (error) {
      console.error('Error eliminando línea de tiempo:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      course_id: '',
      course_topic: '',
      title: '',
      description: '',
      end_date: '',
      generate_with_ai: true
    });
    setManualSteps([{ title: '', description: '', order: 1 }]);
  };

  const addManualStep = () => {
    setManualSteps([...manualSteps, { title: '', description: '', order: manualSteps.length + 1 }]);
  };

  const removeManualStep = (index) => {
    setManualSteps(manualSteps.filter((_, i) => i !== index));
  };

  const updateManualStep = (index, field, value) => {
    const updated = [...manualSteps];
    updated[index][field] = value;
    setManualSteps(updated);
  };

  const getProgressColor = (progress) => {
    if (progress === 100) return 'from-green-500 to-emerald-500';
    if (progress >= 70) return 'from-blue-500 to-cyan-500';
    if (progress >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Sin fecha límite';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' });
  };

  return (
    <div className="p-6 bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-xl shadow-lg">
              <Lightbulb className="text-white" size={28} />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">
                Líneas de Tiempo por Tema
              </h1>
              <p className="text-gray-600 mt-1">
                Crea líneas de tiempo para estudiar temas específicos de tus cursos
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl hover:from-purple-700 hover:to-indigo-700 transition shadow-lg"
          >
            <Plus size={20} />
            <span className="font-semibold">Nueva Línea de Tema</span>
          </button>
        </div>
      </div>

      {/* Lista de líneas de tiempo de temas */}
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
        </div>
      ) : timelines.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl shadow-lg">
          <Lightbulb className="mx-auto text-gray-400 mb-4" size={64} />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            No hay líneas de tiempo de temas
          </h3>
          <p className="text-gray-500 mb-6">
            Crea tu primera línea de tiempo para estudiar un tema específico
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl hover:from-purple-700 hover:to-indigo-700 transition"
          >
            Crear Primera Línea de Tema
          </button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {timelines.map(timeline => (
            <div
              key={timeline.id}
              className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition"
            >
              {/* Header del timeline */}
              <div className={`p-4 bg-gradient-to-r ${getProgressColor(timeline.progress)}`}>
                <div className="flex items-start justify-between text-white">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen size={20} />
                      <span className="text-sm font-medium opacity-90">
                        {timeline.course_name}
                      </span>
                    </div>
                    <h3 className="text-xl font-bold mb-1">{timeline.title}</h3>
                    {timeline.course_topic && (
                      <p className="text-sm opacity-90 flex items-center gap-1">
                        <Target size={16} />
                        {timeline.course_topic}
                      </p>
                    )}
                  </div>
                  <button
                    onClick={() => deleteTimeline(timeline.id)}
                    className="p-2 hover:bg-white/20 rounded-lg transition"
                    title="Eliminar"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>

                {/* Barra de progreso */}
                <div className="mt-4">
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span>Progreso</span>
                    <span className="font-bold">{timeline.progress}%</span>
                  </div>
                  <div className="h-2 bg-white/30 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-white transition-all duration-500"
                      style={{ width: `${timeline.progress}%` }}
                    />
                  </div>
                  <div className="text-xs mt-1 opacity-90">
                    {timeline.completed_steps} de {timeline.total_steps} pasos completados
                  </div>
                </div>
              </div>

              {/* Contenido */}
              <div className="p-4">
                {timeline.description && (
                  <p className="text-gray-600 text-sm mb-3">{timeline.description}</p>
                )}
                
                {timeline.end_date && (
                  <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                    <Calendar size={16} />
                    <span>Fecha límite: {formatDate(timeline.end_date)}</span>
                  </div>
                )}

                {/* Pasos recientes */}
                {timeline.steps && timeline.steps.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-gray-500 uppercase">Próximos pasos</p>
                    {timeline.steps.slice(0, 3).map((step, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        {step.completed ? (
                          <CheckCircle2 size={16} className="text-green-500 mt-0.5 flex-shrink-0" />
                        ) : (
                          <Circle size={16} className="text-gray-300 mt-0.5 flex-shrink-0" />
                        )}
                        <span className={step.completed ? 'line-through text-gray-400' : 'text-gray-700'}>
                          {step.title}
                        </span>
                      </div>
                    ))}
                    {timeline.steps.length > 3 && (
                      <p className="text-xs text-gray-400 pl-6">
                        +{timeline.steps.length - 3} pasos más...
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de creación */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-purple-500 to-indigo-500 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Lightbulb size={28} />
                  <div>
                    <h2 className="text-2xl font-bold">Nueva Línea de Tiempo de Tema</h2>
                    <p className="text-purple-100 text-sm">Organiza el estudio de un tema específico</p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="p-2 hover:bg-white/20 rounded-lg transition"
                >
                  <X size={24} />
                </button>
              </div>
            </div>

            <div className="p-6 space-y-6">
              {/* Seleccionar curso */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Curso *
                </label>
                <select
                  value={formData.course_id}
                  onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                >
                  <option value="">Selecciona un curso</option>
                  {courses.map(course => (
                    <option key={course.id} value={course.id}>
                      {course.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Tema del curso */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Tema del Curso *
                </label>
                <input
                  type="text"
                  value={formData.course_topic}
                  onChange={(e) => setFormData({ ...formData, course_topic: e.target.value })}
                  placeholder="Ej: Integrales por partes, Revolución Francesa, ADN y ARN..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">
                  Escribe el tema específico que quieres estudiar
                </p>
              </div>

              {/* Título personalizado (opcional) */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Título Personalizado (opcional)
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Se generará automáticamente si lo dejas vacío"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              {/* Descripción */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Descripción (opcional)
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                  placeholder="Detalles adicionales sobre lo que quieres aprender..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              {/* Fecha límite */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Fecha Límite (opcional)
                </label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              {/* Generar con IA */}
              <div className="bg-purple-50 rounded-xl p-4">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.generate_with_ai}
                    onChange={(e) => setFormData({ ...formData, generate_with_ai: e.target.checked })}
                    className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
                  />
                  <div className="flex items-center gap-2">
                    <Sparkles className="text-purple-600" size={20} />
                    <span className="font-semibold text-gray-800">Generar pasos con IA</span>
                  </div>
                </label>
                <p className="text-sm text-gray-600 mt-2 ml-8">
                  La IA creará automáticamente pasos de estudio basados en el tema
                </p>
              </div>

              {/* Pasos manuales */}
              {!formData.generate_with_ai && (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Pasos de Estudio Manuales
                  </label>
                  <div className="space-y-3">
                    {manualSteps.map((step, index) => (
                      <div key={index} className="flex gap-2">
                        <div className="flex-1 space-y-2">
                          <input
                            type="text"
                            value={step.title}
                            onChange={(e) => updateManualStep(index, 'title', e.target.value)}
                            placeholder={`Paso ${index + 1} - Título`}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                          <input
                            type="text"
                            value={step.description}
                            onChange={(e) => updateManualStep(index, 'description', e.target.value)}
                            placeholder="Descripción (opcional)"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>
                        {manualSteps.length > 1 && (
                          <button
                            onClick={() => removeManualStep(index)}
                            className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition"
                          >
                            <Trash2 size={20} />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={addManualStep}
                    className="mt-3 flex items-center gap-2 px-4 py-2 text-purple-600 hover:bg-purple-50 rounded-lg transition"
                  >
                    <Plus size={18} />
                    <span>Añadir paso</span>
                  </button>
                </div>
              )}
            </div>

            {/* Footer con botones */}
            <div className="p-6 bg-gray-50 border-t border-gray-200 flex gap-3 justify-end">
              <button
                onClick={() => {
                  setShowCreateModal(false);
                  resetForm();
                }}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-100 transition font-semibold"
                disabled={loading}
              >
                Cancelar
              </button>
              <button
                onClick={handleCreateTopicTimeline}
                disabled={loading}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl hover:from-purple-700 hover:to-indigo-700 transition font-semibold disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Creando...</span>
                  </>
                ) : (
                  <>
                    <Save size={20} />
                    <span>Crear Línea de Tiempo</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TopicTimelineCreator;
