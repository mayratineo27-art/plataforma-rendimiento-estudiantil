import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BookOpen,
  Plus,
  Edit,
  Trash2,
  Save,
  X,
  Palette,
  Smile,
  Star,
  Zap,
  Target,
  Coffee,
  Heart,
  Rocket,
  Award,
  Brain,
  Music,
  Camera,
  Code,
  Laptop,
  Lightbulb,
  TrendingUp
} from 'lucide-react';

/**
 * 🆕 COMPONENTE MEJORADO: Gestión de Cursos con Iconos y Categorías
 * - Selector visual de iconos
 * - Categorías con colores
 * - Mensajes creativos
 */
const CourseManagerPro = ({ userId = 1 }) => {
  const [courses, setCourses] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    code: '',
    professor: '',
    schedule: '',
    category: 'general',
    icon: 'BookOpen',
    color: 'blue'
  });

  // Iconos disponibles
  const availableIcons = [
    { name: 'BookOpen', component: BookOpen, label: 'Libro' },
    { name: 'Brain', component: Brain, label: 'Cerebro' },
    { name: 'Laptop', component: Laptop, label: 'Laptop' },
    { name: 'Code', component: Code, label: 'Código' },
    { name: 'Lightbulb', component: Lightbulb, label: 'Idea' },
    { name: 'Star', component: Star, label: 'Estrella' },
    { name: 'Zap', component: Zap, label: 'Rayo' },
    { name: 'Target', component: Target, label: 'Diana' },
    { name: 'Rocket', component: Rocket, label: 'Cohete' },
    { name: 'Award', component: Award, label: 'Premio' },
    { name: 'Music', component: Music, label: 'Música' },
    { name: 'Camera', component: Camera, label: 'Cámara' },
    { name: 'Heart', component: Heart, label: 'Corazón' },
    { name: 'Coffee', component: Coffee, label: 'Café' },
    { name: 'TrendingUp', component: TrendingUp, label: 'Gráfica' }
  ];

  // Categorías con colores
  const categories = [
    { id: 'general', name: 'General', color: 'blue', emoji: '📚' },
    { id: 'ciencias', name: 'Ciencias', color: 'green', emoji: '🔬' },
    { id: 'matematicas', name: 'Matemáticas', color: 'purple', emoji: '🔢' },
    { id: 'ingenieria', name: 'Ingeniería', color: 'orange', emoji: '⚙️' },
    { id: 'artes', name: 'Artes', color: 'pink', emoji: '🎨' },
    { id: 'idiomas', name: 'Idiomas', color: 'indigo', emoji: '🌍' },
    { id: 'tecnologia', name: 'Tecnología', color: 'cyan', emoji: '💻' },
    { id: 'negocios', name: 'Negocios', color: 'yellow', emoji: '💼' }
  ];

  // Colores disponibles
  const colors = [
    { id: 'blue', name: 'Azul', class: 'from-blue-500 to-blue-600' },
    { id: 'purple', name: 'Morado', class: 'from-purple-500 to-purple-600' },
    { id: 'green', name: 'Verde', class: 'from-green-500 to-green-600' },
    { id: 'orange', name: 'Naranja', class: 'from-orange-500 to-orange-600' },
    { id: 'pink', name: 'Rosa', class: 'from-pink-500 to-pink-600' },
    { id: 'indigo', name: 'Índigo', class: 'from-indigo-500 to-indigo-600' },
    { id: 'red', name: 'Rojo', class: 'from-red-500 to-red-600' },
    { id: 'cyan', name: 'Cian', class: 'from-cyan-500 to-cyan-600' },
    { id: 'yellow', name: 'Amarillo', class: 'from-yellow-500 to-yellow-600' }
  ];

  const motivationalMessages = [
    '¡Crea tu próxima aventura académica! 🚀',
    '¡Agrega un nuevo desafío! 💪',
    '¡Tu futuro empieza aquí! ✨',
    '¡Expande tu conocimiento! 🧠',
    '¡Construye tu éxito! 🏆',
    '¡Un curso más hacia la grandeza! 🌟'
  ];

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/academic/user/${userId}/courses`);
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error('Error cargando cursos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOrUpdate = async () => {
    if (!formData.name) {
      alert('Por favor ingresa el nombre del curso');
      return;
    }

    try {
      setLoading(true);

      const payload = {
        user_id: userId,
        name: formData.name,
        code: formData.code,
        professor: formData.professor,
        schedule: formData.schedule,
        category: formData.category,
        icon: formData.icon,
        color: formData.color
      };

      if (editingCourse) {
        await axios.put(`http://localhost:5000/api/academic/course/${editingCourse.id}`, payload);
        alert('✅ Curso actualizado');
      } else {
        await axios.post('http://localhost:5000/api/academic/course/create', payload);
        alert('✅ Curso creado exitosamente');
      }

      setShowCreateModal(false);
      setEditingCourse(null);
      resetForm();
      loadCourses();
    } catch (error) {
      console.error('Error guardando curso:', error);
      alert('❌ Error al guardar el curso');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (course) => {
    setEditingCourse(course);
    setFormData({
      name: course.name,
      code: course.code || '',
      professor: course.professor || '',
      schedule: course.schedule || '',
      category: course.category || 'general',
      icon: course.icon || 'BookOpen',
      color: course.color || 'blue'
    });
    setShowCreateModal(true);
  };

  const handleDelete = async (courseId) => {
    if (!window.confirm('¿Eliminar este curso?')) return;

    try {
      await axios.delete(`http://localhost:5000/api/academic/course/${courseId}`);
      loadCourses();
    } catch (error) {
      console.error('Error eliminando curso:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      code: '',
      professor: '',
      schedule: '',
      category: 'general',
      icon: 'BookOpen',
      color: 'blue'
    });
    setEditingCourse(null);
  };

  const getIconComponent = (iconName) => {
    const icon = availableIcons.find(i => i.name === iconName);
    return icon ? icon.component : BookOpen;
  };

  const getColorClass = (colorId) => {
    const color = colors.find(c => c.id === colorId);
    return color ? color.class : 'from-blue-500 to-blue-600';
  };

  const getCategoryInfo = (categoryId) => {
    return categories.find(c => c.id === categoryId) || categories[0];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-8 px-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl">
                <BookOpen size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Gestión de Cursos
                </h1>
                <p className="text-gray-600 mt-1">Organiza tus materias con estilo 🎨</p>
              </div>
            </div>
            <button
              onClick={() => {
                resetForm();
                setShowCreateModal(true);
              }}
              className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all"
            >
              <Plus size={20} />
              <span className="font-semibold">
                {motivationalMessages[Math.floor(Math.random() * motivationalMessages.length)]}
              </span>
            </button>
          </div>
        </div>

        {/* Lista de Cursos */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          </div>
        ) : courses.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
            <BookOpen className="mx-auto h-20 w-20 text-gray-300 mb-4" />
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              ¡Empieza tu viaje académico!
            </h3>
            <p className="text-gray-600 mb-6">
              Crea tu primer curso y organiza tu semestre
            </p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:shadow-lg"
            >
              Crear Primer Curso 🚀
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map(course => {
              const IconComponent = getIconComponent(course.icon);
              const colorClass = getColorClass(course.color);
              const category = getCategoryInfo(course.category);

              return (
                <div
                  key={course.id}
                  className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all"
                >
                  {/* Header del Curso */}
                  <div className={`bg-gradient-to-r ${colorClass} p-6 text-white`}>
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-white bg-opacity-20 rounded-xl backdrop-blur-sm">
                        <IconComponent size={32} />
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleEdit(course)}
                          className="p-2 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition"
                        >
                          <Edit size={18} />
                        </button>
                        <button
                          onClick={() => handleDelete(course.id)}
                          className="p-2 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </div>
                    <h3 className="text-xl font-bold mb-1">{course.name}</h3>
                    {course.code && (
                      <p className="text-sm opacity-90">{course.code}</p>
                    )}
                  </div>

                  {/* Contenido del Curso */}
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="text-2xl">{category.emoji}</span>
                      <span className={`text-sm font-semibold px-3 py-1 rounded-full bg-${category.color}-100 text-${category.color}-700`}>
                        {category.name}
                      </span>
                    </div>

                    {course.professor && (
                      <div className="mb-3">
                        <p className="text-xs text-gray-500 mb-1">Profesor</p>
                        <p className="text-sm font-medium text-gray-800">{course.professor}</p>
                      </div>
                    )}

                    {course.schedule && (
                      <div className="mb-3">
                        <p className="text-xs text-gray-500 mb-1">Horario</p>
                        <p className="text-sm font-medium text-gray-800">{course.schedule}</p>
                      </div>
                    )}

                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>Creado: {new Date(course.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Modal de Creación/Edición */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold">
                  {editingCourse ? '✏️ Editar Curso' : '✨ Nuevo Curso'}
                </h2>
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg"
                >
                  <X size={24} />
                </button>
              </div>
            </div>

            <div className="p-6 space-y-6">
              {/* Nombre del Curso */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  📚 Nombre del Curso *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  placeholder="Ej: Cálculo Diferencial"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Código del Curso */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  🔢 Código del Curso
                </label>
                <input
                  type="text"
                  value={formData.code}
                  onChange={(e) => setFormData({...formData, code: e.target.value})}
                  placeholder="Ej: MAT-101"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Profesor */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  👨‍🏫 Profesor
                </label>
                <input
                  type="text"
                  value={formData.professor}
                  onChange={(e) => setFormData({...formData, professor: e.target.value})}
                  placeholder="Ej: Dr. Juan Pérez"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Horario */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  🕐 Horario
                </label>
                <input
                  type="text"
                  value={formData.schedule}
                  onChange={(e) => setFormData({...formData, schedule: e.target.value})}
                  placeholder="Ej: Lun-Mié-Vie 10:00-12:00"
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Categoría */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  🏷️ Categoría
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {categories.map(cat => (
                    <button
                      key={cat.id}
                      onClick={() => setFormData({...formData, category: cat.id})}
                      className={`p-3 rounded-xl border-2 transition-all ${
                        formData.category === cat.id
                          ? `border-${cat.color}-500 bg-${cat.color}-50`
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-2xl mb-1">{cat.emoji}</div>
                      <div className="text-xs font-semibold text-gray-700">{cat.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Selector de Icono */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  🎨 Elige un Icono
                </label>
                <div className="grid grid-cols-5 md:grid-cols-8 gap-3">
                  {availableIcons.map(icon => {
                    const IconComp = icon.component;
                    return (
                      <button
                        key={icon.name}
                        onClick={() => setFormData({...formData, icon: icon.name})}
                        className={`p-3 rounded-xl border-2 transition-all flex flex-col items-center gap-1 ${
                          formData.icon === icon.name
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        title={icon.label}
                      >
                        <IconComp size={24} className={formData.icon === icon.name ? 'text-blue-600' : 'text-gray-600'} />
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Selector de Color */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  🌈 Color del Curso
                </label>
                <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
                  {colors.map(color => (
                    <button
                      key={color.id}
                      onClick={() => setFormData({...formData, color: color.id})}
                      className={`p-4 rounded-xl border-2 transition-all ${
                        formData.color === color.id
                          ? 'border-gray-800 ring-2 ring-gray-400'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className={`h-8 rounded-lg bg-gradient-to-r ${color.class} mb-2`}></div>
                      <div className="text-xs font-semibold text-gray-700">{color.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Botones */}
              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 font-semibold"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleCreateOrUpdate}
                  disabled={loading}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:shadow-lg font-semibold disabled:opacity-50"
                >
                  {loading ? 'Guardando...' : editingCourse ? '💾 Guardar Cambios' : '✨ Crear Curso'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseManagerPro;
