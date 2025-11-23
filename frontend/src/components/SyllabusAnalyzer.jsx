import React, { useState } from 'react';
import { FileText, Loader2, Download, AlertCircle, CheckCircle, BookOpen, TrendingUp, Clock, Link as LinkIcon } from 'lucide-react';

/**
 * SyllabusAnalyzer - Analiza syllabi con IA y permite exportar a PDF
 */
const SyllabusAnalyzer = () => {
  const [syllabusText, setSyllabusText] = useState('');
  const [courseName, setCourseName] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [exportingPdf, setExportingPdf] = useState(false);

  const analyzeSyllabus = async () => {
    if (!syllabusText.trim()) {
      setError('Por favor ingresa el contenido del syllabus');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await fetch('/api/academic/tools/analyze-syllabus', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: syllabusText,
          course_name: courseName
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error al analizar syllabus');
      }

      setAnalysis(data.analysis);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const exportToPdf = async () => {
    if (!analysis) return;

    setExportingPdf(true);
    try {
      const response = await fetch('/api/academic/export-syllabus-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          analysis: analysis,
          course_name: courseName || 'Análisis de Syllabus'
        })
      });

      if (!response.ok) {
        throw new Error('Error al generar PDF');
      }

      // Descargar el PDF
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `analisis_syllabus_${courseName.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Error al exportar PDF: ' + err.message);
    } finally {
      setExportingPdf(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'baja':
        return 'bg-green-100 text-green-800';
      case 'media':
        return 'bg-yellow-100 text-yellow-800';
      case 'alta':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <FileText className="w-6 h-6 text-purple-600" />
        Analizador de Syllabus Mejorado
      </h2>

      {/* Formulario */}
      <div className="space-y-4 mb-8">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Nombre del Curso (Opcional)
          </label>
          <input
            type="text"
            value={courseName}
            onChange={(e) => setCourseName(e.target.value)}
            placeholder="Ej: Inteligencia Artificial"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Contenido del Syllabus
          </label>
          <textarea
            value={syllabusText}
            onChange={(e) => setSyllabusText(e.target.value)}
            placeholder="Pega aquí el contenido completo del syllabus del curso..."
            rows={8}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent font-mono text-sm"
          />
        </div>

        <div className="flex gap-3">
          <button
            onClick={analyzeSyllabus}
            disabled={loading}
            className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analizando...
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                Analizar Syllabus
              </>
            )}
          </button>

          {analysis && (
            <button
              onClick={exportToPdf}
              disabled={exportingPdf}
              className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center gap-2"
            >
              {exportingPdf ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Download className="w-5 h-5" />
              )}
              PDF
            </button>
          )}
        </div>
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

      {/* Analysis Results */}
      {analysis && !analysis.error && (
        <div className="space-y-6">
          {/* Información del Curso */}
          {analysis.course_info && (
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                {analysis.course_info.name || courseName || 'Información del Curso'}
              </h3>
              
              {analysis.course_info.description && (
                <p className="text-gray-700 mb-4">{analysis.course_info.description}</p>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                {analysis.course_info.credits && (
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-purple-600" />
                    <span className="font-medium">Créditos:</span>
                    <span>{analysis.course_info.credits}</span>
                  </div>
                )}
                
                {analysis.estimated_weekly_hours && (
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-purple-600" />
                    <span className="font-medium">Horas semanales:</span>
                    <span>{analysis.estimated_weekly_hours}</span>
                  </div>
                )}
              </div>

              {analysis.course_info.prerequisites && analysis.course_info.prerequisites.length > 0 && (
                <div className="mt-4 pt-4 border-t border-purple-200">
                  <p className="font-medium text-sm text-gray-700 mb-2">Prerequisitos:</p>
                  <div className="flex flex-wrap gap-2">
                    {analysis.course_info.prerequisites.map((prereq, idx) => (
                      <span key={idx} className="bg-purple-100 text-purple-800 text-xs px-3 py-1 rounded-full">
                        {prereq}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Topics */}
          {analysis.topics && analysis.topics.length > 0 && (
            <div>
              <h4 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-purple-600" />
                Temas del Curso ({analysis.topics.length})
              </h4>
              
              <div className="grid gap-4">
                {analysis.topics.map((topic, index) => (
                  <div key={topic.id || index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-grow">
                        <h5 className="font-semibold text-gray-800">{topic.name}</h5>
                        {topic.week && (
                          <p className="text-sm text-purple-600 mt-1">{topic.week}</p>
                        )}
                      </div>
                      {topic.difficulty && (
                        <span className={`text-xs px-3 py-1 rounded-full font-medium ${getDifficultyColor(topic.difficulty)}`}>
                          {topic.difficulty}
                        </span>
                      )}
                    </div>

                    {topic.description && (
                      <p className="text-sm text-gray-600 mb-3">{topic.description}</p>
                    )}

                    {topic.subtopics && topic.subtopics.length > 0 && (
                      <div className="space-y-1">
                        <p className="text-xs font-medium text-gray-500 uppercase">Subtemas:</p>
                        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {topic.subtopics.map((subtopic, idx) => (
                            <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                              <CheckCircle className="w-3 h-3 text-green-500 flex-shrink-0 mt-1" />
                              <span>{subtopic}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Learning Path */}
          {analysis.learning_path && (
            <div className="bg-blue-50 border-l-4 border-blue-400 p-5 rounded-r-lg">
              <h4 className="text-sm font-bold text-blue-900 mb-4 uppercase tracking-wide">
                🎯 Ruta de Aprendizaje Sugerida
              </h4>
              
              <div className="space-y-4">
                {analysis.learning_path.foundational_topics && analysis.learning_path.foundational_topics.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-blue-700 mb-2">📚 Fundamentos:</p>
                    <div className="flex flex-wrap gap-2">
                      {analysis.learning_path.foundational_topics.map((topic, idx) => (
                        <span key={idx} className="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full">
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {analysis.learning_path.intermediate_topics && analysis.learning_path.intermediate_topics.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-blue-700 mb-2">📖 Intermedio:</p>
                    <div className="flex flex-wrap gap-2">
                      {analysis.learning_path.intermediate_topics.map((topic, idx) => (
                        <span key={idx} className="bg-blue-200 text-blue-900 text-xs px-3 py-1 rounded-full">
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {analysis.learning_path.advanced_topics && analysis.learning_path.advanced_topics.length > 0 && (
                  <div>
                    <p className="text-xs font-medium text-blue-700 mb-2">🎓 Avanzado:</p>
                    <div className="flex flex-wrap gap-2">
                      {analysis.learning_path.advanced_topics.map((topic, idx) => (
                        <span key={idx} className="bg-blue-300 text-blue-900 text-xs px-3 py-1 rounded-full">
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Dependencies Map */}
          {analysis.dependencies_map && analysis.dependencies_map.length > 0 && (
            <div>
              <h4 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <LinkIcon className="w-5 h-5 text-purple-600" />
                Mapa de Dependencias
              </h4>
              
              <div className="space-y-3">
                {analysis.dependencies_map.map((dep, idx) => (
                  <div key={idx} className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <p className="font-semibold text-gray-800 mb-2">{dep.topic}</p>
                    <p className="text-sm text-gray-600 mb-2">
                      <span className="font-medium">Requiere:</span> {dep.requires.join(', ')}
                    </p>
                    {dep.reason && (
                      <p className="text-xs text-gray-500 italic">{dep.reason}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recomendaciones */}
          {analysis.study_recommendations && analysis.study_recommendations.length > 0 && (
            <div className="bg-green-50 border-l-4 border-green-400 p-5 rounded-r-lg">
              <h4 className="text-sm font-bold text-green-900 mb-3 uppercase tracking-wide">
                💡 Recomendaciones de Estudio
              </h4>
              <ul className="space-y-2">
                {analysis.study_recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm text-green-800">
                    <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Error de IA */}
      {analysis && analysis.error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-3" />
          <p className="text-red-800 font-medium">No se pudo analizar el syllabus</p>
          <p className="text-sm text-red-600 mt-2">{analysis.message}</p>
        </div>
      )}
    </div>
  );
};

export default SyllabusAnalyzer;
