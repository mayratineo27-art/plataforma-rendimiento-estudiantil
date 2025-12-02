import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CreateTopicTimeline from './CreateTopicTimeline';
import { jwtDecode } from 'jwt-decode';

const TopicTimelines = () => {
  const [timelines, setTimelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setUserId(decoded.user_id || decoded.id || decoded.sub);
      } catch (error) {
        console.error('Error decoding token:', error);
      }
    }
    fetchTopicTimelines();
  }, []);

  const fetchTopicTimelines = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:5000/api/timeline/topic', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTimelines(response.data.timelines || []);
      setError(null);
    } catch (err) {
      console.error('Error obteniendo líneas de tiempo:', err);
      setError('Error al cargar las líneas de tiempo');
    } finally {
      setLoading(false);
    }
  };

  const handleTimelineCreated = (newTimeline) => {
    setTimelines([newTimeline, ...timelines]);
    setShowCreateForm(false);
  };

  const handleDeleteTimeline = async (timelineId) => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar esta línea de tiempo?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:5000/api/timeline/${timelineId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTimelines(timelines.filter(t => t.id !== timelineId));
    } catch (err) {
      console.error('Error eliminando línea de tiempo:', err);
      alert('Error al eliminar la línea de tiempo');
    }
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
        <div className="text-lg text-gray-600">Cargando líneas de tiempo...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Líneas de Tiempo por Tema
        </h1>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          {showCreateForm ? 'Cancelar' : '+ Nueva Línea de Tiempo'}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {showCreateForm && (
      <div className="mb-8">
      <CreateTopicTimeline 
        onTimelineCreated={handleTimelineCreated}
        onCancel={() => setShowCreateForm(false)}
        userId={userId}
      />
      </div>
      )}

      {timelines.length === 0 ? (
        <div className="bg-gray-100 rounded-lg p-8 text-center">
          <p className="text-gray-600 text-lg">
            No hay líneas de tiempo de temas creadas aún.
          </p>
          <p className="text-gray-500 mt-2">
            Haz clic en "Nueva Línea de Tiempo" para crear una.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {timelines.map((timeline) => (
            <div
              key={timeline.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-xl font-bold text-gray-800">
                  {timeline.course_topic || timeline.topic_name}
                </h3>
                <button
                  onClick={() => handleDeleteTimeline(timeline.id)}
                  className="text-red-500 hover:text-red-700"
                  title="Eliminar"
                >
                  🗑️
                </button>
              </div>
              
              <div className="mb-2">
                <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                  {timeline.course_name || 'Sin curso'}
                </span>
              </div>

              {timeline.description && (
                <p className="text-gray-600 text-sm mb-4">
                  {timeline.description}
                </p>
              )}

              <div className="text-sm text-gray-500 space-y-1">
                <div>
                  <span className="font-semibold">Inicio:</span>{' '}
                  {formatDate(timeline.start_date)}
                </div>
                {timeline.end_date && (
                  <div>
                    <span className="font-semibold">Fin:</span>{' '}
                    {formatDate(timeline.end_date)}
                  </div>
                )}
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <a
                  href={`/timeline/${timeline.id}`}
                  className="text-blue-500 hover:text-blue-700 text-sm font-semibold"
                >
                  Ver detalles →
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TopicTimelines;
