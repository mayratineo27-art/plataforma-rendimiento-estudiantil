// frontend/src/pages/Reportes.jsx
// Página de lista y descarga de reportes

import React, { useState, useEffect } from 'react';
import reportService from '../modules/modulo4-reportes-personalizados/services/reportService';

const Reportes = () => {
  const [reports, setReports] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('reports'); // 'reports' o 'templates'
  const [generatingNew, setGeneratingNew] = useState(false);

  const userId = 1; // TODO: Obtener del AuthContext

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [reportsData, templatesData] = await Promise.all([
        reportService.getUserReports(userId, 20),
        reportService.getUserTemplates(userId),
      ]);
      
      setReports(reportsData.reports || []);
      setTemplates(templatesData.templates || []);
    } catch (err) {
      console.error('Error cargando datos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!window.confirm('¿Generar un nuevo reporte completo? (Esto puede tomar 30-60 segundos)')) {
      return;
    }

    try {
      setGeneratingNew(true);
      const result = await reportService.generateReport(userId, 'integral', true, true);
      
      if (result.success) {
        alert('¡Reporte generado exitosamente!');
        await loadData(); // Recargar lista
      } else {
        // Si el backend devuelve success: false pero sin error HTTP
        const errorMsg = result.message || result.error || 'Error desconocido';
        alert(`❌ No se pudo generar el reporte:\n\n${errorMsg}`);
      }
    } catch (err) {
      console.error('Error generando reporte:', err);
      const errorMsg = err.response?.data?.message || err.response?.data?.error || err.message || 'Error de conexión';
      alert(`❌ Error al generar reporte:\n\n${errorMsg}`);
    } finally {
      setGeneratingNew(false);
    }
  };

  const handleDownload = (templateId, filename) => {
    const url = reportService.getDownloadUrl(templateId);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const getFileIcon = (type) => {
    const icons = {
      'ppt': '📊',
      'docx': '📄',
      'pdf': '📕',
    };
    return icons[type] || '📁';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando reportes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Mis Reportes</h1>
            <button
              onClick={handleGenerateReport}
              disabled={generatingNew}
              className={`
                px-6 py-3 rounded-lg font-semibold text-white
                transition transform hover:scale-105
                ${generatingNew
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
                }
              `}
            >
              {generatingNew ? '⏳ Generando...' : '➕ Nuevo Reporte'}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('reports')}
                className={`
                  py-4 px-6 font-medium text-sm
                  ${activeTab === 'reports'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                📊 Reportes Completos ({reports.length})
              </button>
              <button
                onClick={() => setActiveTab('templates')}
                className={`
                  py-4 px-6 font-medium text-sm
                  ${activeTab === 'templates'
                    ? 'border-b-2 border-blue-500 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                📁 Archivos Generados ({templates.length})
              </button>
            </nav>
          </div>
        </div>

        {/* Contenido según tab activo */}
        {activeTab === 'reports' ? (
          <div className="space-y-4">
            {reports.length === 0 ? (
              <div className="bg-white rounded-lg shadow p-12 text-center">
                <div className="text-6xl mb-4">📊</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  No hay reportes generados
                </h3>
                <p className="text-gray-500 mb-6">
                  Genera tu primer reporte completo para ver tus estadísticas
                </p>
                <button
                  onClick={handleGenerateReport}
                  disabled={generatingNew}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
                >
                  Generar Primer Reporte
                </button>
              </div>
            ) : (
              reports.map((report) => (
                <ReportCard
                  key={report.id}
                  report={report}
                  onViewFiles={() => {
                    setActiveTab('templates');
                  }}
                  formatDate={formatDate}
                />
              ))
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.length === 0 ? (
              <div className="col-span-full bg-white rounded-lg shadow p-12 text-center">
                <div className="text-6xl mb-4">📁</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  No hay archivos generados
                </h3>
                <p className="text-gray-500">
                  Los archivos aparecerán aquí cuando generes reportes
                </p>
              </div>
            ) : (
              templates.map((template) => (
                <TemplateCard
                  key={template.id}
                  template={template}
                  onDownload={handleDownload}
                  formatDate={formatDate}
                  formatFileSize={formatFileSize}
                  getFileIcon={getFileIcon}
                />
              ))
            )}
          </div>
        )}
      </main>
    </div>
  );
};

// Componente de Tarjeta de Reporte
const ReportCard = ({ report, onViewFiles, formatDate }) => {
  const statusColors = {
    'completed': 'bg-green-100 text-green-800',
    'generating': 'bg-yellow-100 text-yellow-800',
    'failed': 'bg-red-100 text-red-800',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            {report.title}
          </h3>
          <p className="text-sm text-gray-500">{formatDate(report.created_at)}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${statusColors[report.generation_status]}`}>
          {report.generation_status === 'completed' ? '✓ Completado' :
           report.generation_status === 'generating' ? '⏳ Generando' : '✗ Error'}
        </span>
      </div>

      {report.description && (
        <p className="text-gray-600 text-sm mb-4">{report.description}</p>
      )}

      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <span className="text-sm font-medium text-gray-700">
          Tipo: {report.report_type}
        </span>
        <button
          onClick={onViewFiles}
          className="text-blue-600 hover:text-blue-700 font-medium text-sm"
        >
          Ver Archivos →
        </button>
      </div>
    </div>
  );
};

// Componente de Tarjeta de Plantilla/Archivo
const TemplateCard = ({ template, onDownload, formatDate, formatFileSize, getFileIcon }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
      <div className="text-center mb-4">
        <div className="text-5xl mb-2">{getFileIcon(template.template_type)}</div>
        <h3 className="font-semibold text-gray-800 truncate" title={template.file_name}>
          {template.file_name}
        </h3>
      </div>

      <div className="space-y-2 text-sm text-gray-600 mb-4">
        <div className="flex justify-between">
          <span>Tipo:</span>
          <span className="font-medium uppercase">{template.template_type}</span>
        </div>
        <div className="flex justify-between">
          <span>Tamaño:</span>
          <span className="font-medium">{formatFileSize(template.file_size)}</span>
        </div>
        <div className="flex justify-between">
          <span>Generado:</span>
          <span className="font-medium text-xs">{formatDate(template.created_at)}</span>
        </div>
      </div>

      <button
        onClick={() => onDownload(template.id, template.file_name)}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-medium"
      >
        ⬇️ Descargar
      </button>
    </div>
  );
};

export default Reportes;