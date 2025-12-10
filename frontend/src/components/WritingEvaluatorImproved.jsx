import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Upload,
  FileText,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Book,
  Award,
  Target,
  Lightbulb,
  BarChart3,
  FileCheck,
  X,
  Loader,
  Download,
  History,
  Eye,
  Trash2,
  AlertTriangle,
  Sparkles,
  MessageSquare
} from 'lucide-react';

/**
 * WritingEvaluator Component - Versión Mejorada
 * 
 * Funcionalidades:
 * - Evaluación detallada con análisis de IA
 * - Errores específicos y sugerencias de corrección
 * - Análisis de tono y formalidad
 * - Historial de evaluaciones
 * - Descarga de reportes en PDF
 * - Comparación con versiones anteriores
 */
const WritingEvaluator = ({ userId = 1, courseId = null }) => {
  const [currentFile, setCurrentFile] = useState(null);
  const [previousFile, setPreviousFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [evaluationId, setEvaluationId] = useState(null);
  
  // Estado para historial
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  
  // Estado para vista de detalles
  const [viewingEvaluation, setViewingEvaluation] = useState(null);

  useEffect(() => {
    if (showHistory) {
      loadHistory();
    }
  }, [showHistory]);

  const loadHistory = async () => {
    try {
      setLoadingHistory(true);
      const response = await axios.get(
        `http://localhost:5000/api/academic/tools/writing-history/${userId}`
      );
      setHistory(response.data.evaluations);
    } catch (err) {
      console.error('Error cargando historial:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  const viewHistoricalEvaluation = async (evalId) => {
    try {
      setLoading(true);
      const response = await axios.get(
        `http://localhost:5000/api/academic/tools/writing-evaluation/${evalId}`
      );
      setViewingEvaluation(response.data.evaluation);
      setShowHistory(false);
    } catch (err) {
      console.error('Error cargando evaluación:', err);
      setError('Error al cargar la evaluación');
    } finally {
      setLoading(false);
    }
  };

  const deleteEvaluation = async (evalId) => {
    if (!window.confirm('¿Eliminar esta evaluación del historial?')) return;

    try {
      await axios.delete(
        `http://localhost:5000/api/academic/tools/writing-evaluation/${evalId}`
      );
      loadHistory();
    } catch (err) {
      console.error('Error eliminando:', err);
      alert('Error al eliminar la evaluación');
    }
  };

  const downloadPDF = async (evalId) => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/academic/tools/writing-evaluation/${evalId}/pdf`,
        { responseType: 'blob' }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `evaluacion_${evalId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Error descargando PDF:', err);
      alert('Error al descargar el PDF');
    }
  };

  const handleFileChange = (event, type) => {
    const file = event.target.files[0];
    
    if (!file) return;
    
    const allowedExtensions = ['.txt', '.pdf', '.docx', '.md'];
    const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!allowedExtensions.includes(fileExt)) {
      setError(`Formato no válido: ${fileExt}. Use: ${allowedExtensions.join(', ')}`);
      return;
    }
    
    setError(null);
    
    if (type === 'current') {
      setCurrentFile(file);
    } else {
      setPreviousFile(file);
    }
  };

  const handleSubmit = async () => {
    if (!currentFile) {
      setError('Por favor selecciona un documento');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setReport(null);
      setViewingEvaluation(null);

      const formData = new FormData();
      formData.append('document', currentFile);
      
      if (previousFile) {
        formData.append('previous_document', previousFile);
      }
      
      formData.append('user_id', userId);
      formData.append('save_to_history', 'true');
      
      if (courseId) {
        formData.append('course_id', courseId);
      }

      const response = await axios.post(
        'http://localhost:5000/api/academic/tools/evaluate-writing',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setReport(response.data.report);
      setEvaluationId(response.data.evaluation_id);

    } catch (err) {
      console.error('❌ Error:', err);
      const errorMsg = err.response?.data?.error || err.message || 'Error desconocido';
      setError(`Error al evaluar: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setCurrentFile(null);
    setPreviousFile(null);
    setReport(null);
    setError(null);
    setEvaluationId(null);
    setViewingEvaluation(null);
  };

  const getScoreColor = (score) => {
    if (score >= 85) return 'text-green-600 bg-green-100';
    if (score >= 70) return 'text-blue-600 bg-blue-100';
    if (score >= 50) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreLabel = (score) => {
    if (score >= 85) return 'Excelente';
    if (score >= 70) return 'Bueno';
    if (score >= 50) return 'Regular';
    return 'Necesita Mejora';
  };

  const getPriorityColor = (priority) => {
    if (priority === 'alta') return 'bg-red-100 text-red-700';
    if (priority === 'media') return 'bg-yellow-100 text-yellow-700';
    return 'bg-blue-100 text-blue-700';
  };

  // Determinar qué reporte mostrar (nuevo o histórico)
  const displayReport = viewingEvaluation || (report ? {
    file_name: report.file_name,
    evaluated_at: report.evaluated_at,
    metrics: report.metrics,
    evaluation: report.evaluation
  } : null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl">
                <FileCheck size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  Evaluador de Escritura con IA
                </h1>
                <p className="text-gray-600 mt-1">
                  Análisis exhaustivo con correcciones específicas 📝✨
                </p>
              </div>
            </div>
            
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-all"
            >
              <History size={20} />
              Historial
            </button>
          </div>
        </div>

        {/* Historial */}
        {showHistory && (
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <History className="text-indigo-600" size={28} />
                Historial de Evaluaciones
              </h2>
              <button
                onClick={() => setShowHistory(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-all"
              >
                <X size={24} />
              </button>
            </div>

            {loadingHistory ? (
              <div className="text-center py-8">
                <Loader className="animate-spin mx-auto text-indigo-600" size={40} />
                <p className="text-gray-600 mt-3">Cargando historial...</p>
              </div>
            ) : history.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <FileText size={48} className="mx-auto mb-3 opacity-50" />
                <p>No hay evaluaciones previas</p>
              </div>
            ) : (
              <div className="space-y-3">
                {history.map((evaluation) => (
                  <div
                    key={evaluation.id}
                    className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-xl hover:border-indigo-300 transition-all"
                  >
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-800">{evaluation.file_name}</h3>
                      <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
                        <span>{new Date(evaluation.evaluated_at).toLocaleDateString()}</span>
                        <span className="flex items-center gap-1">
                          <Award size={16} />
                          {evaluation.overall_score}/100
                        </span>
                        <span>{evaluation.word_count} palabras</span>
                        {evaluation.improvement_percentage && (
                          <span className="text-green-600 flex items-center gap-1">
                            <TrendingUp size={16} />
                            +{evaluation.improvement_percentage}%
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => viewHistoricalEvaluation(evaluation.id)}
                        className="p-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-all"
                        title="Ver detalles"
                      >
                        <Eye size={20} />
                      </button>
                      <button
                        onClick={() => downloadPDF(evaluation.id)}
                        className="p-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-all"
                        title="Descargar PDF"
                      >
                        <Download size={20} />
                      </button>
                      <button
                        onClick={() => deleteEvaluation(evaluation.id)}
                        className="p-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-all"
                        title="Eliminar"
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Upload Form */}
        {!displayReport && !showHistory && (
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              <Upload className="text-indigo-600" size={28} />
              Subir Documento
            </h2>

            {/* Current Document */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                📄 Documento Actual *
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-indigo-400 transition-all">
                <input
                  type="file"
                  accept=".txt,.pdf,.docx,.md"
                  onChange={(e) => handleFileChange(e, 'current')}
                  className="hidden"
                  id="current-file"
                />
                <label htmlFor="current-file" className="cursor-pointer">
                  <FileText size={48} className="mx-auto text-gray-400 mb-3" />
                  {currentFile ? (
                    <div>
                      <p className="text-lg font-semibold text-indigo-600">
                        {currentFile.name}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {(currentFile.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-lg font-semibold text-gray-700">
                        Click para seleccionar archivo
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        TXT, PDF, DOCX o MD
                      </p>
                    </div>
                  )}
                </label>
              </div>
            </div>

            {/* Previous Document */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-3">
                📋 Documento Anterior (Opcional)
              </label>
              <p className="text-xs text-gray-500 mb-2">
                Sube una versión anterior para comparar tu progreso
              </p>
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-purple-400 transition-all">
                <input
                  type="file"
                  accept=".txt,.pdf,.docx,.md"
                  onChange={(e) => handleFileChange(e, 'previous')}
                  className="hidden"
                  id="previous-file"
                />
                <label htmlFor="previous-file" className="cursor-pointer">
                  <FileText size={48} className="mx-auto text-gray-400 mb-3" />
                  {previousFile ? (
                    <div>
                      <p className="text-lg font-semibold text-purple-600">
                        {previousFile.name}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {(previousFile.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-lg font-semibold text-gray-700">
                        Click para seleccionar versión anterior
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        Opcional - para comparar progreso
                      </p>
                    </div>
                  )}
                </label>
              </div>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-50 border-2 border-red-300 rounded-xl flex items-center gap-3">
                <AlertCircle className="text-red-600" size={24} />
                <p className="text-red-700 font-semibold">{error}</p>
              </div>
            )}

            <button
              onClick={handleSubmit}
              disabled={loading || !currentFile}
              className={`w-full py-4 rounded-xl font-bold text-lg transition-all flex items-center justify-center gap-3 ${
                loading || !currentFile
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:shadow-lg hover:scale-105'
              }`}
            >
              {loading ? (
                <>
                  <Loader className="animate-spin" size={24} />
                  Evaluando con IA...
                </>
              ) : (
                <>
                  <Sparkles size={24} />
                  Evaluar mi Escritura
                </>
              )}
            </button>
          </div>
        )}

        {/* Report Display */}
        {displayReport && (
          <div className="space-y-6">
            {/* Overall Score */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-xl p-8 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-bold mb-2">
                    Reporte de Evaluación
                  </h2>
                  <p className="text-indigo-100">
                    {displayReport.file_name}
                  </p>
                  {displayReport.evaluated_at && (
                    <p className="text-indigo-200 text-sm mt-1">
                      {new Date(displayReport.evaluated_at).toLocaleString()}
                    </p>
                  )}
                </div>
                <div className="text-center">
                  <div className="text-6xl font-bold">
                    {displayReport.evaluation.overall_score || displayReport.evaluation.scores?.overall}
                  </div>
                  <div className="text-xl mt-2">
                    {getScoreLabel(displayReport.evaluation.overall_score || displayReport.evaluation.scores?.overall)}
                  </div>
                </div>
              </div>
            </div>

            {/* Actions Bar */}
            <div className="flex gap-4">
              {evaluationId && (
                <button
                  onClick={() => downloadPDF(evaluationId)}
                  className="flex-1 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition-all flex items-center justify-center gap-2"
                >
                  <Download size={20} />
                  Descargar PDF
                </button>
              )}
              <button
                onClick={resetForm}
                className="flex-1 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-all flex items-center justify-center gap-2"
              >
                <Upload size={20} />
                Nueva Evaluación
              </button>
            </div>

            {/* Improvement Badge */}
            {displayReport.evaluation.improvement_percentage !== undefined && (
              <div className="bg-green-50 border-2 border-green-300 rounded-2xl p-6">
                <div className="flex items-center gap-3">
                  <TrendingUp size={32} className="text-green-600" />
                  <div>
                    <h3 className="text-xl font-bold text-green-800">
                      ¡Mejora del {displayReport.evaluation.improvement_percentage}%!
                    </h3>
                    <p className="text-green-700">
                      Tu escritura ha mejorado comparado con la versión anterior
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Scores Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'Gramática', score: displayReport.evaluation.grammar_score || displayReport.evaluation.scores?.grammar, icon: Book },
                { label: 'Coherencia', score: displayReport.evaluation.coherence_score || displayReport.evaluation.scores?.coherence, icon: Target },
                { label: 'Vocabulario', score: displayReport.evaluation.vocabulary_score || displayReport.evaluation.scores?.vocabulary, icon: FileText },
                { label: 'Estructura', score: displayReport.evaluation.structure_score || displayReport.evaluation.scores?.structure, icon: BarChart3 }
              ].map((item, idx) => (
                <div key={idx} className="bg-white rounded-xl shadow-lg p-6 text-center">
                  <item.icon size={32} className="mx-auto text-indigo-600 mb-3" />
                  <div className={`text-3xl font-bold mb-2 ${getScoreColor(item.score)}`}>
                    {item.score}
                  </div>
                  <div className="text-sm font-semibold text-gray-700">
                    {item.label}
                  </div>
                </div>
              ))}
            </div>

            {/* Style Analysis */}
            {displayReport.evaluation.analysis && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <MessageSquare className="text-purple-600" />
                  Análisis de Estilo
                </h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-sm text-gray-600">Tono</div>
                    <div className="text-lg font-bold text-purple-700 capitalize">
                      {displayReport.evaluation.analysis.tone || displayReport.evaluation.tone_analysis || 'N/A'}
                    </div>
                  </div>
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-sm text-gray-600">Formalidad</div>
                    <div className="text-lg font-bold text-blue-700">
                      {displayReport.evaluation.analysis.formality || displayReport.evaluation.formality_score || 'N/A'}/100
                    </div>
                  </div>
                  <div className="text-center p-4 bg-indigo-50 rounded-lg">
                    <div className="text-sm text-gray-600">Complejidad</div>
                    <div className="text-lg font-bold text-indigo-700 capitalize">
                      {displayReport.evaluation.analysis.complexity || displayReport.evaluation.complexity_level || 'N/A'}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Metrics */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <BarChart3 className="text-indigo-600" />
                Métricas del Documento
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600">
                    {displayReport.metrics?.word_count || displayReport.metrics?.current?.word_count}
                  </div>
                  <div className="text-sm text-gray-600">Palabras</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {displayReport.metrics?.sentence_count || displayReport.metrics?.current?.sentence_count}
                  </div>
                  <div className="text-sm text-gray-600">Oraciones</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-pink-600">
                    {displayReport.metrics?.vocabulary_size || displayReport.metrics?.current?.vocabulary_size}
                  </div>
                  <div className="text-sm text-gray-600">Vocabulario Único</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {displayReport.metrics?.readability_score || displayReport.metrics?.current?.readability_score}
                  </div>
                  <div className="text-sm text-gray-600">Legibilidad</div>
                </div>
              </div>
            </div>

            {/* Specific Errors */}
            {displayReport.evaluation.specific_errors && displayReport.evaluation.specific_errors.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-red-800 mb-4 flex items-center gap-2">
                  <AlertTriangle className="text-red-600" />
                  Errores Específicos Detectados
                </h3>
                <div className="space-y-4">
                  {displayReport.evaluation.specific_errors.map((error, idx) => (
                    <div key={idx} className="p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="px-2 py-1 bg-red-200 text-red-800 text-xs font-bold rounded uppercase">
                              {error.type}
                            </span>
                            {error.location && (
                              <span className="text-xs text-gray-600">
                                {error.location}
                              </span>
                            )}
                          </div>
                          <div className="mb-2">
                            <span className="font-semibold text-red-700">Error: </span>
                            <span className="line-through text-gray-700">{error.error}</span>
                            <span className="mx-2">→</span>
                            <span className="font-semibold text-green-700">{error.correction}</span>
                          </div>
                          {error.explanation && (
                            <p className="text-sm text-gray-600 italic">
                              {error.explanation}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Suggestions */}
            {displayReport.evaluation.suggestions && displayReport.evaluation.suggestions.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-blue-800 mb-4 flex items-center gap-2">
                  <Sparkles className="text-blue-600" />
                  Sugerencias de Mejora
                </h3>
                <div className="space-y-3">
                  {displayReport.evaluation.suggestions.map((sugg, idx) => (
                    <div key={idx} className="p-4 bg-blue-50 rounded-lg">
                      <div className="flex items-start gap-3">
                        <span className={`px-2 py-1 text-xs font-bold rounded uppercase ${getPriorityColor(sugg.priority)}`}>
                          {sugg.category}
                        </span>
                        <div className="flex-1">
                          <p className="font-semibold text-gray-800 mb-1">
                            {sugg.suggestion}
                          </p>
                          {sugg.example && (
                            <p className="text-sm text-gray-600 italic">
                              Ejemplo: {sugg.example}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Strengths */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-green-800 mb-4 flex items-center gap-2">
                <CheckCircle className="text-green-600" />
                Fortalezas
              </h3>
              <ul className="space-y-2">
                {(displayReport.evaluation.strengths || displayReport.evaluation.evaluation?.strengths || []).map((strength, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <CheckCircle size={20} className="text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Weaknesses */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-orange-800 mb-4 flex items-center gap-2">
                <AlertCircle className="text-orange-600" />
                Áreas de Mejora
              </h3>
              <ul className="space-y-2">
                {(displayReport.evaluation.weaknesses || displayReport.evaluation.evaluation?.weaknesses || []).map((weakness, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <AlertCircle size={20} className="text-orange-600 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{weakness}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Improvements */}
            {displayReport.evaluation.improvements_made && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-blue-800 mb-4 flex items-center gap-2">
                  <TrendingUp className="text-blue-600" />
                  Mejoras Realizadas
                </h3>
                <ul className="space-y-2">
                  {displayReport.evaluation.improvements_made.map((improvement, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <TrendingUp size={20} className="text-blue-600 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{improvement}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommendations */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-indigo-800 mb-4 flex items-center gap-2">
                <Lightbulb className="text-indigo-600" />
                Recomendaciones
              </h3>
              <ul className="space-y-3">
                {(displayReport.evaluation.recommendations || displayReport.evaluation.evaluation?.recommendations || []).map((rec, idx) => (
                  <li key={idx} className="flex items-start gap-3 p-3 bg-indigo-50 rounded-lg">
                    <Lightbulb size={20} className="text-indigo-600 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Summary */}
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-purple-800 mb-3">
                Resumen General
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {displayReport.evaluation.summary || displayReport.evaluation.evaluation?.summary}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WritingEvaluator;
