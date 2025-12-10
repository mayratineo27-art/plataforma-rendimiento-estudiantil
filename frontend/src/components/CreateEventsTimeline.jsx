import React, { useState } from 'react';
import axios from 'axios';
import { Calendar, Clock, Sparkles, TrendingUp, History } from 'lucide-react';

/**
 * Componente para crear Líneas de Tiempo de EVENTOS HISTÓRICOS
 * NO vinculado a proyectos - Para organizar cronológicamente eventos de cualquier tema
 * Ejemplo: Historia de las computadoras, Evolución del internet, etc.
 */
const CreateEventsTimeline = ({ onTimelineCreated, onCancel, userId }) => {
  const [topic, setTopic] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const examples = [
    '🖥️ Historia de las computadoras',
    '🌐 Evolución del Internet',
    '🚀 Exploración espacial',
    '🎨 Historia del arte',
    '⚽ Historia del fútbol',
    '🎵 Evolución de la música',
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      setError('El tema es obligatorio');
      return;
    }

    if (!userId) {
      setError('No se pudo obtener el ID del usuario');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:5000/api/timeline/events/create',
        {
          user_id: userId,
          topic: topic,
          description: description || null
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data) {
        setTopic('');
        setDescription('');
        onTimelineCreated(response.data);
      }
    } catch (err) {
      console.error('Error creando línea de tiempo de eventos:', err);
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Error al crear la línea de tiempo'
      );
    } finally {
      setLoading(false);
    }
  };

  const setExampleTopic = (example) => {
    setTopic(example);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white p-6 rounded-t-2xl">
          <div className="flex items-center gap-3">
            <History size={32} />
            <div>
              <h2 className="text-2xl font-bold">Línea de Tiempo de Eventos</h2>
              <p className="text-indigo-100 text-sm mt-1">
                Organiza cronológicamente eventos históricos o educativos
              </p>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          {/* Descripción */}
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl p-4 mb-6">
            <div className="flex items-start gap-3">
              <Sparkles className="text-indigo-600 mt-1" size={20} />
              <div>
                <h3 className="font-semibold text-gray-800 mb-1">¿Qué es esto?</h3>
                <p className="text-sm text-gray-600">
                  Crea líneas de tiempo para visualizar la <strong>evolución histórica</strong> de cualquier tema.
                  Perfecto para estudiar la cronología de eventos, inventos, movimientos culturales, etc.
                </p>
              </div>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl">
              {error}
            </div>
          )}

          {/* Campo de tema */}
          <div className="mb-6">
            <label className="block text-sm font-bold text-gray-700 mb-2">
              📚 Tema / Título *
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
              placeholder="Ej: Historia de las computadoras"
              required
            />
          </div>

          {/* Ejemplos rápidos */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              💡 Ejemplos rápidos (haz clic para usar)
            </label>
            <div className="grid grid-cols-2 gap-2">
              {examples.map((example, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setExampleTopic(example)}
                  className="text-left px-4 py-2 bg-gradient-to-r from-indigo-50 to-purple-50 hover:from-indigo-100 hover:to-purple-100 border border-indigo-200 rounded-lg text-sm text-gray-700 transition-all"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {/* Descripción opcional */}
          <div className="mb-6">
            <label className="block text-sm font-bold text-gray-700 mb-2">
              📝 Descripción (Opcional)
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
              placeholder="Agrega detalles sobre qué quieres incluir en esta línea de tiempo..."
              rows="3"
            />
          </div>

          {/* Información adicional */}
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
            <div className="flex items-start gap-3">
              <TrendingUp className="text-blue-600 mt-1" size={20} />
              <div className="text-sm text-gray-700">
                <p className="font-semibold mb-1">✨ Generación automática con IA</p>
                <p>
                  Nuestra IA generará automáticamente los eventos más importantes y relevantes
                  sobre el tema que elijas, organizados cronológicamente.
                </p>
              </div>
            </div>
          </div>

          {/* Botones */}
          <div className="flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onCancel}
              className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold rounded-xl transition-all"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg transition-all disabled:opacity-50 flex items-center gap-2"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Clock className="animate-spin" size={20} />
                  Creando...
                </>
              ) : (
                <>
                  <Calendar size={20} />
                  Crear Línea de Tiempo
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateEventsTimeline;
