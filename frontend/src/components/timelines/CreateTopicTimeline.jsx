import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const CreateTopicTimeline = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [courses, setCourses] = useState([]);

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_id: '',
    course_topic: '',
    start_date: '',
    end_date: '',
    allow_project_creation: false
  });

  useEffect(() => {
    fetchCourses();
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
      setError('Error al cargar los cursos disponibles');
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');
      
      // Obtener user_id del localStorage o del token
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        throw new Error('No se pudo obtener la información del usuario');
      }
      
      // Validaciones
      if (!formData.title.trim()) {
        throw new Error('El título es requerido');
      }
      if (!formData.course_id) {
        throw new Error('Debe seleccionar un curso');
      }
      if (!formData.course_topic.trim()) {
        throw new Error('El tema del curso es requerido');
      }
      if (!formData.start_date) {
        throw new Error('La fecha de inicio es requerida');
      }

      const payload = {
        user_id: parseInt(userId),
        title: formData.title.trim(),
        description: formData.description.trim() || null,
        course_id: parseInt(formData.course_id),
        course_topic: formData.course_topic.trim(),
        start_date: formData.start_date,
        end_date: formData.end_date || null,
        generate_with_ai: false,  // Por defecto sin IA, se puede añadir opción después
        steps: []  // Por ahora sin pasos iniciales
      };

      const response = await axios.post(
        `${API_URL}/api/timeline/topic/create`,
        payload,
        {
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      setSuccess('¡Línea de tiempo creada exitosamente!');
      setTimeout(() => {
        navigate(`/timeline/${response.data.timeline.id}`);
      }, 1500);

    } catch (err) {
      console.error('Error al crear línea de tiempo:', err);
      setError(err.response?.data?.error || err.message || 'Error al crear la línea de tiempo');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/timelines');
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">
          Crear Línea de Tiempo sobre Tema de Curso
        </h2>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-md">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Título */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Título de la Línea de Tiempo *
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ej: Evolución de la Programación Orientada a Objetos"
            />
          </div>

          {/* Descripción */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Descripción
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe el contenido y objetivos de esta línea de tiempo..."
            />
          </div>

          {/* Curso */}
          <div>
            <label htmlFor="course_id" className="block text-sm font-medium text-gray-700 mb-2">
              Curso *
            </label>
            <select
              id="course_id"
              name="course_id"
              value={formData.course_id}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Seleccione un curso</option>
              {courses.map(course => (
                <option key={course.id} value={course.id}>
                  {course.name}
                </option>
              ))}
            </select>
          </div>

          {/* Tema del Curso */}
          <div>
            <label htmlFor="course_topic" className="block text-sm font-medium text-gray-700 mb-2">
              Tema Específico del Curso *
            </label>
            <input
              type="text"
              id="course_topic"
              name="course_topic"
              value={formData.course_topic}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ej: Principios SOLID, Patrones de Diseño, Algoritmos de Ordenamiento"
            />
            <p className="mt-1 text-sm text-gray-500">
              Ingrese el tema o concepto específico que cubrirá esta línea de tiempo
            </p>
          </div>

          {/* Fechas */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-2">
                Fecha de Inicio *
              </label>
              <input
                type="date"
                id="start_date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-2">
                Fecha de Fin (Opcional)
              </label>
              <input
                type="date"
                id="end_date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                min={formData.start_date}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Permitir creación de proyectos */}
          <div className="flex items-center">
            <input
              type="checkbox"
              id="allow_project_creation"
              name="allow_project_creation"
              checked={formData.allow_project_creation}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="allow_project_creation" className="ml-2 block text-sm text-gray-700">
              Permitir que los estudiantes creen proyectos en esta línea de tiempo
            </label>
          </div>

          {/* Botones */}
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={handleCancel}
              disabled={loading}
              className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creando...' : 'Crear Línea de Tiempo'}
            </button>
          </div>
        </form>
      </div>

      {/* Información adicional */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-800 mb-2">ℹ️ Acerca de las Líneas de Tiempo de Temas</h3>
        <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
          <li>Estas líneas de tiempo te permiten organizar contenido sobre temas específicos de cualquier curso</li>
          <li>Puedes añadir eventos, hitos y recursos relacionados con el tema</li>
          <li>Los estudiantes pueden seguir el progreso y aprender de manera estructurada</li>
          <li>Si activas "Permitir creación de proyectos", los estudiantes podrán crear sus propios proyectos relacionados con el tema</li>
        </ul>
      </div>
    </div>
  );
};

export default CreateTopicTimeline;
