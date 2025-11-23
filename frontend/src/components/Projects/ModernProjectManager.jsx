import React, { useState, useEffect } from 'react';
import {
  FolderOpen,
  Plus,
  Play,
  Square,
  Trash2,
  Clock,
  Save,
  X,
  Loader2,
  AlertCircle,
  Sparkles,
  TrendingUp,
  Target,
  Award,
  Zap,
  Coffee,
  Rocket,
  Brain,
  ChevronDown,
  ChevronUp,
  Calendar,
  Edit3
} from 'lucide-react';

const ModernProjectManager = ({ userId = 1, courses = [] }) => {
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [projects, setProjects] = useState([]);
  const [sessions, setSessions] = useState({});
  const [activeSession, setActiveSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Estado del formulario
  const [showNewProjectForm, setShowNewProjectForm] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    priority: 'media',
    status: 'pendiente'
  });

  // Timer y expansión
  const [timerSeconds, setTimerSeconds] = useState(0);
  const [timerInterval, setTimerInterval] = useState(null);
  const [expandedProject, setExpandedProject] = useState(null);

  useEffect(() => {
    if (selectedCourse) {
      loadProjects(selectedCourse.id);
    }
  }, [selectedCourse]);

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
      const response = await fetch(`http://localhost:5000/api/projects/course/${courseId}`);
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
      const response = await fetch(`http://localhost:5000/api/projects/${projectId}/sessions`);
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
      alert('¡Dale un nombre épico a tu proyecto! 🚀');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/projects/', {
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
      const response = await fetch(`http://localhost:5000/api/projects/${projectId}/session/start`, {
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

    const notes = prompt('✨ ¡Increíble sesión! ¿Qué lograste hoy? (Puedes dejarlo vacío si prefieres)');

    try {
      const response = await fetch(`http://localhost:5000/api/projects/${projectId}/session/stop`, {
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
        loadProjects(selectedCourse.id);
        loadSessions(projectId);
      } else {
        alert(data.error || 'Error al detener sesión');
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const deleteProject = async (projectId) => {
    if (!window.confirm('⚠️ ¿Seguro que quieres eliminar este proyecto? Esta acción no se puede deshacer.')) return;

    try {
      const response = await fetch(`http://localhost:5000/api/projects/${projectId}`, {
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

  const getPriorityConfig = (priority) => {
    const configs = {
      critica: {
        color: 'from-red-500 to-rose-500',
        bg: 'bg-red-100',
        text: 'text-red-800',
        border: 'border-red-300',
        icon: <Zap className="w-4 h-4" />,
        label: '🔥 Crítica'
      },
      alta: {
        color: 'from-orange-500 to-amber-500',
        bg: 'bg-orange-100',
        text: 'text-orange-800',
        border: 'border-orange-300',
        icon: <TrendingUp className="w-4 h-4" />,
        label: '⚡ Alta'
      },
      media: {
        color: 'from-yellow-500 to-yellow-600',
        bg: 'bg-yellow-100',
        text: 'text-yellow-800',
        border: 'border-yellow-300',
        icon: <Target className="w-4 h-4" />,
        label: '🎯 Media'
      },
      baja: {
        color: 'from-green-500 to-emerald-500',
        bg: 'bg-green-100',
        text: 'text-green-800',
        border: 'border-green-300',
        icon: <Coffee className="w-4 h-4" />,
        label: '☕ Baja'
      }
    };
    return configs[priority] || configs.media;
  };

  const getStatusConfig = (status) => {
    const configs = {
      completado: {
        color: 'bg-gradient-to-r from-green-500 to-emerald-500',
        icon: <Award className="w-5 h-5" />,
        label: '✅ Completado'
      },
      en_progreso: {
        color: 'bg-gradient-to-r from-blue-500 to-indigo-500',
        icon: <Rocket className="w-5 h-5" />,
        label: '🚀 En Progreso'
      },
      pendiente: {
        color: 'bg-gradient-to-r from-yellow-500 to-orange-500',
        icon: <Brain className="w-5 h-5" />,
        label: '💭 Pendiente'
      }
    };
    return configs[status] || configs.pendiente;
  };

  const getMotivationalMessage = () => {
    const messages = [
      "✨ ¿Listo para conquistar el mundo con tu nuevo proyecto?",
      "🚀 ¡El primer paso hacia el éxito comienza aquí!",
      "💡 Las grandes ideas merecen grandes proyectos",
      "🎯 Organiza tu genialidad en un proyecto increíble",
      "⭐ Convierte tus sueños en proyectos realizables",
      "🌟 Tu próximo logro comienza con un solo click"
    ];
    return messages[Math.floor(Math.random() * messages.length)];
  };

  const getEmptyMessage = () => {
    const messages = [
      { icon: <Sparkles className="w-20 h-20" />, text: "¡Es momento de brillar!", sub: "Crea tu primer proyecto y empieza a rastrear tu progreso" },
      { icon: <Rocket className="w-20 h-20" />, text: "¡Despegando hacia el éxito!", sub: "Agrega un proyecto para comenzar tu aventura" },
      { icon: <Brain className="w-20 h-20" />, text: "¡Tu genio necesita un proyecto!", sub: "Dale vida a tus ideas creando tu primer proyecto" }
    ];
    return messages[Math.floor(Math.random() * messages.length)];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-xl">
                <FolderOpen className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  Gestor de Proyectos
                </h1>
                <p className="text-gray-600 mt-1">Organiza tu tiempo, alcanza tus metas 🎯</p>
              </div>
            </div>
          </div>
        </div>

        {/* Selector de Curso */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <label className="block text-sm font-bold text-gray-700 mb-3 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-purple-600" />
            Selecciona tu Curso
          </label>
          <select
            value={selectedCourse?.id || ''}
            onChange={(e) => {
              const course = courses.find(c => c.id === parseInt(e.target.value));
              setSelectedCourse(course);
            }}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all text-gray-800 font-medium"
          >
            <option value="">🎓 -- Elige un curso para comenzar --</option>
            {courses.map(course => (
              <option key={course.id} value={course.id}>
                📚 {course.name}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <div className="bg-gradient-to-r from-red-50 to-rose-50 border-l-4 border-red-500 p-4 rounded-xl shadow-lg">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-800">¡Ups! Algo salió mal</p>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {selectedCourse && (
          <>
            {/* Botón Nuevo Proyecto */}
            <div>
              {!showNewProjectForm ? (
                <button
                  onClick={() => setShowNewProjectForm(true)}
                  className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold py-4 px-6 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:scale-[1.02] flex items-center justify-center gap-3"
                >
                  <Plus className="w-6 h-6" />
                  {getMotivationalMessage()}
                </button>
              ) : (
                <div className="bg-white border-2 border-purple-300 rounded-2xl p-6 shadow-xl space-y-4">
                  <div className="flex items-center gap-3 mb-4">
                    <Sparkles className="w-6 h-6 text-purple-600" />
                    <h3 className="text-xl font-bold text-gray-800">Crear Nuevo Proyecto</h3>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      ✨ Nombre del Proyecto *
                    </label>
                    <input
                      type="text"
                      placeholder="Ej: Trabajo Final de Matemáticas 🚀"
                      value={newProject.name}
                      onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      📝 Cuéntanos más sobre tu proyecto
                    </label>
                    <textarea
                      placeholder="¿Qué vas a crear? ¡Comparte tus ideas! 💡"
                      value={newProject.description}
                      onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all resize-none"
                    />
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        🎯 Prioridad
                      </label>
                      <select
                        value={newProject.priority}
                        onChange={(e) => setNewProject({ ...newProject, priority: e.target.value })}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 transition-all"
                      >
                        <option value="baja">☕ Baja - Sin apuro</option>
                        <option value="media">🎯 Media - Normal</option>
                        <option value="alta">⚡ Alta - Importante</option>
                        <option value="critica">🔥 Crítica - Urgente</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">
                        📊 Estado
                      </label>
                      <select
                        value={newProject.status}
                        onChange={(e) => setNewProject({ ...newProject, status: e.target.value })}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 transition-all"
                      >
                        <option value="pendiente">💭 Pendiente</option>
                        <option value="en_progreso">🚀 En Progreso</option>
                        <option value="completado">✅ Completado</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      onClick={createProject}
                      className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transition-all"
                    >
                      <Save className="w-5 h-5" />
                      ¡Crear Proyecto!
                    </button>
                    <button
                      onClick={() => {
                        setShowNewProjectForm(false);
                        setNewProject({ name: '', description: '', priority: 'media', status: 'pendiente' });
                      }}
                      className="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg transition-all"
                    >
                      <X className="w-5 h-5" />
                      Cancelar
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Lista de Proyectos */}
            {loading ? (
              <div className="bg-white rounded-2xl shadow-lg p-16">
                <div className="flex flex-col items-center justify-center">
                  <Loader2 className="w-16 h-16 text-purple-600 animate-spin mb-4" />
                  <p className="text-gray-600 font-medium">Cargando tu magia... ✨</p>
                </div>
              </div>
            ) : projects.length === 0 ? (
              <div className="bg-white rounded-2xl shadow-lg p-16 text-center border-2 border-dashed border-purple-300">
                {(() => {
                  const msg = getEmptyMessage();
                  return (
                    <>
                      <div className="text-purple-400 mx-auto mb-6">{msg.icon}</div>
                      <h3 className="text-2xl font-bold text-gray-800 mb-3">{msg.text}</h3>
                      <p className="text-gray-600 mb-6">{msg.sub}</p>
                      <button
                        onClick={() => setShowNewProjectForm(true)}
                        className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl font-bold shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
                      >
                        <Plus className="w-5 h-5" />
                        ¡Empecemos!
                      </button>
                    </>
                  );
                })()}
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-6">
                {projects.map(project => {
                  const isActive = activeSession?.project_id === project.id;
                  const priorityConfig = getPriorityConfig(project.priority);
                  const statusConfig = getStatusConfig(project.status);
                  const isExpanded = expandedProject === project.id;
                  
                  return (
                    <div
                      key={project.id}
                      className={`bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden ${
                        isActive ? 'ring-4 ring-green-400' : ''
                      }`}
                    >
                      {/* Header con gradiente según estado */}
                      <div className={`${statusConfig.color} p-6 text-white`}>
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              {statusConfig.icon}
                              <h3 className="text-2xl font-bold">{project.name}</h3>
                            </div>
                            {project.description && (
                              <p className="text-white/90 text-sm">{project.description}</p>
                            )}
                          </div>
                          
                          <div className="flex items-center gap-2">
                            <span className={`px-4 py-2 rounded-full border-2 border-white/30 backdrop-blur-sm ${priorityConfig.bg} ${priorityConfig.text} font-bold text-sm flex items-center gap-2`}>
                              {priorityConfig.icon}
                              {priorityConfig.label}
                            </span>
                          </div>
                        </div>

                        {/* Tiempo Total */}
                        <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Clock className="w-5 h-5" />
                              <span className="font-bold">Tiempo Total Invertido:</span>
                            </div>
                            <span className="text-3xl font-bold font-mono">
                              {formatTime(project.total_time_seconds)}
                            </span>
                          </div>
                          
                          {isActive && (
                            <div className="mt-3 pt-3 border-t border-white/30">
                              <div className="flex items-center justify-between">
                                <span className="text-sm flex items-center gap-2">
                                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                                  Sesión en progreso:
                                </span>
                                <span className="text-xl font-mono font-bold text-green-200">
                                  {formatTime(timerSeconds)}
                                </span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Acciones */}
                      <div className="p-6 space-y-4">
                        <div className="flex gap-3">
                          {!isActive ? (
                            <button
                              onClick={() => startSession(project.id)}
                              disabled={activeSession !== null}
                              className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 text-white py-3 rounded-xl flex items-center justify-center gap-2 font-bold shadow-lg hover:shadow-xl transition-all transform hover:scale-[1.02] disabled:transform-none"
                            >
                              <Play className="w-5 h-5" />
                              ¡Iniciar Sesión!
                            </button>
                          ) : (
                            <button
                              onClick={() => stopSession(project.id)}
                              className="flex-1 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-700 hover:to-rose-700 text-white py-3 rounded-xl flex items-center justify-center gap-2 font-bold shadow-lg hover:shadow-xl transition-all transform hover:scale-[1.02]"
                            >
                              <Square className="w-5 h-5" />
                              Detener y Guardar
                            </button>
                          )}

                          <button
                            onClick={() => {
                              if (isExpanded) {
                                setExpandedProject(null);
                              } else {
                                setExpandedProject(project.id);
                                loadSessions(project.id);
                              }
                            }}
                            className="bg-purple-100 hover:bg-purple-200 text-purple-700 py-3 px-6 rounded-xl font-bold transition-all flex items-center gap-2"
                          >
                            <Calendar className="w-5 h-5" />
                            Historial ({project.sessions_count || 0})
                            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                          </button>

                          <button
                            onClick={() => deleteProject(project.id)}
                            disabled={isActive}
                            className="bg-red-100 hover:bg-red-200 disabled:bg-gray-100 disabled:text-gray-400 text-red-600 p-3 rounded-xl transition-all"
                            title="Eliminar proyecto"
                          >
                            <Trash2 className="w-5 h-5" />
                          </button>
                        </div>

                        {/* Sesiones (expandibles) */}
                        {isExpanded && sessions[project.id] && (
                          <div className="pt-4 border-t-2 border-gray-200">
                            {sessions[project.id].length === 0 ? (
                              <div className="text-center py-8 text-gray-500">
                                <Clock className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                                <p className="font-medium">Aún no hay sesiones registradas</p>
                                <p className="text-sm">¡Inicia tu primera sesión ahora!</p>
                              </div>
                            ) : (
                              <>
                                <div className="flex items-center gap-2 mb-4">
                                  <Sparkles className="w-5 h-5 text-purple-600" />
                                  <h4 className="font-bold text-gray-800">Registro de Sesiones</h4>
                                </div>
                                <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
                                  {sessions[project.id].map(session => (
                                    <div
                                      key={session.id}
                                      className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-4 border-2 border-purple-200 hover:shadow-md transition-all"
                                    >
                                      <div className="flex justify-between items-center mb-2">
                                        <span className="text-2xl font-mono font-bold text-purple-700">
                                          ⏱️ {session.duration_formatted}
                                        </span>
                                        <span className="text-sm text-gray-600 flex items-center gap-2">
                                          <Calendar className="w-4 h-4" />
                                          {new Date(session.created_at).toLocaleDateString('es-ES', {
                                            weekday: 'short',
                                            year: 'numeric',
                                            month: 'short',
                                            day: 'numeric',
                                            hour: '2-digit',
                                            minute: '2-digit'
                                          })}
                                        </span>
                                      </div>
                                      {session.notes && (
                                        <div className="bg-white/60 rounded-lg p-3 border border-purple-200">
                                          <p className="text-sm text-gray-700 flex items-start gap-2">
                                            <Edit3 className="w-4 h-4 mt-0.5 text-purple-600 flex-shrink-0" />
                                            <span className="italic">{session.notes}</span>
                                          </p>
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              </>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </>
        )}

        {!selectedCourse && (
          <div className="bg-white rounded-2xl shadow-lg p-16 text-center">
            <Sparkles className="w-20 h-20 mx-auto mb-6 text-purple-400" />
            <h3 className="text-2xl font-bold text-gray-800 mb-3">
              ¡Bienvenido a tu espacio de productividad! 🚀
            </h3>
            <p className="text-gray-600">
              Selecciona un curso arriba para comenzar a gestionar tus proyectos
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ModernProjectManager;
