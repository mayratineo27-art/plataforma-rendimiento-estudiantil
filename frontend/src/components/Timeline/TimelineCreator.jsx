import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Plus,
  Clock,
  Calendar,
  Sparkles,
  Target,
  Zap,
  ArrowRight,
  Trash2,
  Edit,
  Save,
  X,
  PlayCircle,
  CheckCircle2,
  Circle,
  TrendingUp
} from 'lucide-react';

/**
 * 🆕 COMPONENTE: Creador de Líneas de Tiempo con IA
 * - Crear nueva línea de tiempo desde cero
 * - Generar pasos automáticamente con IA
 * - Editar y personalizar pasos
 * - Ver historial de líneas de tiempo
 */
const TimelineCreator = ({ userId = 1 }) => {
  const [timelines, setTimelines] = useState([]);
  const [courses, setCourses] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedTimeline, setSelectedTimeline] = useState(null);
  const [loading, setLoading] = useState(false);

  // Form states
  const [formData, setFormData] = useState({
    course_id: '',
    title: '',
    description: '',
    end_date: '',
    generate_with_ai: false,
    ai_context: ''
  });

  const [manualSteps, setManualSteps] = useState([
    { title: '', description: '', order: 1 }
  ]);

  useEffect(() => {
    loadCourses();
    loadTimelines();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/academic/user/${userId}/dashboard`);
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error('Error cargando cursos:', error);
    }
  };

  const loadTimelines = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/timeline/user/${userId}`);
      setTimelines(response.data.timelines || []);
    } catch (error) {
      console.error('Error cargando líneas de tiempo:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTimeline = async () => {
    console.log('🎯 handleCreateTimeline iniciado');
    console.log('📋 formData:', formData);
    console.log('📋 userId:', userId);
    
    if (!formData.course_id || !formData.title) {
      console.warn('⚠️ Validación falló - falta course_id o title');
      alert('Por favor completa el curso y título');
      return;
    }

    try {
      setLoading(true);
      console.log('⏳ Loading activado');

      const payload = {
        user_id: parseInt(userId),
        course_id: parseInt(formData.course_id),
        title: formData.title,
        description: formData.description,
        timeline_type: 'course',
        end_date: formData.end_date || null,
        steps: formData.generate_with_ai 
          ? [] 
          : manualSteps.filter(s => s.title.trim()).map((s, i) => ({
              title: s.title,
              description: s.description,
              order: i + 1
            }))
      };

      if (formData.generate_with_ai) {
        payload.generate_with_ai = true;
        payload.ai_context = formData.ai_context || formData.title;
      }

      console.log('📤 Enviando payload:', JSON.stringify(payload, null, 2));
      console.log('🌐 URL:', 'http://localhost:5000/api/timeline/create');

      const response = await axios.post('http://localhost:5000/api/timeline/create', payload);

      console.log('✅ Respuesta recibida:', response.data);
      alert(`✅ Línea de tiempo creada: ${response.data.timeline.title}`);
      setShowCreateModal(false);
      resetForm();
      loadTimelines();
    } catch (error) {
      console.error('❌ ERROR COMPLETO:', error);
      console.error('❌ Error.response:', error.response);
      console.error('❌ Error.response.data:', error.response?.data);
      console.error('❌ Error.message:', error.message);
      
      const errorMsg = error.response?.data?.error || error.message || 'Error desconocido';
      alert(`❌ Error al crear la línea de tiempo: ${errorMsg}`);
    } finally {
      console.log('🏁 Finalizando - desactivando loading');
      setLoading(false);
    }
  };

  const toggleStepComplete = async (timelineId, stepId) => {
    try {
      const response = await axios.put(
        `http://localhost:5000/api/timeline/${timelineId}/step/${stepId}/toggle`
      );
      
      // Actualizar el estado local
      if (selectedTimeline?.id === timelineId) {
        setSelectedTimeline(response.data.timeline);
      }
      loadTimelines();
    } catch (error) {
      console.error('Error actualizando paso:', error);
    }
  };

  const deleteTimeline = async (timelineId) => {
    if (!window.confirm('¿Eliminar esta línea de tiempo?')) return;

    try {
      await axios.delete(`http://localhost:5000/api/timeline/${timelineId}`);
      loadTimelines();
      if (selectedTimeline?.id === timelineId) {
        setSelectedTimeline(null);
      }
    } catch (error) {
      console.error('Error eliminando línea de tiempo:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      course_id: '',
      title: '',
      description: '',
      end_date: '',
      generate_with_ai: false,
      ai_context: ''
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

  const motivationalMessages = [
    '¡Crea tu ruta al éxito! 🚀',
    '¡Planifica y conquista! 🎯',
    '¡Tu camino comienza aquí! ✨',
    '¡Organiza tu victoria! 🏆',
    '¡Diseña tu futuro ahora! 💡',
    '¡El éxito se planifica! 📈'
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl">
                <Clock size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Gestor de Líneas de Tiempo
                </h1>
                <p className="text-gray-600 mt-1">Crea, organiza y sigue tus planes de estudio 🎯</p>
              </div>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all"
            >
              <Plus size={20} />
              <span className="font-semibold">
                {motivationalMessages[Math.floor(Math.random() * motivationalMessages.length)]}
              </span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Lista de Líneas de Tiempo */}
          <div className="lg:col-span-1 bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Calendar className="text-purple-600" size={24} />
              Mis Líneas de Tiempo
            </h2>

            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
              </div>
            ) : timelines.length === 0 ? (
              <div className="text-center py-12">
                <Clock className="mx-auto h-16 w-16 text-gray-300 mb-3" />
                <p className="text-gray-500 text-sm">
                  Aún no tienes líneas de tiempo
                </p>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="mt-4 text-purple-600 hover:text-purple-700 font-semibold text-sm"
                >
                  Crea tu primera línea 🚀
                </button>
              </div>
            ) : (
              <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {timelines.map(timeline => {
                  const progress = calculateProgress(timeline);
                  return (
                    <div
                      key={timeline.id}
                      className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
                        selectedTimeline?.id === timeline.id
                          ? 'border-purple-500 bg-purple-50'
                          : 'border-gray-200 hover:border-purple-300'
                      }`}
                      onClick={() => setSelectedTimeline(timeline)}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-800 text-sm">
                            {timeline.title}
                          </h3>
                          <p className="text-xs text-gray-500 mt-1">
                            {timeline.course_name}
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

                      <div className="flex items-center gap-2 text-xs text-gray-500 mb-3">
                        <Target size={12} />
                        <span>{timeline.steps?.length || 0} pasos</span>
                        {timeline.end_date && (
                          <>
                            <span>•</span>
                            <span>{new Date(timeline.end_date).toLocaleDateString()}</span>
                          </>
                        )}
                      </div>

                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-gray-600">Progreso</span>
                          <span className="font-bold text-purple-600">{progress}%</span>
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
                <Sparkles className="h-20 w-20 text-purple-300 mb-4" />
                <h3 className="text-2xl font-bold text-gray-800 mb-2">
                  ¡Empieza a planificar!
                </h3>
                <p className="text-gray-600 mb-6">
                  Crea una línea de tiempo o selecciona una existente
                </p>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all"
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
                      <p className="text-sm text-gray-500 mt-1">
                        {selectedTimeline.course_name}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-purple-600">
                        {calculateProgress(selectedTimeline)}%
                      </div>
                      <div className="text-xs text-gray-500">Completado</div>
                    </div>
                  </div>

                  {selectedTimeline.description && (
                    <p className="text-gray-600 mt-4">
                      {selectedTimeline.description}
                    </p>
                  )}

                  {selectedTimeline.end_date && (
                    <div className="mt-4 flex items-center gap-2 text-sm text-gray-600">
                      <Calendar size={16} />
                      <span>Fecha límite: {new Date(selectedTimeline.end_date).toLocaleDateString()}</span>
                    </div>
                  )}
                </div>

                {/* Pasos de la Línea de Tiempo */}
                <div>
                  <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <TrendingUp size={20} className="text-pink-600" />
                    Pasos del Plan ({selectedTimeline.steps?.length || 0})
                  </h3>

                  {!selectedTimeline.steps || selectedTimeline.steps.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">
                      Esta línea de tiempo no tiene pasos definidos
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {selectedTimeline.steps
                        .sort((a, b) => a.order - b.order)
                        .map((step, index) => (
                          <div
                            key={step.id}
                            className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
                              step.completed
                                ? 'bg-green-50 border-green-300'
                                : 'bg-white border-gray-200 hover:border-purple-300'
                            }`}
                            onClick={() => toggleStepComplete(selectedTimeline.id, step.id)}
                          >
                            <div className="flex items-start gap-3">
                              <div className="flex flex-col items-center">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                                  step.completed
                                    ? 'bg-green-500 text-white'
                                    : 'bg-purple-100 text-purple-600'
                                }`}>
                                  {step.completed ? <CheckCircle2 size={18} /> : index + 1}
                                </div>
                                {index < selectedTimeline.steps.length - 1 && (
                                  <div className={`w-0.5 h-8 mt-2 ${
                                    step.completed ? 'bg-green-300' : 'bg-gray-300'
                                  }`}></div>
                                )}
                              </div>

                              <div className="flex-1">
                                <h4 className={`font-semibold ${
                                  step.completed ? 'text-green-800 line-through' : 'text-gray-800'
                                }`}>
                                  {step.title}
                                </h4>
                                {step.description && (
                                  <p className="text-sm text-gray-600 mt-2">
                                    {step.description}
                                  </p>
                                )}
                                {step.completed && step.completed_at && (
                                  <p className="text-xs text-green-600 mt-2">
                                    ✓ Completado el {new Date(step.completed_at).toLocaleDateString()}
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
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">✨ Nueva Línea de Tiempo</h2>
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg"
                >
                  <X size={24} />
                </button>
              </div>
            </div>

            <div className="p-6 space-y-6">
              {/* Curso */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📚 Curso *
                </label>
                <select
                  value={formData.course_id}
                  onChange={(e) => setFormData({...formData, course_id: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="">-- Selecciona un curso --</option>
                  {courses.map(course => (
                    <option key={course.id} value={course.id}>
                      {course.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Título */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  🎯 Título *
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  placeholder="Ej: Plan de estudio para Parcial 1"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                />
              </div>

              {/* Descripción */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📝 Descripción
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  placeholder="Describe el objetivo de esta línea de tiempo..."
                  rows={3}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                />
              </div>

              {/* Fecha límite */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📅 Fecha Límite (Opcional)
                </label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                />
              </div>

              {/* Generar con IA */}
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-4">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.generate_with_ai}
                    onChange={(e) => setFormData({...formData, generate_with_ai: e.target.checked})}
                    className="w-5 h-5 text-purple-600"
                  />
                  <div className="flex items-center gap-2">
                    <Sparkles className="text-purple-600" size={20} />
                    <span className="font-semibold text-gray-800">
                      Generar pasos automáticamente con IA 🤖
                    </span>
                  </div>
                </label>

                {formData.generate_with_ai && (
                  <div className="mt-4">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      💡 Contexto para la IA
                    </label>
                    <textarea
                      value={formData.ai_context}
                      onChange={(e) => setFormData({...formData, ai_context: e.target.value})}
                      placeholder="Ej: Necesito estudiar para un examen de cálculo sobre derivadas e integrales..."
                      rows={3}
                      className="w-full px-4 py-3 border-2 border-purple-300 rounded-xl focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                )}
              </div>

              {/* Pasos Manuales */}
              {!formData.generate_with_ai && (
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <label className="text-sm font-semibold text-gray-700">
                      📋 Pasos de la Línea de Tiempo
                    </label>
                    <button
                      onClick={addManualStep}
                      className="text-purple-600 hover:text-purple-700 text-sm font-semibold flex items-center gap-1"
                    >
                      <Plus size={16} />
                      Agregar Paso
                    </button>
                  </div>

                  <div className="space-y-3">
                    {manualSteps.map((step, index) => (
                      <div key={index} className="border-2 border-gray-200 rounded-xl p-4">
                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold text-sm">
                            {index + 1}
                          </div>
                          <div className="flex-1 space-y-2">
                            <input
                              type="text"
                              value={step.title}
                              onChange={(e) => updateManualStep(index, 'title', e.target.value)}
                              placeholder="Título del paso"
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                            />
                            <textarea
                              value={step.description}
                              onChange={(e) => updateManualStep(index, 'description', e.target.value)}
                              placeholder="Descripción (opcional)"
                              rows={2}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                            />
                          </div>
                          {manualSteps.length > 1 && (
                            <button
                              onClick={() => removeManualStep(index)}
                              className="text-red-400 hover:text-red-600 p-2"
                            >
                              <Trash2 size={18} />
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Botones */}
              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 font-semibold"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleCreateTimeline}
                  disabled={loading}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:shadow-lg font-semibold disabled:opacity-50"
                >
                  {loading ? 'Creando...' : '✨ Crear Línea de Tiempo'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TimelineCreator;
