// frontend/src/pages/PerfilEstudiante.jsx
// Página de perfil detallado del estudiante con visualizaciones

import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, RadialLinearScale, PointElement, LineElement, Filler } from 'chart.js';
import { Doughnut, Radar } from 'react-chartjs-2';
import profileService from '../modules/modulo3-perfil-integral/services/profileService';
import reportService from '../modules/modulo4-reportes-personalizados/services/reportService';

// Registrar componentes de Chart.js
ChartJS.register(ArcElement, Tooltip, Legend, RadialLinearScale, PointElement, LineElement, Filler);

const PerfilEstudiante = () => {
  const [profile, setProfile] = useState(null);
  const [visualizations, setVisualizations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState('overview');

  const userId = 1; // TODO: Obtener del AuthContext

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [profileData, vizData] = await Promise.all([
        profileService.getProfile(userId),
        reportService.getVisualizationData(userId),
      ]);
      
      setProfile(profileData);
      setVisualizations(vizData);
    } catch (err) {
      console.error('Error cargando datos:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando perfil...</p>
        </div>
      </div>
    );
  }

  const stats = visualizations?.charts?.summary_stats || {};

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header Mejorado */}
      <header className="relative overflow-hidden bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 text-white shadow-2xl">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center md:items-start space-y-6 md:space-y-0 md:space-x-8">
            {/* Avatar con efecto glassmorphism */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-yellow-400 to-pink-500 rounded-full blur-xl opacity-50 animate-pulse"></div>
              <div className="relative w-32 h-32 bg-gradient-to-br from-white to-blue-100 rounded-full flex items-center justify-center text-6xl shadow-2xl ring-4 ring-white/50 backdrop-blur-sm">
                👤
              </div>
              <div className="absolute bottom-0 right-0 w-10 h-10 bg-green-500 rounded-full border-4 border-white flex items-center justify-center shadow-lg">
                <span className="text-white text-xl">✓</span>
              </div>
            </div>
            
            {/* Información del perfil */}
            <div className="flex-1 text-center md:text-left">
              <div className="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-md rounded-full px-4 py-1 mb-3">
                <span className="text-xs font-semibold uppercase tracking-wider">Perfil Activo</span>
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              </div>
              
              <h1 className="text-4xl md:text-5xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-white to-blue-100">
                Juan Perez
              </h1>
              
              <p className="text-xl text-blue-100 font-medium mb-3">Estudiante de Ingeniería</p>
              
              <div className="flex flex-wrap gap-3 justify-center md:justify-start">
                <div className="flex items-center space-x-2 bg-white/20 backdrop-blur-md rounded-lg px-4 py-2">
                  <span className="text-2xl">🎓</span>
                  <span className="text-sm font-medium">
                    {profile?.learning_style || 'Analizando estilo...'}
                  </span>
                </div>
                
                <div className="flex items-center space-x-2 bg-white/20 backdrop-blur-md rounded-lg px-4 py-2">
                  <span className="text-2xl">📊</span>
                  <span className="text-sm font-medium">Nivel Intermedio</span>
                </div>
                
                <div className="flex items-center space-x-2 bg-white/20 backdrop-blur-md rounded-lg px-4 py-2">
                  <span className="text-2xl">🔥</span>
                  <span className="text-sm font-medium">Racha de 7 días</span>
                </div>
              </div>
            </div>
            
            {/* Botón de acción */}
            <div className="flex flex-col space-y-3">
              <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition transform hover:scale-105 shadow-xl">
                ✏️ Editar Perfil
              </button>
              <button className="bg-white/20 backdrop-blur-md text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/30 transition">
                📄 Ver Reportes
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Tabs de Secciones Mejorados */}
        <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl mb-8 overflow-hidden border border-white/20">
          <div className="border-b border-gray-200/50">
            <nav className="flex -mb-px">
              <SectionTab
                active={activeSection === 'overview'}
                onClick={() => setActiveSection('overview')}
                icon="📊"
                label="Resumen"
              />
              <SectionTab
                active={activeSection === 'charts'}
                onClick={() => setActiveSection('charts')}
                icon="📈"
                label="Gráficos"
              />
              <SectionTab
                active={activeSection === 'detailed'}
                onClick={() => setActiveSection('detailed')}
                icon="📋"
                label="Detallado"
              />
            </nav>
          </div>
        </div>

        {/* Contenido según sección activa */}
        {activeSection === 'overview' && (
          <OverviewSection profile={profile} stats={stats} />
        )}

        {activeSection === 'charts' && (
          <ChartsSection visualizations={visualizations} />
        )}

        {activeSection === 'detailed' && (
          <DetailedSection profile={profile} />
        )}
      </main>
    </div>
  );
};

