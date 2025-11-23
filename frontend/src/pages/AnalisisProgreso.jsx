import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const AnalisisProgreso = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const userId = 1; // TODO: Obtener del context

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    try {
      const response = await axios.post(
        `${API_URL}/api/analysis/upload`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setResult(response.data);
      alert('¡Documento analizado exitosamente!');
    } catch (error) {
      alert('Error al analizar documento');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          📄 Nodo Operacional del Progreso Académico
        </h1>

        {/* Subir archivo */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-6">
          <h2 className="text-2xl font-bold mb-4">Subir Documento</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="text-6xl mb-4">📄</div>
              <p className="text-gray-600 mb-2">
                {file ? file.name : 'Haz clic para seleccionar un archivo'}
              </p>
              <p className="text-sm text-gray-400">PDF o DOCX hasta 50MB</p>
            </label>
          </div>

          {file && (
            <button
              onClick={handleUpload}
              disabled={loading}
              className="mt-4 w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Analizando...' : 'Analizar Documento'}
            </button>
          )}
        </div>

        {/* Resultados */}
        {result && (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-4">Resultados del Análisis</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600">Calidad de Escritura</div>
                <div className="text-3xl font-bold text-blue-600">
                  {result.writing_quality || 0}/100
                </div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-sm text-gray-600">Vocabulario</div>
                <div className="text-3xl font-bold text-purple-600">
                  {result.vocabulary_score || 0}/100
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalisisProgreso;