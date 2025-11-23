import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-6">
            Plataforma Integral de<br />
            <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Rendimiento Estudiantil
            </span>
          </h1>
          <p className="text-xl text-slate-300 mb-8 max-w-3xl mx-auto">
            Potencia tu aprendizaje con análisis de IA, seguimiento en tiempo real
            y reportes personalizados para maximizar tu preparación académica
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/login"
              className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:from-indigo-700 hover:to-purple-700 transition shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Iniciar Sesión
            </Link>
            <Link
              to="/register"
              className="px-8 py-4 bg-slate-800/50 border border-indigo-500/30 text-white rounded-lg font-semibold hover:bg-slate-700/50 transition"
            >
              Registrarse Gratis
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          <FeatureCard
            icon="📄"
            title="Nodo Digital"
            description="NLP avanzado para evaluar calidad de escritura y vocabulario"
          />
          <FeatureCard
            icon="🎥"
            title= "Stream Multimedia"
            description="Detección de emociones y transcripción automática con IA"
          />
          <FeatureCard
            icon="👤"
            title="Avatar Personal"
            description="Identifica fortalezas, debilidades y estilo de aprendizaje"
          />
          <FeatureCard
            icon="📊"
            title="Análisis Inteligente"
            description="Genera PPT, DOCX y PDF adaptados a tu perfil"
          />
        </div>
      </div>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }) => (
  <div className="bg-slate-800/50 backdrop-blur-md border border-indigo-500/30 rounded-xl p-6 hover:scale-105 transition">
    <div className="text-5xl mb-4">{icon}</div>
    <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
    <p className="text-slate-400 text-sm">{description}</p>
  </div>
);

export default Home;