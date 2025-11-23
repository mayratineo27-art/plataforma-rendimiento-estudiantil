import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BookOpen,
  Plus,
  Upload,
  FileText,
  CheckCircle2,
  Circle,
  Trash2,
  Eye,
  Clock,
  Calendar,
  TrendingUp,
  Download,
  Sparkles,
  Search,
  Filter,
  BookMarked,
  GraduationCap,
  Palette,
  Smile
} from 'lucide-react';

/**
 * 🆕 COMPONENTE MEJORADO: Análisis de Sílabos con Historial
 * - Cargar y analizar PDFs
 * - Guardar historial de análisis
 * - Marcar temas como completados
 * - Progreso visual
 */
const SyllabusAnalyzerPro = ({ userId = 1 }) => {
  const [syllabusList, setSyllabusList] = useState([]);
  const [selectedSyllabus, setSelectedSyllabus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [courses, setCourses] = useState([]);
  const [selectedCourseId, setSelectedCourseId] = useState('');

  useEffect(() => {
    loadCourses();
    loadSyllabusList();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/academic/user/${userId}/dashboard`);
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error('Error cargando cursos:', error);
    }
  };

  const loadSyllabusList = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/academic/user/${userId}/syllabus-history`);
      setSyllabusList(response.data.syllabus_list || []);
    } catch (error) {
      console.error('Error cargando historial:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file || !selectedCourseId) {
      alert('Por favor selecciona un curso primero');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    try {
      const response = await axios.post(
        `http://localhost:5000/api/academic/course/${selectedCourseId}/upload-syllabus`,
        formData
      );

      if (response.data.syllabus_analysis) {
        alert(`✅ Sílabo analizado: ${response.data.tasks_created} tareas creadas`);
        loadSyllabusList();
      }
    } catch (error) {
      console.error('Error subiendo sílabo:', error);
      alert('❌ Error al analizar el sílabo');
    } finally {
      setUploading(false);
    }
  };

  const viewSyllabusDetails = async (syllabusId) => {
    try {
      const response = await axios.get(`http://localhost:5000/api/academic/syllabus/${syllabusId}`);
      setSelectedSyllabus(response.data);
    } catch (error) {
      console.error('Error cargando detalles:', error);
    }
  };

  const toggleTopicComplete = async (topicIndex) => {
    if (!selectedSyllabus) return;

    try {
      const response = await axios.put(
        `http://localhost:5000/api/academic/syllabus/${selectedSyllabus.id}/topic/${topicIndex}/toggle`
      );
      setSelectedSyllabus(response.data.syllabus);
      loadSyllabusList();
    } catch (error) {
      console.error('Error actualizando tema:', error);
    }
  };

  const deleteSyllabus = async (syllabusId) => {
    if (!window.confirm('¿Eliminar este análisis de sílabo?')) return;

    try {
      await axios.delete(`http://localhost:5000/api/academic/syllabus/${syllabusId}`);
      loadSyllabusList();
      if (selectedSyllabus?.id === syllabusId) {
        setSelectedSyllabus(null);
      }
    } catch (error) {
      console.error('Error eliminando sílabo:', error);
    }
  };

  const calculateProgress = (topics) => {
    if (!topics || topics.length === 0) return 0;
    const completed = topics.filter(t => t.completed).length;
    return Math.round((completed / topics.length) * 100);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl">
                <FileText size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  Análisis Inteligente de Sílabos
                </h1>
                <p className="text-gray-600 mt-1">Carga, analiza y sigue tu progreso académico 📚</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Panel de Carga */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Upload className="text-indigo-600" size={24} />
                Cargar Nuevo Sílabo
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    📚 Selecciona el Curso
                  </label>
                  <select
                    value={selectedCourseId}
                    onChange={(e) => setSelectedCourseId(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="">-- Elige un curso --</option>
                    {courses.map(course => (
                      <option key={course.id} value={course.id}>
                        {course.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    📄 Archivo PDF del Sílabo
                  </label>
                  <label className="w-full flex flex-col items-center px-6 py-8 bg-gradient-to-br from-indigo-50 to-purple-50 border-2 border-dashed border-indigo-300 rounded-xl cursor-pointer hover:bg-indigo-100 transition">
                    <Upload size={40} className="text-indigo-600 mb-3" />
                    <span className="text-sm font-medium text-indigo-700">
                      {uploading ? 'Analizando con IA... 🤖' : 'Click para cargar PDF'}
                    </span>
                    <span className="text-xs text-gray-500 mt-1">
                      Máximo 10MB
                    </span>
                    <input
                      type="file"
                      accept=".pdf"
                      className="hidden"
                      onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0])}
                      disabled={uploading || !selectedCourseId}
                    />
                  </label>
                </div>

                {uploading && (
                  <div className="bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600"></div>
                      <p className="text-sm text-indigo-700 font-medium">
                        La IA está analizando tu sílabo...
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Historial de Sílabos */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Clock className="text-purple-600" size={24} />
                Historial de Análisis
              </h2>

              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                </div>
              ) : syllabusList.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="mx-auto h-16 w-16 text-gray-300 mb-3" />
                  <p className="text-gray-500 text-sm">
                    Aún no has analizado ningún sílabo
                  </p>
                </div>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {syllabusList.map(syllabus => {
                    const progress = calculateProgress(syllabus.topics);
                    return (
                      <div
                        key={syllabus.id}
                        className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
                          selectedSyllabus?.id === syllabus.id
                            ? 'border-indigo-500 bg-indigo-50'
                            : 'border-gray-200 hover:border-indigo-300'
                        }`}
                        onClick={() => viewSyllabusDetails(syllabus.id)}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-800 text-sm">
                              {syllabus.course_name}
                            </h3>
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(syllabus.uploaded_at).toLocaleDateString()}
                            </p>
                          </div>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteSyllabus(syllabus.id);
                            }}
                            className="text-red-400 hover:text-red-600"
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>

                        <div className="mt-3">
                          <div className="flex justify-between text-xs mb-1">
                            <span className="text-gray-600">Progreso</span>
                            <span className="font-bold text-indigo-600">{progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full transition-all ${
                                progress === 100 ? 'bg-green-500' : 'bg-indigo-500'
                              }`}
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
          </div>

          {/* Panel de Detalles */}
          <div className="lg:col-span-2">
            {!selectedSyllabus ? (
              <div className="bg-white rounded-2xl shadow-lg p-12 text-center h-full flex flex-col items-center justify-center">
                <Sparkles className="h-20 w-20 text-indigo-300 mb-4" />
                <h3 className="text-2xl font-bold text-gray-800 mb-2">
                  ¡Comienza tu análisis!
                </h3>
                <p className="text-gray-600">
                  Carga un PDF o selecciona un análisis del historial
                </p>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">
                      {selectedSyllabus.course_name}
                    </h2>
                    <p className="text-sm text-gray-500 mt-1">
                      Analizado el {new Date(selectedSyllabus.uploaded_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-indigo-600">
                      {calculateProgress(selectedSyllabus.topics)}%
                    </div>
                    <div className="text-xs text-gray-500">Completado</div>
                  </div>
                </div>

                {/* Información del Curso */}
                {selectedSyllabus.course_info && (
                  <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 mb-6">
                    <h3 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                      <BookMarked size={18} className="text-indigo-600" />
                      Información del Curso
                    </h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      {selectedSyllabus.course_info.professor && (
                        <div>
                          <span className="text-gray-600">Profesor:</span>
                          <p className="font-medium text-gray-800">{selectedSyllabus.course_info.professor}</p>
                        </div>
                      )}
                      {selectedSyllabus.course_info.credits && (
                        <div>
                          <span className="text-gray-600">Créditos:</span>
                          <p className="font-medium text-gray-800">{selectedSyllabus.course_info.credits}</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Lista de Temas */}
                <div>
                  <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <GraduationCap size={20} className="text-purple-600" />
                    Temas del Curso ({selectedSyllabus.topics?.length || 0})
                  </h3>

                  {!selectedSyllabus.topics || selectedSyllabus.topics.length === 0 ? (
                    <p className="text-gray-500 text-center py-8">
                      No se encontraron temas en el análisis
                    </p>
                  ) : (
                    <div className="space-y-3">
                      {selectedSyllabus.topics.map((topic, index) => (
                        <div
                          key={index}
                          className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
                            topic.completed
                              ? 'bg-green-50 border-green-300'
                              : 'bg-white border-gray-200 hover:border-indigo-300'
                          }`}
                          onClick={() => toggleTopicComplete(index)}
                        >
                          <div className="flex items-start gap-3">
                            <div className="mt-1">
                              {topic.completed ? (
                                <CheckCircle2 className="text-green-600" size={24} />
                              ) : (
                                <Circle className="text-gray-400" size={24} />
                              )}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-start justify-between">
                                <h4 className={`font-semibold ${
                                  topic.completed ? 'text-green-800 line-through' : 'text-gray-800'
                                }`}>
                                  {index + 1}. {topic.title || topic.name || topic.topic}
                                </h4>
                                {topic.weeks && (
                                  <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full">
                                    {topic.weeks}
                                  </span>
                                )}
                              </div>
                              {topic.description && (
                                <p className="text-sm text-gray-600 mt-2">
                                  {topic.description}
                                </p>
                              )}
                              {topic.objectives && topic.objectives.length > 0 && (
                                <div className="mt-2">
                                  <p className="text-xs font-semibold text-gray-700 mb-1">Objetivos:</p>
                                  <ul className="text-xs text-gray-600 list-disc list-inside space-y-1">
                                    {topic.objectives.slice(0, 3).map((obj, i) => (
                                      <li key={i}>{obj}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                              {topic.completed && topic.completed_at && (
                                <p className="text-xs text-green-600 mt-2">
                                  ✓ Completado el {new Date(topic.completed_at).toLocaleDateString()}
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
    </div>
  );
};

export default SyllabusAnalyzerPro;
