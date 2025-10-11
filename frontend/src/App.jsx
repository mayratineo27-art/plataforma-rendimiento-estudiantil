import React, { useState, useEffect } from 'react';
// import './App.css';  // ← ELIMINA O COMENTA ESTA LÍNEA

function App() {
  const [backendStatus, setBackendStatus] = useState('Verificando...');

  useEffect(() => {
    // Verificar conexión con el backend
    fetch('http://localhost:5000/')
      .then(res => res.json())
      .then(data => {
        setBackendStatus('✅ Conectado');
        console.log('Backend response:', data);
      })
      .catch(err => {
        setBackendStatus('❌ No conectado');
        console.error('Error conectando al backend:', err);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-2xl w-full">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-blue-600 mb-4">
            🎓 Plataforma Integral de Rendimiento Estudiantil
          </h1>
          
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-700 mb-2">
              <strong>Backend:</strong> {backendStatus}
            </p>
            <p className="text-sm text-gray-500">
              http://localhost:5000
            </p>
          </div>

          <div className="mt-6 text-left">
            <h2 className="text-xl font-semibold text-gray-800 mb-3">
              🚀 Estado del Sistema
            </h2>
            <ul className="space-y-2 text-gray-600">
              <li>✅ Frontend iniciado correctamente</li>
              <li>✅ Backend Flask corriendo</li>
              <li>⏳ Módulos en desarrollo...</li>
            </ul>
          </div>

          <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 font-semibold">
              🎉 ¡Sistema listo para desarrollo!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;