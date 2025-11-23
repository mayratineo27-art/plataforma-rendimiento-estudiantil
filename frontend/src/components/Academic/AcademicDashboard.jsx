import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BookOpen,
  Plus,
  Calendar,
  Clock,
  CheckCircle2,
  Circle,
  Trash2,
  Edit,
  FileText,
  TrendingUp,
  Target,
  AlertCircle,
  Download,
  Sparkles
} from 'lucide-react';

const AcademicDashboard = ({ userId }) => {
  const [courses, setCourses] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddCourse, setShowAddCourse] = useState(false);
  const [newCourse, setNewCourse] = useState({
    name: '',
    professor: '',
    schedule_info: '',
    color: '#3B82F6'
  });

  useEffect(() => {
    fetchDashboardData();
  }, [userId]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [dashboardRes, statsRes] = await Promise.all([
        axios.get(`http://localhost:5000/api/academic/user/${userId}/dashboard`),
        axios.get(`http://localhost:5000/api/academic/user/${userId}/stats`)
      ]);
      
      setCourses(dashboardRes.data.courses);
      setTasks(dashboardRes.data.pending_tasks);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCourse = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/academic/courses', {
        ...newCourse,
        user_id: userId
      });
      
      setNewCourse({ name: '', professor: '', schedule_info: '', color: '#3B82F6' });
      setShowAddCourse(false);
      fetchDashboardData();
    } catch (error) {
      console.error('Error creando curso:', error);
      alert('Error al crear el curso');
    }
  };

  const handleDeleteCourse = async (courseId) => {
    if (!window.confirm('¿Eliminar este curso y todas sus tareas?')) return;
    
    try {
      await axios.delete(`http://localhost:5000/api/academic/course/${courseId}`);
      fetchDashboardData();
    } catch (error) {
      console.error('Error eliminando curso:', error);
    }
  };

  const getPriorityColor = (priority) => {
    const colors = {
      critica: 'bg-red-100 text-red-800 border-red-300',
      alta: 'bg-orange-100 text-orange-800 border-orange-300',
      media: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      baja: 'bg-green-100 text-green-800 border-green-300'
    };
    return colors[priority] || colors.media;
  };

  const getPriorityIcon = (priority) => {
    if (priority === 'critica') return <AlertCircle size={16} className="text-red-600" />;
    if (priority === 'alta') return <TrendingUp size={16} className="text-orange-600" />;
    return <Target size={16} className="text-yellow-600" />;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Cargando tu asistente académico...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl shadow-lg">
              <BookOpen size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Asistente Académico
              </h1>
              <p className="text-gray-600 mt-1">Tu espacio de organización inteligente</p>
            </div>
          </div>
          <button
            onClick={() => setShowAddCourse(true)}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
          >
            <Plus size={20} />
            Nuevo Curso
          </button>
        </div>

        {/* Estadísticas */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-blue-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Total Cursos</p>
                  <p className="text-3xl font-bold text-gray-800 mt-2">{stats.total_courses}</p>
                </div>
                <div className="p-3 bg-blue-100 rounded-xl">
                  <BookOpen size={28} className="text-blue-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-yellow-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Tareas Pendientes</p>
                  <p className="text-3xl font-bold text-gray-800 mt-2">{stats.pending_tasks}</p>
                </div>
                <div className="p-3 bg-yellow-100 rounded-xl">
                  <Circle size={28} className="text-yellow-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-green-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Completadas</p>
                  <p className="text-3xl font-bold text-gray-800 mt-2">{stats.completed_tasks}</p>
                </div>
                <div className="p-3 bg-green-100 rounded-xl">
                  <CheckCircle2 size={28} className="text-green-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 border-l-4 border-purple-500 hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">Completitud</p>
                  <p className="text-3xl font-bold text-gray-800 mt-2">{stats.completion_rate}%</p>
                </div>
                <div className="p-3 bg-purple-100 rounded-xl">
                  <TrendingUp size={28} className="text-purple-600" />
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Lista de Cursos */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <BookOpen size={24} className="text-blue-600" />
                Mis Cursos
              </h2>
              {courses.length > 0 && (
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                  {courses.length} {courses.length === 1 ? 'curso' : 'cursos'}
                </span>
              )}
            </div>

            {courses.length === 0 ? (
              <div className="bg-white rounded-2xl shadow-lg p-12 text-center border-2 border-dashed border-gray-300">
                <Sparkles className="mx-auto h-16 w-16 text-gray-400 mb-4" />
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  ¡Comienza tu organización!
                </h3>
                <p className="text-gray-600 mb-6">
                  Agrega tu primer curso para empezar a organizar tus tareas y proyectos
                </p>
                <button
                  onClick={() => setShowAddCourse(true)}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
                >
                  <Plus size={20} />
                  Agregar Primer Curso
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {courses.map((course) => (
                  <div
                    key={course.id}
                    className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden border-l-4"
                    style={{ borderLeftColor: course.color }}
                  >
                    <div className="p-6">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-gray-800 mb-2">
                            {course.name}
                          </h3>
                          {course.professor && (
                            <p className="text-sm text-gray-600 flex items-center gap-2">
                              <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                              {course.professor}
                            </p>
                          )}
                        </div>
                        <button
                          onClick={() => handleDeleteCourse(course.id)}
                          className="p-2 hover:bg-red-50 rounded-lg text-red-600 transition"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>

                      {course.schedule_info && (
                        <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
                          <Clock size={14} />
                          {course.schedule_info}
                        </div>
                      )}

                      <div className="flex gap-2 mt-4">
                        <button className="flex-1 py-2 px-3 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg text-sm font-medium transition flex items-center justify-center gap-2">
                          <FileText size={16} />
                          Ver Tareas
                        </button>
                        <button className="flex-1 py-2 px-3 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-lg text-sm font-medium transition flex items-center justify-center gap-2">
                          <Sparkles size={16} />
                          IA
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Panel de Tareas Pendientes */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <CheckCircle2 size={24} className="text-yellow-600" />
                Tareas Urgentes
              </h2>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6 space-y-4">
              {tasks.length === 0 ? (
                <div className="text-center py-8">
                  <CheckCircle2 className="mx-auto h-16 w-16 text-green-500 mb-4" />
                  <p className="text-gray-600 font-medium">
                    ¡Todo al día!
                  </p>
                  <p className="text-sm text-gray-500 mt-2">
                    No tienes tareas pendientes
                  </p>
                </div>
              ) : (
                tasks.slice(0, 8).map((task) => (
                  <div
                    key={task.id}
                    className={`p-4 rounded-xl border-2 hover:shadow-md transition-all ${getPriorityColor(task.priority)}`}
                  >
                    <div className="flex items-start gap-3">
                      {getPriorityIcon(task.priority)}
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-800 mb-1">
                          {task.title}
                        </h4>
                        {task.due_date && (
                          <div className="flex items-center gap-2 text-xs text-gray-600">
                            <Calendar size={12} />
                            {new Date(task.due_date).toLocaleDateString()}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Modal Agregar Curso */}
        {showAddCourse && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                <Plus size={24} className="text-blue-600" />
                Nuevo Curso
              </h3>
              <form onSubmit={handleCreateCourse} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Nombre del Curso *
                  </label>
                  <input
                    type="text"
                    required
                    value={newCourse.name}
                    onChange={(e) => setNewCourse({ ...newCourse, name: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition"
                    placeholder="Ej: Matemáticas Avanzadas"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Profesor
                  </label>
                  <input
                    type="text"
                    value={newCourse.professor}
                    onChange={(e) => setNewCourse({ ...newCourse, professor: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition"
                    placeholder="Ej: Dr. García"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Horario
                  </label>
                  <input
                    type="text"
                    value={newCourse.schedule_info}
                    onChange={(e) => setNewCourse({ ...newCourse, schedule_info: e.target.value })}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none transition"
                    placeholder="Ej: Lun/Mié 10:00-12:00"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Color
                  </label>
                  <div className="flex gap-2">
                    {['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899'].map(color => (
                      <button
                        key={color}
                        type="button"
                        onClick={() => setNewCourse({ ...newCourse, color })}
                        className={`w-10 h-10 rounded-full transition-transform hover:scale-110 ${
                          newCourse.color === color ? 'ring-4 ring-gray-300' : ''
                        }`}
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowAddCourse(false)}
                    className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg transition"
                  >
                    Crear Curso
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AcademicDashboard;
