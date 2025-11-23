import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Play, Pause, Square, Clock, Activity } from 'lucide-react';

const SmartTimer = ({ projectId, userId, onTimeUpdate }) => {
  const [session, setSession] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [lastActivity, setLastActivity] = useState(Date.now());
  
  const timerRef = useRef(null);
  const heartbeatRef = useRef(null);
  const activityCheckRef = useRef(null);
  
  const INACTIVITY_THRESHOLD = 60000; // 1 minuto de inactividad
  const HEARTBEAT_INTERVAL = 5000; // Enviar heartbeat cada 5 segundos
  const ACTIVITY_CHECK_INTERVAL = 10000; // Verificar actividad cada 10 segundos

  useEffect(() => {
    // Detectar actividad del usuario
    const handleActivity = () => {
      setLastActivity(Date.now());
    };

    window.addEventListener('mousemove', handleActivity);
    window.addEventListener('keydown', handleActivity);
    window.addEventListener('click', handleActivity);
    window.addEventListener('scroll', handleActivity);

    return () => {
      window.removeEventListener('mousemove', handleActivity);
      window.removeEventListener('keydown', handleActivity);
      window.removeEventListener('click', handleActivity);
      window.removeEventListener('scroll', handleActivity);
    };
  }, []);

  useEffect(() => {
    if (isRunning && session) {
      // Actualizar el cronómetro cada segundo
      timerRef.current = setInterval(() => {
        if (!isPaused) {
          setElapsedTime(prev => prev + 1);
        }
      }, 1000);

      // Enviar heartbeat periódicamente
      heartbeatRef.current = setInterval(() => {
        if (!isPaused) {
          sendHeartbeat();
        }
      }, HEARTBEAT_INTERVAL);

      // Verificar inactividad
      activityCheckRef.current = setInterval(() => {
        checkInactivity();
      }, ACTIVITY_CHECK_INTERVAL);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (heartbeatRef.current) clearInterval(heartbeatRef.current);
      if (activityCheckRef.current) clearInterval(activityCheckRef.current);
    };
  }, [isRunning, isPaused, session, lastActivity]);

  const sendHeartbeat = async () => {
    if (!session) return;
    
    try {
      await axios.post(
        `http://localhost:5000/api/projects/session/${session.id}/heartbeat`
      );
    } catch (error) {
      console.error('Error enviando heartbeat:', error);
    }
  };

  const checkInactivity = async () => {
    const now = Date.now();
    const timeSinceActivity = now - lastActivity;

    if (timeSinceActivity > INACTIVITY_THRESHOLD && !isPaused && session) {
      console.log('Inactividad detectada, pausando sesión...');
      await pauseSession(true); // true = auto-pause
    }
  };

  const startSession = async () => {
    try {
      const response = await axios.post(
        `http://localhost:5000/api/projects/${projectId}/smart-session/start`,
        { user_id: userId }
      );
      
      setSession(response.data.session);
      setIsRunning(true);
      setIsPaused(false);
      setElapsedTime(0);
      setLastActivity(Date.now());
    } catch (error) {
      console.error('Error iniciando sesión:', error);
      alert(error.response?.data?.error || 'Error al iniciar sesión');
    }
  };

  const pauseSession = async (isAutoPause = false) => {
    if (!session) return;

    try {
      await axios.post(
        `http://localhost:5000/api/projects/session/${session.id}/auto-pause`
      );
      
      setIsPaused(true);
      
      if (isAutoPause) {
        // Notificar al usuario
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('Cronómetro pausado', {
            body: 'Se detectó inactividad y el cronómetro fue pausado automáticamente.',
            icon: '/favicon.ico'
          });
        }
      }
    } catch (error) {
      console.error('Error pausando sesión:', error);
    }
  };

  const resumeSession = async () => {
    if (!session) return;

    try {
      await axios.post(
        `http://localhost:5000/api/projects/session/${session.id}/resume`
      );
      
      setIsPaused(false);
      setLastActivity(Date.now());
    } catch (error) {
      console.error('Error reanudando sesión:', error);
    }
  };

  const stopSession = async () => {
    if (!session) return;

    try {
      const response = await axios.post(
        `http://localhost:5000/api/projects/session/${session.id}/smart-stop`
      );
      
      setSession(null);
      setIsRunning(false);
      setIsPaused(false);
      setElapsedTime(0);

      if (onTimeUpdate) {
        onTimeUpdate(response.data.session.duration_seconds);
      }

      alert(`Sesión finalizada. Tiempo total: ${response.data.session.duration_formatted}`);
    } catch (error) {
      console.error('Error deteniendo sesión:', error);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const requestNotificationPermission = () => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  };

  useEffect(() => {
    requestNotificationPermission();
  }, []);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <Clock size={24} />
          Cronómetro Inteligente
        </h3>
        {isRunning && (
          <div className="flex items-center gap-2 text-sm">
            <Activity size={16} className={isPaused ? 'text-yellow-500' : 'text-green-500'} />
            <span className={isPaused ? 'text-yellow-600' : 'text-green-600'}>
              {isPaused ? 'Pausado' : 'Activo'}
            </span>
          </div>
        )}
      </div>

      {/* Display del tiempo */}
      <div className="text-center mb-6">
        <div className={`text-6xl font-mono font-bold ${
          isPaused ? 'text-yellow-600' : isRunning ? 'text-blue-600' : 'text-gray-800'
        }`}>
          {formatTime(elapsedTime)}
        </div>
        {isRunning && (
          <p className="text-sm text-gray-600 mt-2">
            {isPaused
              ? '⏸️ Pausado por inactividad. Mueve el mouse para reanudar.'
              : '▶️ Registrando tiempo automáticamente'}
          </p>
        )}
      </div>

      {/* Controles */}
      <div className="flex gap-3 justify-center">
        {!isRunning ? (
          <button
            onClick={startSession}
            className="flex items-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-semibold transition shadow-md"
          >
            <Play size={20} />
            Iniciar Sesión
          </button>
        ) : (
          <>
            {isPaused ? (
              <button
                onClick={resumeSession}
                className="flex items-center gap-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold transition shadow-md"
              >
                <Play size={20} />
                Reanudar
              </button>
            ) : (
              <button
                onClick={() => pauseSession(false)}
                className="flex items-center gap-2 px-6 py-3 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg font-semibold transition shadow-md"
              >
                <Pause size={20} />
                Pausar
              </button>
            )}
            
            <button
              onClick={stopSession}
              className="flex items-center gap-2 px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg font-semibold transition shadow-md"
            >
              <Square size={20} />
              Detener
            </button>
          </>
        )}
      </div>

      {/* Información adicional */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
          <Activity size={16} />
          Características del Cronómetro Inteligente
        </h4>
        <ul className="text-sm text-gray-700 space-y-1">
          <li>• Detección automática de inactividad (pausa tras 1 minuto sin actividad)</li>
          <li>• Reanudación automática al detectar movimiento del mouse o teclado</li>
          <li>• Notificaciones cuando se pausa por inactividad</li>
          <li>• Sincronización constante con el servidor</li>
        </ul>
      </div>
    </div>
  );
};

export default SmartTimer;