// Componente Tab Mejorado
const SectionTab = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={`
      relative py-4 px-8 font-semibold text-sm flex items-center space-x-3 transition-all duration-300
      ${active
        ? 'text-blue-600'
        : 'text-gray-500 hover:text-gray-700'
      }
    `}
  >
    <span className="text-xl">{icon}</span>
    <span>{label}</span>
    {active && (
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-t-full"></div>
    )}
  </button>
);

// Sección Overview
const OverviewSection = ({ profile, stats }) => (
  <div className="space-y-6">
    {/* Stats Cards */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        title="Documentos"
        value={stats.total_documents || 10}
        icon="📄"
        color="blue"
      />
      <StatCard
        title="Sesiones"
        value={stats.total_sessions || 4}
        icon="🎥"
        color="green"
      />
      <StatCard
        title="Escritura"
        value={`${stats.writing_quality?.toFixed(0) || 0}/100`}
        icon="✍️"
        color="purple"
      />
      <StatCard
        title="Vocabulario"
        value={`${stats.vocabulary_score?.toFixed(0) || 0}/100`}
        icon="📚"
        color="orange"
      />
    </div>

    {/* Resumen IA Mejorado */}
    {profile?.summary && (
      <div className="relative bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-600 rounded-2xl shadow-2xl p-8 overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>
        
        <div className="relative">
          <div className="flex items-center space-x-3 mb-5">
            <div className="bg-white/20 backdrop-blur-md rounded-xl p-3">
              <span className="text-4xl">🤖</span>
            </div>
            <h2 className="text-2xl font-bold text-white">Análisis Inteligente con IA</h2>
          </div>
          
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
            <p className="text-white/90 text-lg leading-relaxed whitespace-pre-line">
              {profile.summary}
            </p>
          </div>
          
          <div className="mt-4 flex items-center space-x-2 text-white/80 text-sm">
            <span>⚡</span>
            <span>Generado con Gemini 2.5 Flash</span>
          </div>
        </div>
      </div>
    )}

    {/* Fortalezas y Debilidades en grid */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <ListCard
        title="💪 Fortalezas"
        items={profile?.strengths || []}
        color="green"
      />
      <ListCard
        title="🎯 Áreas de Mejora"
        items={profile?.weaknesses || []}
        color="orange"
      />
    </div>

    {/* Recomendaciones Mejoradas */}
    {profile?.recommendations && profile.recommendations.length > 0 && (
      <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-6">
          <div className="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-xl p-3 shadow-lg">
            <span className="text-3xl">💡</span>
          </div>
          <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Recomendaciones Personalizadas
          </h3>
        </div>
        
        <ol className="space-y-4">
          {profile.recommendations.map((rec, index) => (
            <li key={index} className="group flex items-start bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-4 hover:shadow-md transition-all duration-300">
              <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 text-white rounded-xl flex items-center justify-center text-lg font-bold mr-4 shadow-lg group-hover:scale-110 transition-transform">
                {index + 1}
              </div>
              <span className="text-gray-700 leading-relaxed pt-2">{rec}</span>
            </li>
          ))}
        </ol>
      </div>
    )}
  </div>
);

// Sección de Gráficos
const ChartsSection = ({ visualizations }) => {
  if (!visualizations?.success) {
    return (
      <div className="bg-white rounded-lg shadow p-12 text-center">
        <p className="text-gray-500">No hay datos de visualización disponibles</p>
      </div>
    );
  }

  const charts = visualizations.charts || {};

  // Preparar datos para Radar (Thesis Readiness)
  const radarData = {
    labels: charts.thesis_readiness?.labels || [],
    datasets: charts.thesis_readiness?.datasets || [],
  };

  // Preparar datos para Doughnut (Attention Distribution)
  const doughnutData = {
    labels: charts.attention_distribution?.labels || [],
    datasets: charts.attention_distribution?.datasets || [],
  };

  return (
    <div className="space-y-6">
      {/* Gráfico de Preparación para Tesis (Radar) */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-6">
          Preparación para Tesis
        </h3>
        <div className="max-w-md mx-auto">
          <Radar 
            data={radarData}
            options={{
              scales: {
                r: {
                  beginAtZero: true,
                  max: 100,
                },
              },
            }}
          />
        </div>
      </div>

      {/* Gráfico de Distribución de Atención (Doughnut) */}
      {charts.attention_distribution && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-6">
            Distribución de Niveles de Atención
          </h3>
          <div className="max-w-md mx-auto">
            <Doughnut data={doughnutData} />
          </div>
        </div>
      )}

      {/* Métricas Resumidas */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-6">
          Métricas Resumidas
        </h3>
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(charts.summary_stats || {}).map(([key, value]) => (
            <div key={key} className="bg-gray-50 p-4 rounded-lg">
              <dt className="text-sm text-gray-600 capitalize">
                {key.replace(/_/g, ' ')}
              </dt>
              <dd className="text-2xl font-bold text-gray-900">
                {typeof value === 'number' ? value.toFixed(1) : value}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  );
};


// Sección Detallada
const DetailedSection = ({ profile }) => {
  const [expandedSections, setExpandedSections] = useState({
    basic: true,
    strengths: false,
    weaknesses: false,
    recommendations: false,
    metrics: false,
    raw: false,
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const profileData = profile?.profile || {};

  return (
    <div className="space-y-4">
      {/* Información Básica */}
      <CollapsibleSection
        title="📋 Información Básica"
        isExpanded={expandedSections.basic}
        onToggle={() => toggleSection('basic')}
      >
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow label="ID de Perfil" value={profileData.id} />
          <DetailRow label="Usuario ID" value={profileData.user_id} />
          <DetailRow label="Estilo de Aprendizaje" value={profileData.learning_style || 'No determinado'} />
          <DetailRow label="Nivel General" value={profileData.overall_performance_level} />
          <DetailRow label="Documentos Analizados" value={profileData.total_documents_analyzed} />
          <DetailRow label="Sesiones Completadas" value={profileData.total_sessions_completed} />
          <DetailRow label="Span de Atención" value={`${profileData.avg_attention_span_minutes || 0} minutos`} />
          <DetailRow label="Duración Óptima" value={profileData.optimal_session_duration ? `${profileData.optimal_session_duration} min` : 'N/A'} />
          <DetailRow label="Momento Productivo" value={profileData.most_productive_time || 'No determinado'} />
          <DetailRow label="Patrón de Atención" value={profileData.attention_pattern || 'N/A'} />
        </dl>
      </CollapsibleSection>

      {/* Preparación para Tesis */}
      <CollapsibleSection
        title="🎓 Preparación para Tesis"
        isExpanded={expandedSections.metrics}
        onToggle={() => toggleSection('metrics')}
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricBox
              label="Score de Preparación"
              value={`${profileData.thesis_readiness_score || 0}/100`}
              color="blue"
            />
            <MetricBox
              label="Nivel"
              value={profileData.thesis_readiness_level || 'bajo'}
              color="purple"
            />
            <MetricBox
              label="Meses Estimados"
              value={profileData.estimated_preparation_months || 12}
              color="orange"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <MetricBox
              label="Calidad de Escritura"
              value={`${profileData.avg_writing_quality || 0}/100`}
              color="green"
            />
            <MetricBox
              label="Riqueza de Vocabulario"
              value={`${profileData.avg_vocabulary_richness || 0}/100`}
              color="indigo"
            />
            <MetricBox
              label="Tendencia"
              value={profileData.writing_improvement_trend || 'Sin datos'}
              color="gray"
            />
          </div>
        </div>
      </CollapsibleSection>

      {/* Fortalezas */}
      <CollapsibleSection
        title="💪 Fortalezas Detalladas"
        isExpanded={expandedSections.strengths}
        onToggle={() => toggleSection('strengths')}
      >
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-green-700 mb-2">Académicas</h4>
            <List items={profileData.academic_strengths} emptyText="Sin fortalezas académicas identificadas" />
          </div>
          <div>
            <h4 className="font-semibold text-green-700 mb-2">Escritura</h4>
            <List items={profileData.writing_strengths} emptyText="Sin fortalezas de escritura identificadas" />
          </div>
          <div>
            <h4 className="font-semibold text-green-700 mb-2">Técnicas</h4>
            <List items={profileData.technical_strengths} emptyText="Sin fortalezas técnicas identificadas" />
          </div>
        </div>
      </CollapsibleSection>

      {/* Debilidades */}
      <CollapsibleSection
        title="🎯 Áreas de Mejora Detalladas"
        isExpanded={expandedSections.weaknesses}
        onToggle={() => toggleSection('weaknesses')}
      >
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-orange-700 mb-2">Académicas</h4>
            <List items={profileData.academic_weaknesses} emptyText="Sin debilidades académicas identificadas" />
          </div>
          <div>
            <h4 className="font-semibold text-orange-700 mb-2">Escritura</h4>
            <List items={profileData.writing_weaknesses} emptyText="Sin debilidades de escritura identificadas" />
          </div>
          <div>
            <h4 className="font-semibold text-orange-700 mb-2">Áreas de Mejora</h4>
            <List items={profileData.areas_for_improvement} emptyText="Sin áreas críticas identificadas" />
          </div>
        </div>
      </CollapsibleSection>

      {/* Recomendaciones */}
      <CollapsibleSection
        title="💡 Recomendaciones Completas"
        isExpanded={expandedSections.recommendations}
        onToggle={() => toggleSection('recommendations')}
      >
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-purple-700 mb-2">Estrategias de Estudio</h4>
            <List items={profileData.study_recommendations} emptyText="Sin recomendaciones de estudio" numbered />
          </div>
          <div>
            <h4 className="font-semibold text-purple-700 mb-2">Recursos Recomendados</h4>
            <List items={profileData.resource_recommendations} emptyText="Sin recursos recomendados" />
          </div>
        </div>
      </CollapsibleSection>

      {/* JSON Crudo (para debugging) */}
      <CollapsibleSection
        title="🔧 Datos Técnicos (JSON)"
        isExpanded={expandedSections.raw}
        onToggle={() => toggleSection('raw')}
      >
        <div className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-auto max-h-96 text-xs font-mono">
          <pre>{JSON.stringify(profile, null, 2)}</pre>
        </div>
      </CollapsibleSection>
    </div>
  );
};

// Componente Section Colapsable
const CollapsibleSection = ({ title, isExpanded, onToggle, children }) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden">
    <button
      onClick={onToggle}
      className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition"
    >
      <h3 className="text-lg font-bold text-gray-800">{title}</h3>
      <span className="text-2xl text-gray-400">
        {isExpanded ? '−' : '+'}
      </span>
    </button>
    {isExpanded && (
      <div className="px-6 py-4 border-t border-gray-200">
        {children}
      </div>
    )}
  </div>
);

// Componente DetailRow
const DetailRow = ({ label, value }) => (
  <div className="flex flex-col">
    <dt className="text-sm font-medium text-gray-600">{label}</dt>
    <dd className="mt-1 text-base text-gray-900">{value !== null && value !== undefined ? value : 'N/A'}</dd>
  </div>
);

// Componente MetricBox
const MetricBox = ({ label, value, color }) => {
  const colors = {
    blue: 'bg-blue-50 border-blue-200 text-blue-900',
    purple: 'bg-purple-50 border-purple-200 text-purple-900',
    orange: 'bg-orange-50 border-orange-200 text-orange-900',
    green: 'bg-green-50 border-green-200 text-green-900',
    indigo: 'bg-indigo-50 border-indigo-200 text-indigo-900',
    gray: 'bg-gray-50 border-gray-200 text-gray-900',
  };

  return (
    <div className={`border-2 rounded-lg p-4 ${colors[color]}`}>
      <div className="text-sm font-medium opacity-75">{label}</div>
      <div className="text-2xl font-bold mt-1">{value}</div>
    </div>
  );
};

// Componente List
const List = ({ items, emptyText, numbered = false }) => {
  if (!items || items.length === 0) {
    return <p className="text-gray-500 italic">{emptyText}</p>;
  }

  const ListTag = numbered ? 'ol' : 'ul';
  const listClass = numbered ? 'list-decimal list-inside' : 'list-disc list-inside';

  return (
    <ListTag className={`space-y-1 ${listClass}`}>
      {items.map((item, index) => (
        <li key={index} className="text-gray-700">{item}</li>
      ))}
    </ListTag>
  );
};

// Componente StatCard
const StatCard = ({ title, value, icon, color }) => {
  const colors = {
    blue: {
      gradient: 'from-blue-500 via-blue-600 to-indigo-600',
      bg: 'bg-blue-50',
      text: 'text-blue-600',
      ring: 'ring-blue-200'
    },
    green: {
      gradient: 'from-green-500 via-emerald-600 to-teal-600',
      bg: 'bg-green-50',
      text: 'text-green-600',
      ring: 'ring-green-200'
    },
    purple: {
      gradient: 'from-purple-500 via-violet-600 to-purple-600',
      bg: 'bg-purple-50',
      text: 'text-purple-600',
      ring: 'ring-purple-200'
    },
    orange: {
      gradient: 'from-orange-500 via-amber-600 to-orange-600',
      bg: 'bg-orange-50',
      text: 'text-orange-600',
      ring: 'ring-orange-200'
    },
  };

  const colorScheme = colors[color];

  return (
    <div className="group relative bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-white/20 hover:scale-105">
      <div className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
      
      <div className={`bg-gradient-to-br ${colorScheme.gradient} p-6`}>
        <div className="flex items-start justify-between">
          <div className={`${colorScheme.bg} rounded-xl p-3 ring-4 ${colorScheme.ring} shadow-lg`}>
            <span className="text-4xl">{icon}</span>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-white drop-shadow-lg">{value}</div>
          </div>
        </div>
      </div>
      
      <div className="p-5">
        <h3 className={`text-sm font-bold uppercase tracking-wider ${colorScheme.text}`}>{title}</h3>
      </div>
    </div>
  );
};

// Componente ListCard Mejorado
const ListCard = ({ title, items, color }) => {
  const colorClasses = {
    green: {
      icon: '✓',
      iconBg: 'bg-green-100',
      iconText: 'text-green-600',
      border: 'border-green-200',
      title: 'text-green-700'
    },
    orange: {
      icon: '→',
      iconBg: 'bg-orange-100',
      iconText: 'text-orange-600',
      border: 'border-orange-200',
      title: 'text-orange-700'
    },
  };

  const scheme = colorClasses[color];

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-6 border border-white/20">
      <h3 className={`text-xl font-bold mb-5 ${scheme.title} flex items-center`}>
        {title}
      </h3>
      {items && items.length > 0 ? (
        <ul className="space-y-3">
          {items.map((item, index) => (
            <li key={index} className="flex items-start group">
              <div className={`${scheme.iconBg} ${scheme.iconText} rounded-lg p-2 mr-3 flex-shrink-0 group-hover:scale-110 transition-transform`}>
                <span className="font-bold text-sm">{scheme.icon}</span>
              </div>
              <span className="text-gray-700 leading-relaxed pt-1">{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">📊</div>
          <p className="text-gray-500 italic">Sin información disponible</p>
        </div>
      )}
    </div>
  );
};

export default PerfilEstudiante;