// frontend/src/pages/Register.jsx
// Página de registro de nuevos usuarios

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    career: '',
    semester: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validaciones
    if (!formData.name || !formData.email || !formData.password) {
      setError('Por favor completa todos los campos obligatorios');
      setLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      setLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      setLoading(false);
      return;
    }

    try {
      // TODO: Implementar llamada real al backend
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Registro exitoso
      alert('¡Cuenta creada exitosamente! Inicia sesión para continuar.');
      navigate('/login');
    } catch (err) {
      setError('Error al crear la cuenta. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-4">
      <div className="w-full max-w-2xl">
        {/* Logo y título */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-lg shadow-indigo-500/50 mb-4">
            <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">
            Crear Cuenta
          </h1>
          <p className="text-indigo-300">
            Únete a la plataforma de rendimiento estudiantil
          </p>
        </div>

        {/* Formulario */}
        <div className="bg-slate-800/90 backdrop-blur-md rounded-2xl border border-indigo-500/30 shadow-2xl p-8">
          {error && (
            <div className="mb-6 bg-red-500/10 border border-red-500/30 rounded-lg p-3">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Nombre completo */}
              <div className="md:col-span-2">
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Nombre Completo *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                  placeholder="Juan Pérez"
                  required
                />
              </div>

              {/* Email */}
              <div className="md:col-span-2">
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Correo Electrónico *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                  placeholder="juan@ejemplo.com"
                  required
                />
              </div>

              {/* Contraseña */}
              <div>
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Contraseña *
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                  placeholder="Mínimo 6 caracteres"
                  required
                />
              </div>

              {/* Confirmar contraseña */}
              <div>
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Confirmar Contraseña *
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                  placeholder="Repite la contraseña"
                  required
                />
              </div>

              {/* Carrera */}
              <div>
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Carrera
                </label>
                <select
                  name="career"
                  value={formData.career}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                >
                  <option value="">Selecciona...</option>
                  <option value="ingenieria-sistemas">Ingeniería de Sistemas</option>
                  <option value="ingenieria-industrial">Ingeniería Industrial</option>
                  <option value="medicina">Medicina</option>
                  <option value="derecho">Derecho</option>
                  <option value="administracion">Administración</option>
                  <option value="otra">Otra</option>
                </select>
              </div>

              {/* Semestre */}
              <div>
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Ciclo/Semestre
                </label>
                <select
                  name="semester"
                  value={formData.semester}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                >
                  <option value="">Selecciona...</option>
                  {[...Array(10)].map((_, i) => (
                    <option key={i} value={i + 1}>Ciclo {i + 1}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Términos y condiciones */}
            <div className="flex items-start">
              <input
                type="checkbox"
                required
                className="w-4 h-4 mt-1 text-indigo-600 bg-slate-700 border-slate-600 rounded focus:ring-indigo-500"
              />
              <label className="ml-3 text-sm text-slate-300">
                Acepto los{' '}
                <Link to="/terms" className="text-indigo-400 hover:text-indigo-300">
                  términos y condiciones
                </Link>{' '}
                y la{' '}
                <Link to="/privacy" className="text-indigo-400 hover:text-indigo-300">
                  política de privacidad
                </Link>
              </label>
            </div>

            {/* Botón */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:from-indigo-700 hover:to-purple-700 transition shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creando cuenta...
                </span>
              ) : (
                'Crear Cuenta'
              )}
            </button>
          </form>

          {/* Ya tienes cuenta */}
          <div className="mt-6 text-center">
            <p className="text-slate-400 text-sm">
              ¿Ya tienes una cuenta?{' '}
              <Link to="/login" className="text-indigo-400 hover:text-indigo-300 font-semibold transition">
                Inicia sesión aquí
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-slate-500 text-xs mt-8">
          © 2025 Plataforma de Rendimiento Estudiantil. Todos los derechos reservados.
        </p>
      </div>
    </div>
  );
};

export default Register;