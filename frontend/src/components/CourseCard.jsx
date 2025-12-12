import React, { useState } from 'react';
import { Edit, Trash2, MoreVertical, BookOpen, User, Calendar, Clock } from 'lucide-react';
import EditCourseModal from './EditCourseModal';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const CourseCard = ({ course, onUpdate, onDelete }) => {
  const [showMenu, setShowMenu] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const colorClasses = {
    slate: 'from-slate-600 to-slate-800',
    cyan: 'from-cyan-600 to-cyan-800',
    teal: 'from-teal-600 to-teal-800',
    emerald: 'from-emerald-600 to-emerald-800',
    sky: 'from-sky-600 to-sky-800',
    violet: 'from-violet-600 to-violet-800',
    rose: 'from-rose-600 to-rose-800',
    amber: 'from-amber-600 to-amber-800'
  };

  const iconMap = {
    BookOpen: '📚',
    Code: '💻',
    Calculator: '🧮',
    Atom: '⚛️',
    Globe: '🌍',
    TrendingUp: '📈',
    Palette: '🎨',
    Cpu: '🖥️',
    Database: '💾',
    Zap: '⚡'
  };

  const handleSaveCourse = async (formData) => {
    try {
      const response = await axios.put(
        `${API_URL}/api/academic/courses/${course.id}`,
        formData
      );
      
      if (onUpdate) {
        onUpdate(response.data.course);
      }
      
      setShowEditModal(false);
    } catch (error) {
      console.error('Error updating course:', error);
      throw new Error(error.response?.data?.error || 'Error al actualizar el curso');
    }
  };

  const handleDeleteCourse = async () => {
    if (!window.confirm(`¿Estás seguro de eliminar el curso "${course.name}"?`)) {
      return;
    }

    setDeleting(true);
    try {
      await axios.delete(`${API_URL}/api/academic/courses/${course.id}`);
      
      if (onDelete) {
        onDelete(course.id);
      }
    } catch (error) {
      console.error('Error deleting course:', error);
      alert('Error al eliminar el curso');
    } finally {
      setDeleting(false);
      setShowMenu(false);
    }
  };

  return (
    <>
      <div className="relative group">
        <div className={`bg-gradient-to-br ${colorClasses[course.color || 'blue']} rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-105 overflow-hidden`}>
          {/* Menu Button */}
          <div className="absolute top-3 right-3 z-10">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="bg-black/30 backdrop-blur-sm p-2 rounded-lg hover:bg-black/50 transition text-white"
            >
              <MoreVertical className="w-5 h-5" />
            </button>

            {/* Dropdown Menu */}
            {showMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-slate-800 rounded-lg shadow-xl border border-slate-700 overflow-hidden">
                <button
                  onClick={() => {
                    setShowEditModal(true);
                    setShowMenu(false);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 text-white hover:bg-slate-700 transition"
                >
                  <Edit className="w-4 h-4 text-blue-400" />
                  <span>Editar</span>
                </button>
                <button
                  onClick={handleDeleteCourse}
                  disabled={deleting}
                  className="w-full flex items-center gap-3 px-4 py-3 text-white hover:bg-slate-700 transition disabled:opacity-50"
                >
                  <Trash2 className="w-4 h-4 text-red-400" />
                  <span>{deleting ? 'Eliminando...' : 'Eliminar'}</span>
                </button>
              </div>
            )}
          </div>

          {/* Course Content */}
          <div className="p-6 text-white">
            {/* Icon and Code */}
            <div className="flex items-center justify-between mb-4">
              <div className="text-5xl">
                {iconMap[course.icon] || '📚'}
              </div>
              {course.code && (
                <div className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-semibold">
                  {course.code}
                </div>
              )}
            </div>

            {/* Course Name */}
            <h3 className="text-xl font-bold mb-2 line-clamp-2">
              {course.name}
            </h3>

            {/* Category */}
            {course.category && (
              <div className="inline-block bg-white/10 px-3 py-1 rounded-full text-xs font-semibold mb-4">
                {course.category}
              </div>
            )}

            {/* Course Details */}
            <div className="space-y-2 text-sm opacity-90">
              {course.professor && (
                <div className="flex items-center gap-2">
                  <User className="w-4 h-4" />
                  <span className="truncate">{course.professor}</span>
                </div>
              )}
              
              {course.schedule_info && (
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4" />
                  <span className="truncate">{course.schedule_info}</span>
                </div>
              )}
            </div>

            {/* Footer with status */}
            <div className="mt-4 pt-4 border-t border-white/20 flex items-center justify-between">
              <span className="text-xs opacity-75">
                {course.status === 'active' ? '✓ Activo' : 'Inactivo'}
              </span>
              {course.created_at && (
                <span className="text-xs opacity-75">
                  {new Date(course.created_at).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Edit Modal */}
      <EditCourseModal
        course={course}
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        onSave={handleSaveCourse}
      />
    </>
  );
};

export default CourseCard;
