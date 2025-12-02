import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const TopicTimelines = () => {
  const navigate = useNavigate();
  const [timelines, setTimelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState({
    course_id: '',
    search: ''
  });
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    fetchCourses();
    fetchTimelines();
  }, []);

  const fetchCourses = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCourses(response.data);
    } catch (err) {
      console.error('Error al cargar cursos:', err);
    }
  };

  const fetchTimelines = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/timeline/user/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Filtrar solo las líneas de tiempo tipo 'free'
      const topicTimelines = response.data.filter(t => t.type === 'free');
      setTimelines(topicTimelines);
    } catch (err) {
      console.error('Error al cargar líneas de tiempo:', err);
      setError('Error al cargar las líneas de tiempo de temas');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar esta línea de tiempo?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/timelines/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setTimelines(timelines.filter(t => t.id !== id));
    } catch (err) {
      console.error('Error al eliminar línea de tiempo:', err);
      alert('Error al eliminar la línea de tiempo');
    }
  };

  const filteredTimelines = timelines.filter(timeline => {
    if (filter.course_id && timeline.course_id !== parseInt(filter.course_id)) {
      return false;
    }
    if (filter.search) {
      const searchLower = filter.search.toLowerCase();
      return (
        timeline.title?.toLowerCase().includes(searchLower) ||
        timeline.description?.toLowerCase().includes(searchLower) ||
        timeline.course_topic?.toLowerCase().includes(searchLower)
      );
    }
    return true;
  });

  const getCourseName = (courseId) => {
    const course = courses.find(c => c.id === courseId);
    return course ? course.name : 'Curso desconocido';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800">
          Líneas de Tiempo de Temas
        </h2>
        <button
          onClick={() => navigate('/timelines/topic/create')}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          + Nueva Línea de Tiempo
        </button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="course_filter" className="block text-sm font-medium text-gray-700 mb-2">
              Filtrar por Curso
            </label>
            <select
              id="course_filter"
              value={filter.course_id}
              onChange={(e) => setFilter({ ...filter, course_id: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos los cursos</option>
              {courses.map(course => (
                <option key={course.id} value={course.id}>
                  {course.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
              Buscar
            </label>
            <input
              type="text"
              id="search"
              value={filter.search}
              onChange={(e) => setFilter({ ...filter, search: e.target.value })}
              placeholder="Buscar por título, descripción o tema..."
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Lista de líneas de tiempo */}
      {filteredTimelines.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <p className="text-gray-600 mb-4">
            {timelines.length === 0 
              ? 'No hay líneas de tiempo de temas creadas aún.'
              : 'No se encontraron líneas de tiempo con los filtros aplicados.'}
          </p>
          <button
            onClick={() => navigate('/timelines/topic/create')}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Crear Primera Línea de Tiempo
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTimelines.map(timeline => (
            <div key={timeline.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="text-xl font-semibold text-gray-800 flex-1">
                    {timeline.title}
                  </h3>
                  <span className="ml-2 px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">
                    Tema
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Curso:</span> {getCourseName(timeline.course_id)}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Tema:</span> {timeline.course_topic || 'No especificado'}
                  </p>
                  {timeline.description && (
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {timeline.description}
                    </p>
                  )}
                </div>

                <div className="border-t pt-3 mb-4">
                  <p className="text-xs text-gray-500">
                    <span className="font-medium">Inicio:</span> {formatDate(timeline.start_date)}
                  </p>
                  {timeline.end_date && (
                    <p className="text-xs text-gray-500">
                      <span className="font-medium">Fin:</span> {formatDate(timeline.end_date)}
                    </p>
                  )}
                </div>

                {timeline.allow_project_creation && (
                  <div className="mb-4">
                    <span className="inline-flex items-center px-2 py-1 text-xs font-medium rounded bg-green-100 text-green-800">
                      ✓ Permite proyectos
                    </span>
                  </div>
                )}

                <div className="flex space-x-2">
                  <Link
                    to={`/timelines/${timeline.id}`}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white text-center text-sm rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    Ver Detalles
                  </Link>
                  <button
                    onClick={() => handleDelete(timeline.id)}
                    className="px-4 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Información adicional */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-800 mb-2">💡 Acerca de las Líneas de Tiempo de Temas</h3>
        <p className="text-sm text-blue-700">
          Las líneas de tiempo de temas te permiten organizar y estructurar el aprendizaje sobre 
          conceptos específicos de cualquier curso. Puedes crear eventos, añadir recursos y permitir 
          que los estudiantes desarrollen proyectos relacionados con el tema.
        </p>
      </div>
    </div>
  );
};

export default TopicTimelines;
