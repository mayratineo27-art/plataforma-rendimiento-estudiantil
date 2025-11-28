import React, { useState } from 'react';
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
  Loader
} from 'lucide-react';

/**
 * WritingEvaluator Component
 * 
 * Permite al usuario subir documentos de escritura y recibir evaluación con IA.
 * 
 * Funcionalidades:
 * - Subir documento actual (TXT, PDF, DOCX)
 * - Subir documento anterior para comparar progreso (opcional)
 * - Ver reporte detallado con scores
 * - Ver métricas, fortalezas, debilidades y recomendaciones
 * - Comparación visual si hay versión anterior
 */
const WritingEvaluator = ({ userId = 1, courseId = null }) => {
  const [currentFile, setCurrentFile] = useState(null);
  const [previousFile, setPreviousFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event, type) => {
    const file = event.target.files[0];
    
    if (!file) return;
    
    // Validar extensión
    const allowedExtensions = ['.txt', '.pdf', '.docx', '.md'];
    const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!allowedExtensions.includes(fileExt)) {
      setError(`Formato no válido: ${fileExt}. Use: ${allowedExtensions.join(', ')}`);
      return;
    }
    
    setError(null);
    
    if (type === 'current') {
      setCurrentFile(file);
      console.log('📄 Archivo actual seleccionado:', file.name);
    } else {
      setPreviousFile(file);
      console.log('📄 Archivo anterior seleccionado:', file.name);
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

      // Preparar FormData
      const formData = new FormData();
      formData.append('document', currentFile);
      
      if (previousFile) {
        formData.append('previous_document', previousFile);
      }
      
      formData.append('user_id', userId);
      
      if (courseId) {
        formData.append('course_id', courseId);
      }

      console.log('📤 Enviando documentos para evaluación...');

      const response = await axios.post(
        'http://localhost:5000/api/academic/tools/evaluate-writing',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      console.log('✅ Reporte recibido:', response.data);
      setReport(response.data.report);

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl">
              <FileCheck size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Evaluador de Escritura con IA
              </h1>
              <p className="text-gray-600 mt-1">
                Sube tu documento y recibe feedback detallado sobre tu escritura 📝
              </p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        {!report ? (
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              <Upload className="text-indigo-600" size={28} />
              Subir Documento
            </h2>

            {/* Current Document Upload */}
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

            {/* Previous Document Upload (Optional) */}
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

            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border-2 border-red-300 rounded-xl flex items-center gap-3">
                <AlertCircle className="text-red-600" size={24} />
                <p className="text-red-700 font-semibold">{error}</p>
              </div>
            )}

            {/* Submit Button */}
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
                  Evaluando...
                </>
              ) : (
                <>
                  <Award size={24} />
                  Evaluar mi Escritura
                </>
              )}
            </button>
          </div>
        ) : (
          /* Report Display */
          <div className="space-y-6">
            {/* Overall Score */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-xl p-8 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-bold mb-2">
                    Reporte de Evaluación
                  </h2>
                  <p className="text-indigo-100">
                    {report.file_name}
                  </p>
                </div>
                <div className="text-center">
                  <div className="text-6xl font-bold">
                    {report.evaluation.overall_score}
                  </div>
                  <div className="text-xl mt-2">
                    {getScoreLabel(report.evaluation.overall_score)}
                  </div>
                </div>
              </div>
            </div>

            {/* Improvement Badge (if comparing) */}
            {report.evaluation.improvement_percentage !== undefined && (
              <div className="bg-green-50 border-2 border-green-300 rounded-2xl p-6">
                <div className="flex items-center gap-3">
                  <TrendingUp size={32} className="text-green-600" />
                  <div>
                    <h3 className="text-xl font-bold text-green-800">
                      ¡Mejora del {report.evaluation.improvement_percentage}%!
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
                { label: 'Gramática', score: report.evaluation.grammar_score, icon: Book },
                { label: 'Coherencia', score: report.evaluation.coherence_score, icon: Target },
                { label: 'Vocabulario', score: report.evaluation.vocabulary_score, icon: FileText },
                { label: 'Estructura', score: report.evaluation.structure_score, icon: BarChart3 }
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

            {/* Metrics */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <BarChart3 className="text-indigo-600" />
                Métricas del Documento
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600">
                    {report.metrics.current.word_count}
                  </div>
                  <div className="text-sm text-gray-600">Palabras</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {report.metrics.current.sentence_count}
                  </div>
                  <div className="text-sm text-gray-600">Oraciones</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-pink-600">
                    {report.metrics.current.vocabulary_size}
                  </div>
                  <div className="text-sm text-gray-600">Vocabulario Único</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {report.metrics.current.readability_score}
                  </div>
                  <div className="text-sm text-gray-600">Legibilidad</div>
                </div>
              </div>
            </div>

            {/* Strengths */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-green-800 mb-4 flex items-center gap-2">
                <CheckCircle className="text-green-600" />
                Fortalezas
              </h3>
              <ul className="space-y-2">
                {report.evaluation.strengths.map((strength, idx) => (
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
                {report.evaluation.weaknesses.map((weakness, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <AlertCircle size={20} className="text-orange-600 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{weakness}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Improvements (if comparing) */}
            {report.evaluation.improvements_made && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-xl font-bold text-blue-800 mb-4 flex items-center gap-2">
                  <TrendingUp className="text-blue-600" />
                  Mejoras Realizadas
                </h3>
                <ul className="space-y-2">
                  {report.evaluation.improvements_made.map((improvement, idx) => (
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
                {report.evaluation.recommendations.map((rec, idx) => (
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
                {report.evaluation.summary}
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-4">
              <button
                onClick={resetForm}
                className="flex-1 py-4 bg-white border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-all flex items-center justify-center gap-2"
              >
                <Upload size={20} />
                Evaluar Otro Documento
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WritingEvaluator;
