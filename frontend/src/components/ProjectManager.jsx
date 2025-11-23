import React, { useState, useEffect } from 'react';
import { FolderOpen, Plus, Play, Square, Trash2, Edit2, Clock, Save, X, Loader2, AlertCircle } from 'lucide-react';

/**
 * ProjectManager - Gestiona la jerarquía Curso → Proyectos → Sesiones de Tiempo
 */
const ProjectManager = ({ userId = 1, courses = [] }) => {
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [projects, setProjects] = useState([]);
  const [sessions, setSessions] = useState({});
  const [activeSession, setActiveSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Estado del formulario de nuevo proyecto
  const [showNewProjectForm, setShowNewProjectForm] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    priority: 'media',
    status: 'pendiente'
  });

  // Timer state
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [timerInterval, setTimerInterval] = useState(null);

  // Cargar proyectos cuando se selecciona un curso
  useEffect(() => {
    if (selectedCourse) {
      loadProjects(selectedCourse.id);
    }
  }, [selectedCourse]);

  // Timer effect
  useEffect(() => {
    if (activeSession) {
      const interval = setInterval(() => {
        setTimerSeconds(prev => prev + 1);
      }, 1000);
      setTimerInterval(interval);
      return () => clearInterval(interval);
    } else {
      if (timerInterval) {
        clearInterval(timerInterval);
        setTimerInterval(null);
      }
    }
  }, [activeSession]);

  const loadProjects = async (courseId) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/projects/course/${courseId}`);
      const data = await response.json();
      
      if (response.ok) {
        setProjects(data.projects || []);
        setError(null);
      } else {
        throw new Error(data.error || 'Error al cargar proyectos');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadSessions = async (projectId) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/sessions`);
      const data = await response.json();
      
      if (response.ok) {
        setSessions(prev => ({
          ...prev,
          [projectId]: data.sessions || []
        }));
      }
    } catch (err) {
      console.error('Error loading sessions:', err);
    }
  };

  const createProject = async () => {
    if (!newProject.name.trim()) {
      alert('El nombre del proyecto es obligatorio');
      return;
    }

    try {
      const response = await fetch('/api/projects/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...newProject,
          course_id: selectedCourse.id,
          user_id: userId
        })
      });

      const data = await response.json();

      if (response.ok) {
        setProjects([...projects, data.project]);
        setShowNewProjectForm(false);
        setNewProject({ name: '', description: '', priority: 'media', status: 'pendiente' });
      } else {
        alert(data.error || 'Error al crear proyecto');
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const startSession = async (projectId) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/session/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId })
      });

      const data = await response.json();

      if (response.ok) {
        setActiveSession({ project_id: projectId, session_id: data.session.id });
        setTimerSeconds(0);
      } else {
        alert(data.error || 'Error al iniciar sesión');
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const stopSession = async (projectId) => {
    if (!activeSession) return;

    const notes = prompt('¿Qué trabajaste en esta sesión? (Opcional)');

    try {
      const response = await fetch(`/api/projects/${projectId}/session/stop`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          duration_seconds: timerSeconds,
          notes: notes || ''
        })
      });

      const data = await response.json();

      if (response.ok) {
        setActiveSession(null);
        setTimerSeconds(0);
        loadProjects(selectedCourse.id); // Recargar para actualizar tiempos
        loadSessions(projectId);
      } else {
        alert(data.error || 'Error al detener sesión');
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const deleteProject = async (projectId) => {
    if (!window.confirm('¿Eliminar este proyecto y todas sus sesiones?')) return;

    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setProjects(projects.filter(p => p.id !== projectId));
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critica': return 'bg-red-100 text-red-800 border-red-300';
      case 'alta': return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'media': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'baja': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completado': return 'bg-green-500';
      case 'en_progreso': return 'bg-blue-500';
      case 'pendiente': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <FolderOpen className="w-6 h-6 text-blue-600" />
        Gestor de Proyectos y Tiempo
      </h2>

      {/* Selector de Curso */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Selecciona un Curso
        </label>
        <select
          value={selectedCourse?.id || ''}
          onChange={(e) => {
            const course = courses.find(c => c.id === parseInt(e.target.value));
            setSelectedCourse(course);
          }}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">-- Selecciona un curso --</option>
          {courses.map(course => (
            <option key={course.id} value={course.id}>
              {course.name}
            </option>
          ))}
        </select>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {selectedCourse && (
        <>
          {/* Botón Nuevo Proyecto */}
          <div className="mb-6">
            {!showNewProjectForm ? (
              <button
                onClick={() => setShowNewProjectForm(true)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
              >
                <Plus className="w-5 h-5" />
                Nuevo Proyecto
              </button>
            ) : (
              <div className="border border-gray-300 rounded-lg p-4 space-y-3">
                <input
                  type="text"
                  placeholder="Nombre del proyecto"
                  value={newProject.name}
                  onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <textarea
                  placeholder="Descripción (opcional)"
                  value={newProject.description}
                  onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                
                <div className="grid grid-cols-2 gap-3">
                  <select
                    value={newProject.priority}
                    onChange={(e) => setNewProject({ ...newProject, priority: e.target.value })}
                    className="px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="baja">Prioridad Baja</option>
                    <option value="media">Prioridad Media</option>
                    <option value="alta">Prioridad Alta</option>
                    <option value="critica">Prioridad Crítica</option>
                  </select>

                  <select
                    value={newProject.status}
                    onChange={(e) => setNewProject({ ...newProject, status: e.target.value })}
                    className="px-3 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="pendiente">Pendiente</option>
                    <option value="en_progreso">En Progreso</option>
                    <option value="completado">Completado</option>
                  </select>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={createProject}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg flex items-center justify-center gap-2"
                  >
                    <Save className="w-4 h-4" />
                    Guardar
                  </button>
                  <button
                    onClick={() => setShowNewProjectForm(false)}
                    className="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-2 rounded-lg flex items-center justify-center gap-2"
                  >
                    <X className="w-4 h-4" />
                    Cancelar
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Lista de Proyectos */}
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
          ) : projects.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <FolderOpen className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p>No hay proyectos en este curso</p>
              <p className="text-sm">Crea uno para comenzar a rastrear tu tiempo</p>
            </div>
          ) : (
            <div className="space-y-4">
              {projects.map(project => {
                const isActive = activeSession?.project_id === project.id;
                
                return (
                  <div key={project.id} className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-grow">
                        <div className="flex items-center gap-3 mb-2">
                          <div className={`w-3 h-3 rounded-full ${getStatusColor(project.status)}`}></div>
                          <h3 className="font-semibold text-gray-800">{project.name}</h3>
                        </div>
                        {project.description && (
                          <p className="text-sm text-gray-600 ml-6">{project.description}</p>
                        )}
                      </div>
                      
                      <span className={`text-xs px-3 py-1 rounded-full border ${getPriorityColor(project.priority)}`}>
                        {project.priority}
                      </span>
                    </div>

                    {/* Tiempo Total */}
                    <div className="bg-gray-50 rounded-lg p-3 mb-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4 text-gray-600" />
                          <span className="text-sm font-medium text-gray-700">Tiempo total:</span>
                        </div>
                        <span className="text-lg font-bold text-blue-600">
                          {formatTime(project.total_time_seconds)}
                        </span>
                      </div>
                      
                      {isActive && (
                        <div className="mt-2 pt-2 border-t border-gray-200">
                          <div className="flex items-center justify-between">
                            <span className="text-xs text-gray-600">Sesión actual:</span>
                            <span className="text-sm font-mono text-green-600">
                              {formatTime(timerSeconds)}
                            </span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Acciones */}
                    <div className="flex gap-2">
                      {!isActive ? (
                        <button
                          onClick={() => startSession(project.id)}
                          disabled={activeSession !== null}
                          className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white py-2 rounded-lg flex items-center justify-center gap-2 text-sm"
                        >
                          <Play className="w-4 h-4" />
                          Iniciar Sesión
                        </button>
                      ) : (
                        <button
                          onClick={() => stopSession(project.id)}
                          className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded-lg flex items-center justify-center gap-2 text-sm"
                        >
                          <Square className="w-4 h-4" />
                          Detener
                        </button>
                      )}

                      <button
                        onClick={() => loadSessions(project.id)}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 px-4 rounded-lg text-sm"
                      >
                        Ver Sesiones ({project.sessions_count || 0})
                      </button>

                      <button
                        onClick={() => deleteProject(project.id)}
                        disabled={isActive}
                        className="bg-red-100 hover:bg-red-200 disabled:bg-gray-100 text-red-600 p-2 rounded-lg"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>

                    {/* Sesiones (si están cargadas) */}
                    {sessions[project.id] && sessions[project.id].length > 0 && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-xs font-medium text-gray-500 uppercase mb-2">
                          Historial de Sesiones
                        </p>
                        <div className="space-y-2 max-h-40 overflow-y-auto">
                          {sessions[project.id].map(session => (
                            <div key={session.id} className="bg-gray-50 rounded p-2 text-xs">
                              <div className="flex justify-between items-center">
                                <span className="font-mono font-bold text-blue-600">
                                  {session.duration_formatted}
                                </span>
                                <span className="text-gray-500">
                                  {new Date(session.created_at).toLocaleDateString()}
                                </span>
                              </div>
                              {session.notes && (
                                <p className="text-gray-600 mt-1">{session.notes}</p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}

      {!selectedCourse && (
        <div className="text-center py-12 text-gray-400">
          <FolderOpen className="w-16 h-16 mx-auto mb-4" />
          <p>Selecciona un curso para ver sus proyectos</p>
        </div>
      )}
    </div>
  );
};

export default ProjectManager;
