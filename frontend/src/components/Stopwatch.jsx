import React, { useState, useEffect } from 'react';
import { Timer, Pause, Play, RotateCcw, Save, Clock } from 'lucide-react';

const Stopwatch = ({ courseId = null, taskId = null, userId = 1 }) => {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [timerId, setTimerId] = useState(null);
  const [savedTime, setSavedTime] = useState(0);

  // Cargar timer existente al montar
  useEffect(() => {
    loadTimer();
  }, [courseId, taskId, userId]);

  // Efecto del cronómetro
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        setTime((prevTime) => prevTime + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const loadTimer = async () => {
    try {
      const params = new URLSearchParams({ user_id: userId });
      if (courseId) params.append('course_id', courseId);
      if (taskId) params.append('task_id', taskId);

      const res = await fetch(`/api/timer/user/${userId}?${params}`);
      const data = await res.json();

      if (data.timers && data.timers.length > 0) {
        const timer = data.timers[0];
        setTimerId(timer.id);
        setTime(timer.total_seconds);
        setSavedTime(timer.total_seconds);
        setIsRunning(timer.is_active);
      }
    } catch (error) {
      console.error('Error cargando timer:', error);
    }
  };

  const handleStartStop = async () => {
    if (isRunning) {
      // Detener
      if (timerId) {
        try {
          await fetch(`/api/timer/stop/${timerId}`, { method: 'PUT' });
          setSavedTime(time);
        } catch (error) {
          console.error('Error deteniendo timer:', error);
        }
      }
      setIsRunning(false);
    } else {
      // Iniciar
      if (!timerId) {
        try {
          const res = await fetch('/api/timer/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              user_id: userId,
              course_id: courseId,
              task_id: taskId,
              session_name: 'Sesión de estudio'
            })
          });
          const data = await res.json();
          setTimerId(data.timer.id);
        } catch (error) {
          console.error('Error iniciando timer:', error);
        }
      }
      setIsRunning(true);
    }
  };

  const handleReset = async () => {
    if (window.confirm('¿Reiniciar el cronómetro? Se perderá el tiempo actual.')) {
      if (timerId) {
        try {
          await fetch(`/api/timer/reset/${timerId}`, { method: 'PUT' });
        } catch (error) {
          console.error('Error reseteando timer:', error);
        }
      }
      setIsRunning(false);
      setTime(0);
      setSavedTime(0);
    }
  };

  const handleSave = async () => {
    if (timerId && isRunning) {
      try {
        await fetch(`/api/timer/stop/${timerId}`, { method: 'PUT' });
        setSavedTime(time);
        setIsRunning(false);
        alert('✅ Tiempo guardado correctamente');
      } catch (error) {
        console.error('Error guardando timer:', error);
      }
    }
  };

  const formatTime = (seconds) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hrs > 0) {
      return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex items-center gap-3 bg-gradient-to-r from-blue-50 to-indigo-50 text-slate-700 px-4 py-2 rounded-lg border border-blue-200 shadow-sm">
      <div className="flex items-center gap-2">
        <Timer size={18} className={`${isRunning ? 'text-blue-600 animate-pulse' : 'text-blue-400'}`} />
        <span className="font-mono font-bold text-lg min-w-[70px] text-center">
          {formatTime(time)}
        </span>
      </div>
      
      <div className="flex gap-1.5 ml-2 border-l border-blue-200 pl-3">
        <button 
          onClick={handleStartStop} 
          className={`p-1.5 rounded transition ${isRunning ? 'hover:bg-red-100 text-red-600' : 'hover:bg-green-100 text-green-600'}`}
          title={isRunning ? 'Pausar' : 'Iniciar'}
        >
          {isRunning ? <Pause size={16} /> : <Play size={16} />}
        </button>
        
        {isRunning && (
          <button 
            onClick={handleSave} 
            className="p-1.5 hover:bg-blue-100 rounded text-blue-600 transition"
            title="Guardar tiempo"
          >
            <Save size={16} />
          </button>
        )}
        
        <button 
          onClick={handleReset} 
          className="p-1.5 hover:bg-red-100 rounded text-red-500 transition"
          title="Reiniciar"
        >
          <RotateCcw size={16} />
        </button>
      </div>
      
      {savedTime > 0 && time !== savedTime && (
        <div className="text-xs text-blue-600 border-l border-blue-200 pl-3">
          <Clock size={12} className="inline mr-1" />
          Guardado: {formatTime(savedTime)}
        </div>
      )}
    </div>
  );
};

export default Stopwatch;