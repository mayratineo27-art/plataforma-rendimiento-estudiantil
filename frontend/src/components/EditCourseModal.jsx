import React, { useState, useEffect } from 'react';
import { X, BookOpen, User, Calendar, Tag, Palette } from 'lucide-react';

const EditCourseModal = ({ course, isOpen, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    professor: '',
    schedule: '',
    category: 'general',
    icon: 'BookOpen',
    color: 'slate'
  });

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (course) {
      setFormData({
        name: course.name || '',
        code: course.code || '',
        professor: course.professor || '',
        schedule: course.schedule_info || '',
        category: course.category || 'general',
        icon: course.icon || 'BookOpen',
        color: course.color || 'slate'
      });
    }
  }, [course]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!formData.name.trim()) {
      setError('El nombre del curso es obligatorio');
      return;
    }

    setSaving(true);
    
    try {
      await onSave(formData);
      onClose();
    } catch (err) {
      setError(err.message || 'Error al guardar el curso');
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen) return null;

  const categories = [
    { value: 'general', label: 'General' },
    { value: 'programacion', label: 'Programación' },
    { value: 'matematicas', label: 'Matemáticas' },
    { value: 'ciencias', label: 'Ciencias' },
    { value: 'idiomas', label: 'Idiomas' },
    { value: 'negocios', label: 'Negocios' },
    { value: 'arte', label: 'Arte' },
    { value: 'ingenieria', label: 'Ingeniería' }
  ];

  const icons = [
    'BookOpen', 'Code', 'Calculator', 'Atom', 'Globe', 
    'TrendingUp', 'Palette', 'Cpu', 'Database', 'Zap'
  ];

  const colors = [
    { value: 'slate', label: 'Pizarra', class: 'bg-slate-600' },
    { value: 'cyan', label: 'Cian', class: 'bg-cyan-600' },
    { value: 'teal', label: 'Turquesa', class: 'bg-teal-600' },
    { value: 'emerald', label: 'Esmeralda', class: 'bg-emerald-600' },
    { value: 'sky', label: 'Azul Cielo', class: 'bg-sky-600' },
    { value: 'violet', label: 'Violeta', class: 'bg-violet-600' },
    { value: 'rose', label: 'Rosa', class: 'bg-rose-600' },
    { value: 'amber', label: 'Ámbar', class: 'bg-amber-600' }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-slate-800 rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4">
        {/* Header */}
        <div className="sticky top-0 bg-slate-800 border-b border-slate-700 p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-500/20 p-2 rounded-lg">
              <BookOpen className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">
                {course ? 'Editar Curso' : 'Nuevo Curso'}
              </h2>
              <p className="text-slate-400 text-sm">
                {course ? 'Actualiza la información del curso' : 'Agrega un nuevo curso académico'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition p-2 hover:bg-slate-700 rounded-lg"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Error Message */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {/* Nombre del Curso */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Nombre del Curso *
            </label>
            <div className="relative">
              <BookOpen className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg pl-11 pr-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Ej: Introducción a la Programación"
                required
              />
            </div>
          </div>

          {/* Código del Curso */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Código del Curso
            </label>
            <div className="relative">
              <Tag className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                name="code"
                value={formData.code}
                onChange={handleChange}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg pl-11 pr-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Ej: CS101"
              />
            </div>
          </div>

          {/* Profesor */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Profesor
            </label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                name="professor"
                value={formData.professor}
                onChange={handleChange}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg pl-11 pr-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Ej: Dr. Juan Pérez"
              />
            </div>
          </div>

          {/* Horario */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Horario
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                name="schedule"
                value={formData.schedule}
                onChange={handleChange}
                className="w-full bg-slate-700/50 border border-slate-600 rounded-lg pl-11 pr-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Ej: Lun/Mié 10:00-12:00"
              />
            </div>
          </div>

          {/* Categoría */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Categoría
            </label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full bg-slate-700/50 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          {/* Icono */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">
              Icono
            </label>
            <div className="grid grid-cols-5 gap-2">
              {icons.map(icon => (
                <button
                  key={icon}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, icon }))}
                  className={`p-3 rounded-lg border-2 transition ${
                    formData.icon === icon
                      ? 'border-indigo-500 bg-indigo-500/20'
                      : 'border-slate-600 bg-slate-700/50 hover:border-slate-500'
                  }`}
                >
                  <span className="text-2xl">{icon === 'BookOpen' ? '📚' : icon === 'Code' ? '💻' : icon === 'Calculator' ? '🧮' : icon === 'Atom' ? '⚛️' : icon === 'Globe' ? '🌍' : icon === 'TrendingUp' ? '📈' : icon === 'Palette' ? '🎨' : icon === 'Cpu' ? '🖥️' : icon === 'Database' ? '💾' : '⚡'}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Color */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2 flex items-center gap-2">
              <Palette className="w-4 h-4" />
              Color
            </label>
            <div className="grid grid-cols-4 gap-3">
              {colors.map(color => (
                <button
                  key={color.value}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, color: color.value }))}
                  className={`p-3 rounded-lg border-2 transition flex items-center gap-2 ${
                    formData.color === color.value
                      ? 'border-white bg-slate-700'
                      : 'border-slate-600 bg-slate-700/50 hover:border-slate-500'
                  }`}
                >
                  <div className={`w-6 h-6 rounded-full ${color.class}`}></div>
                  <span className="text-white text-sm">{color.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition font-semibold"
              disabled={saving}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={saving}
            >
              {saving ? 'Guardando...' : course ? 'Guardar Cambios' : 'Crear Curso'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditCourseModal;
