import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate, Outlet } from 'react-router-dom'; // 👈 Se añadió Outlet

// Importación de Páginas
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
// import AnalisisProgreso from './pages/AnalisisProgreso'; // Ya no se usa en esta ruta
import SesionTiempoReal from './pages/SesionTiempoReal';
import PerfilEstudiante from './pages/PerfilEstudiante';
import Reportes from './pages/Reportes';
import AcademicDashboard from './pages/AcademicDashboard'; // 👈 Tu nuevo módulo
import FreeTimeline from './components/FreeTimeline'; // 👈 Líneas de tiempo libres
import TopicTimelines from './components/TopicTimelines'; // 👈 Líneas de tiempo por tema de curso

function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas públicas */}
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas protegidas */}
        <Route path="/" element={<ProtectedLayout />}>
          <Route index element={<Dashboard />} />
          
          {/* 🆕 AQUÍ ESTÁ EL CAMBIO: Módulo 1 - Asistente Académico */}
          <Route path="analisis" element={<AcademicDashboard />} />
          
          {/* 🆕 Líneas de Tiempo Libres (SO, tecnologías, etc.) */}
          <Route path="timelines-libre" element={<FreeTimeline />} />
          
          {/* 🆕 Líneas de Tiempo por Tema de Curso */}
          <Route path="timelines-temas" element={<TopicTimelines />} />
          
          <Route path="sesion" element={<SesionTiempoReal />} />
          <Route path="perfil" element={<PerfilEstudiante />} />
          <Route path="reportes" element={<Reportes />} />
        </Route>

        {/* Ruta catch-all (404) redirige a home */}
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </Router>
  );
}

// Layout con navegación
const ProtectedLayout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Aquí podrías añadir lógica para limpiar cookies si fuera necesario
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center cursor-pointer" onClick={() => navigate('/')}>
                <span className="text-2xl font-bold text-blue-600">
                  🎓 Matriz de Progreso
                </span>
              </div>

              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <NavLink to="/">⚛️ Nodo Operacional</NavLink>
                <NavLink to="/analisis">📄 Nodo Digital</NavLink> {/* Ahora lleva a AcademicDashboard */}
                <NavLink to="/timelines-libre">🆓 Timelines Libres</NavLink> {/* Líneas de tiempo para SO, tecnologías */}
                <NavLink to="/timelines-temas">📚 Temas de Cursos</NavLink> {/* Líneas de tiempo por tema */}
                <NavLink to="/sesion">🎥 Stream Multimedia</NavLink>
                <NavLink to="/perfil">👤 Avatar Personal</NavLink>
                <NavLink to="/reportes">📊 Análisis Inteligente</NavLink>
              </div>
            </div>

            <div className="flex items-center">
              <div className="hidden md:block mr-4 text-sm text-gray-500">
                {/* Opcional: Mostrar nombre de usuario si está en localStorage */}
                {JSON.parse(localStorage.getItem('user'))?.username || 'Estudiante'}
              </div>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition flex items-center gap-2"
              >
                🚪 Desconexión 
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Contenido Principal */}
      <main className="py-6">
        {/* 🚨 IMPORTANTE: 
            Usamos <Outlet /> aquí. Esto le dice a React Router:
            "Renderiza aquí el componente hijo que coincida con la ruta definida en App()" 
        */}
        <Outlet />
      </main>
    </div>
  );
};

// Componente NavLink reutilizable para navegación
// Usamos useLocation para resaltar la pestaña activa
import { useLocation } from 'react-router-dom';

const NavLink = ({ to, children, ...props }) => {
  const location = useLocation();
  // Verifica si la ruta actual coincide con el link para activarlo visualmente
  const isActive = location.pathname === to || (to !== '/' && location.pathname.startsWith(to));

  return (
    <Link
      to={to}
      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition ${
        isActive 
          ? 'border-blue-500 text-gray-900' 
          : 'border-transparent text-gray-500 hover:border-blue-300 hover:text-gray-700'
      }`}
      {...props}
    >
      {children}
    </Link>
  );
};

export default App;