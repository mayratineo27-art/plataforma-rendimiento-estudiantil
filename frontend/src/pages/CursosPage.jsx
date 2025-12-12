import React, { useState, useEffect } from 'react';
import { Plus, BookOpen, Search, Filter } from 'lucide-react';
import CourseCard from '../components/CourseCard';
import EditCourseModal from '../components/EditCourseModal';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const CursosPage = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  
  const userId = 1; // TODO: Get from AuthContext

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/academic/user/${userId}/courses`);
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error('Error loading courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCourse = async (formData) => {
    try {
      const response = await axios.post(`${API_URL}/api/academic/courses`, {
        ...formData,
        user_id: userId
      });
      
      setCourses(prev => [...prev, response.data.course]);
      setShowCreateModal(false);
    } catch (error) {
      console.error('Error creating course:', error);
      throw new Error(error.response?.data?.error || 'Error al crear el curso');
    }
  };

  const handleUpdateCourse = (updatedCourse) => {
    setCourses(prev =>
      prev.map(course =>
        course.id === updatedCourse.id ? updatedCourse : course
      )
    );
  };

  const handleDeleteCourse = (courseId) => {
    setCourses(prev => prev.filter(course => course.id !== courseId));
  };

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (course.code && course.code.toLowerCase().includes(searchTerm.toLowerCase())) ||
                         (course.professor && course.professor.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const matchesCategory = filterCategory === 'all' || course.category === filterCategory;
    
    return matchesSearch && matchesCategory;
  });

  const categories = [
    { value: 'all', label: 'Todos' },
    { value: 'general', label: 'General' },
    { value: 'programacion', label: 'Programación' },
    { value: 'matematicas', label: 'Matemáticas' },
    { value: 'ciencias', label: 'Ciencias' },
    { value: 'idiomas', label: 'Idiomas' },
    { value: 'negocios', label: 'Negocios' },
    { value: 'arte', label: 'Arte' },
    { value: 'ingenieria', label: 'Ingeniería' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="bg-indigo-500/20 p-3 rounded-xl">
                <BookOpen className="w-8 h-8 text-indigo-400" />
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white">Mis Cursos</h1>
                <p className="text-slate-400 mt-1">
                  Gestiona tus cursos académicos
                </p>
              </div>
            </div>

            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-semibold transition shadow-lg hover:shadow-xl"
            >
              <Plus className="w-5 h-5" />
              Nuevo Curso
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
              <div className="text-slate-400 text-sm mb-1">Total de Cursos</div>
              <div className="text-3xl font-bold text-white">{courses.length}</div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
              <div className="text-slate-400 text-sm mb-1">Cursos Activos</div>
              <div className="text-3xl font-bold text-green-400">
                {courses.filter(c => c.status === 'active').length}
              </div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
              <div className="text-slate-400 text-sm mb-1">Categorías</div>
              <div className="text-3xl font-bold text-blue-400">
                {new Set(courses.map(c => c.category)).size}
              </div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700">
              <div className="text-slate-400 text-sm mb-1">Este Semestre</div>
              <div className="text-3xl font-bold text-purple-400">{courses.length}</div>
            </div>
          </div>

          {/* Search and Filter */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                placeholder="Buscar cursos por nombre, código o profesor..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-800/50 border border-slate-700 rounded-lg pl-11 pr-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="relative md:w-64">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="w-full bg-slate-800/50 border border-slate-700 rounded-lg pl-11 pr-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 appearance-none cursor-pointer"
              >
                {categories.map(cat => (
                  <option key={cat.value} value={cat.value}>
                    {cat.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Courses Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          </div>
        ) : filteredCourses.length === 0 ? (
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-12 text-center border border-slate-700">
            <BookOpen className="w-16 h-16 text-slate-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">
              {searchTerm || filterCategory !== 'all' 
                ? 'No se encontraron cursos'
                : 'No tienes cursos registrados'
              }
            </h3>
            <p className="text-slate-400 mb-6">
              {searchTerm || filterCategory !== 'all'
                ? 'Intenta con otros términos de búsqueda'
                : 'Comienza agregando tu primer curso académico'
              }
            </p>
            {!searchTerm && filterCategory === 'all' && (
              <button
                onClick={() => setShowCreateModal(true)}
                className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-semibold transition"
              >
                <Plus className="w-5 h-5" />
                Crear Primer Curso
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map(course => (
              <CourseCard
                key={course.id}
                course={course}
                onUpdate={handleUpdateCourse}
                onDelete={handleDeleteCourse}
              />
            ))}
          </div>
        )}
      </div>

      {/* Create Modal */}
      <EditCourseModal
        course={null}
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSave={handleCreateCourse}
      />
    </div>
  );
};

export default CursosPage;
