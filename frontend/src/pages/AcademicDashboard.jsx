import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Calendar, CheckCircle, Plus, Brain, FileText, 
  Upload, RefreshCw, Trash2, CheckSquare, Square, Clock, X,
  Download, Search, Filter, TrendingUp, BookMarked, Layers,
  FolderOpen, BarChart3
} from 'lucide-react';
import Stopwatch from '../components/Stopwatch';
import TimelineViewer from '../components/TimelineViewer';
import ModernProjectManager from '../components/Projects/ModernProjectManager'; // 🆕 Proyectos mejorado
import EvolutionChart from '../components/EvolutionChart';
import TimelineCreator from '../components/Timeline/TimelineCreator'; // 🆕 Timeline con creador
import SyllabusAnalyzerPro from '../components/Syllabus/SyllabusAnalyzerPro'; // 🆕 Syllabus con historial
import CourseManagerPro from '../components/Courses/CourseManagerPro'; // 🆕 Cursos con iconos 

// --- COMPONENTE HERRAMIENTAS IA ---
const StudyTools = () => {
  const [mode, setMode] = useState('mindmap');
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [selectedCourseId, setSelectedCourseId] = useState('');
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [history, setHistory] = useState([]);

  const USER_ID = 1; 

  useEffect(() => {
    fetch(`/api/academic/user/${USER_ID}/dashboard`)
      .then(res => res.json())
      .then(data => setCourses(data.courses || []))
      .catch(err => console.error(err));
    
    // Cargar historial del localStorage
    const savedHistory = localStorage.getItem('study_tools_history');
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

  const saveToHistory = (type, input, output) => {
    const newEntry = {
      id: Date.now(),
      type,
      input: input.substring(0, 100),
      output,
      course: courses.find(c => c.id == selectedCourseId)?.name || "General",
      timestamp: new Date().toISOString()
    };
    
    const updatedHistory = [newEntry, ...history].slice(0, 10); // Mantener solo 10
    setHistory(updatedHistory);
    localStorage.setItem('study_tools_history', JSON.stringify(updatedHistory));
  };

  const handleGenerate = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    setResult(null);

    const courseName = courses.find(c => c.id == selectedCourseId)?.name || "General";
    const endpoint = mode === 'summary' ? '/api/academic/tools/summary' : '/api/academic/tools/mindmap';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText, context: `Curso de ${courseName}` })
      });
      const data = await res.json();
      const resultData = mode === 'mindmap' ? data.mindmap : data.summary;
      setResult(resultData);
      saveToHistory(mode, inputText, resultData);
    } catch (error) {
      alert("Error al conectar con la IA");
    } finally {
      setLoading(false);
    }
  };

  const exportAsJSON = () => {
    if (!result) return;
    const dataStr = JSON.stringify(result, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${mode}-${Date.now()}.json`;
    link.click();
  };

  const exportAsText = () => {
    if (!result) return;
    const textContent = mode === 'mindmap' ? JSON.stringify(result, null, 2) : result;
    const dataBlob = new Blob([textContent], { type: 'text/plain' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${mode}-${Date.now()}.txt`;
    link.click();
  };

  const MindMapNode = ({ node, level = 0 }) => {
    if (!node) return null;
    const colors = [
      'bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-lg',
      'bg-gradient-to-br from-blue-100 to-indigo-100 text-blue-900 border-2 border-blue-300',
      'bg-white text-gray-700 border-2 border-gray-300 hover:border-blue-400 transition'
    ];
    const style = colors[level] || colors[2];

    return (
      <div className="flex flex-col items-center animate-in fade-in slide-in-from-top-2 duration-300">
        <div className={`px-5 py-3 rounded-xl border shadow-md text-center mb-6 font-medium ${style} min-w-[140px] max-w-[280px] transform hover:scale-105 transition-transform cursor-pointer`}>
          {node.root || node.name || "Nodo"}
        </div>
        {node.children && node.children.length > 0 && (
          <div className="flex gap-8 relative">
            <div className="absolute -top-3 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-blue-300 to-transparent mx-auto w-[calc(100%-2rem)]"></div>
            {node.children.map((child, idx) => (
              <div key={idx} className="flex flex-col items-center relative">
                <div className="h-3 w-0.5 bg-blue-300 mb-0 absolute -top-3"></div>
                <MindMapNode node={child} level={level + 1} />
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg border border-gray-200 p-8 min-h-[600px]">
      {/* Header mejorado */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 pb-6 border-b-2 border-gradient-to-r from-blue-200 to-purple-200 gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-md">
            <Brain size={28} className="text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Herramientas IA</h2>
            <p className="text-sm text-gray-500">Procesa tus documentos con inteligencia artificial</p>
          </div>
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex gap-2 bg-gradient-to-r from-gray-100 to-gray-50 p-1.5 rounded-xl shadow-inner">
            <button 
              onClick={() => setMode('mindmap')} 
              className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${mode === 'mindmap' ? 'bg-white text-blue-700 shadow-md transform scale-105' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <Layers size={16} className="inline mr-2" />
              Mapa Mental
            </button>
            <button 
              onClick={() => setMode('summary')} 
              className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${mode === 'summary' ? 'bg-white text-purple-700 shadow-md transform scale-105' : 'text-gray-500 hover:text-gray-700'}`}
            >
              <FileText size={16} className="inline mr-2" />
              Resumen
            </button>
          </div>
          <div className="flex items-center gap-2 border-l-2 border-gray-200 pl-3">
            <span className="text-xs font-bold text-gray-400 uppercase tracking-wide">Tiempo</span>
            <Stopwatch courseId={selectedCourseId} userId={USER_ID} />
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8 h-full">
        {/* Panel de entrada */}
        <div className="flex flex-col gap-4">
            <div>
                <label className="text-xs font-bold text-gray-600 uppercase mb-2 block flex items-center gap-2">
                  <BookMarked size={14} />
                  Contexto del Curso
                </label>
                <select 
                    value={selectedCourseId}
                    onChange={(e) => setSelectedCourseId(e.target.value)}
                    className="w-full p-3 bg-gradient-to-br from-gray-50 to-white border-2 border-gray-200 rounded-xl text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition shadow-sm"
                >
                    <option value="">🌐 General (Sin curso específico)</option>
                    {courses.map(c => <option key={c.id} value={c.id}>📚 {c.name}</option>)}
                </select>
            </div>
            
            <div className="flex-1">
                <label className="text-xs font-bold text-gray-600 uppercase mb-2 block">
                  {mode === 'mindmap' ? '💡 Describe el tema' : '📄 Texto a resumir'}
                </label>
                <textarea
                    className="w-full h-64 p-4 bg-gradient-to-br from-gray-50 to-white border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none text-sm leading-relaxed outline-none shadow-sm transition"
                    placeholder={mode === 'mindmap' ? "Ej: Revolución Francesa, causas y consecuencias principales..." : "Pega aquí el texto que deseas resumir..."}
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                />
            </div>
            
            <button 
              onClick={handleGenerate} 
              disabled={loading || !inputText} 
              className="w-full py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all duration-200 flex justify-center items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98]"
            >
                {loading ? (
                  <>
                    <RefreshCw className="animate-spin" size={20} />
                    Procesando con IA...
                  </>
                ) : (
                  <>
                    <Brain size={20} />
                    Generar {mode === 'mindmap' ? 'Mapa' : 'Resumen'}
                  </>
                )}
            </button>
        </div>

        {/* Panel de resultados mejorado */}
        <div className="lg:col-span-2 bg-gradient-to-br from-slate-50 to-gray-100 rounded-2xl border-2 border-gray-200 overflow-hidden relative min-h-[400px] shadow-inner">
          {/* Toolbar de exportación */}
          {result && (
            <div className="absolute top-4 right-4 z-10 flex gap-2">
              <button 
                onClick={exportAsText} 
                className="p-2 bg-white rounded-lg shadow-md hover:shadow-lg transition text-gray-700 hover:text-blue-600"
                title="Exportar como TXT"
              >
                <Download size={18} />
              </button>
              <button 
                onClick={exportAsJSON} 
                className="p-2 bg-white rounded-lg shadow-md hover:shadow-lg transition text-gray-700 hover:text-blue-600"
                title="Exportar como JSON"
              >
                <FileText size={18} />
              </button>
            </div>
          )}
          
          <div className="p-8 overflow-auto h-full">
            {!result && !loading && (
              <div className="flex flex-col items-center justify-center h-full text-gray-400 animate-in fade-in duration-500">
                  <div className="p-6 bg-white rounded-2xl shadow-md mb-4">
                    <Brain size={56} className="opacity-20" />
                  </div>
                  <p className="text-base font-medium">Los resultados aparecerán aquí</p>
                  <p className="text-xs mt-2 text-gray-400">Ingresa texto y presiona "Generar"</p>
              </div>
            )}
            
            {loading && (
              <div className="absolute inset-0 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center">
                  <div className="animate-spin w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full mb-4"></div>
                  <p className="text-sm font-medium text-gray-600">Analizando contenido...</p>
              </div>
            )}
            
            {result && mode === 'mindmap' && (
              <div className="w-full overflow-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
                <MindMapNode node={result} />
              </div>
            )}
            
            {result && mode === 'summary' && (
              <div className="prose prose-sm max-w-none bg-white p-6 rounded-xl shadow-md animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="whitespace-pre-wrap leading-relaxed text-gray-700">{result}</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Historial reciente */}
      {history.length > 0 && (
        <div className="mt-8 pt-6 border-t-2 border-gray-200">
          <h3 className="text-sm font-bold text-gray-600 uppercase mb-3 flex items-center gap-2">
            <Clock size={16} />
            Historial Reciente
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {history.slice(0, 6).map(item => (
              <div 
                key={item.id} 
                className="bg-white p-3 rounded-lg border border-gray-200 hover:border-blue-300 transition cursor-pointer group"
                onClick={() => {
                  setInputText(item.input);
                  setMode(item.type);
                }}
              >
                <div className="flex items-start justify-between mb-2">
                  <span className={`text-xs font-semibold px-2 py-1 rounded ${item.type === 'mindmap' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'}`}>
                    {item.type === 'mindmap' ? 'Mapa' : 'Resumen'}
                  </span>
                  <span className="text-xs text-gray-400">{new Date(item.timestamp).toLocaleDateString()}</span>
                </div>
                <p className="text-xs text-gray-600 line-clamp-2">{item.input}...</p>
                <p className="text-xs text-blue-600 mt-1 font-medium">{item.course}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// --- DASHBOARD PRINCIPAL ---
const AcademicDashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [courses, setCourses] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [uploadingId, setUploadingId] = useState(null);
  
  // Estados para el formulario de Crear Curso
  const [isCreating, setIsCreating] = useState(false);
  const [newCourseName, setNewCourseName] = useState('');
  const [newCourseProf, setNewCourseProf] = useState('');
  
  // Nuevos estados para búsqueda y filtros
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPriority, setFilterPriority] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  const USER_ID = 1;

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const res = await fetch(`/api/academic/user/${USER_ID}/dashboard`);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Error al cargar dashboard');
      setCourses(data.courses || []);
      setTasks(data.pending_tasks || []);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setErrorMsg(error.message || 'No se pudo cargar el dashboard');
      setLoading(false);
    }
  };

  const handleCreateCourse = async (e) => {
    e.preventDefault();
    if (!newCourseName) return;

    try {
      const res = await fetch('/api/academic/courses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            user_id: USER_ID, 
            name: newCourseName, 
            professor: newCourseProf, 
            color: '#' + Math.floor(Math.random()*16777215).toString(16) 
        })
      });
      const data = await res.json();
      if (res.ok) {
        setIsCreating(false);
        setNewCourseName('');
        setNewCourseProf('');
        loadData(); // Recargar datos inmediatamente
      } else {
        alert(`Error al crear curso: ${data.error || 'Desconocido'}`);
      }
    } catch (error) {
      console.error(error);
      alert(`Error de conexión: ${error.message}`);
    }
  };

  const handleUpload = async (courseId, file) => {
    if (!file) return;
    setUploadingId(courseId);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', USER_ID);

    try {
      const res = await fetch(`/api/academic/course/${courseId}/upload-syllabus`, { method: 'POST', body: formData });
      const data = await res.json();
      if(res.ok) {
        alert(`✅ ${data.tasks_created} tareas creadas.`);
        loadData();
      } else {
        alert("Error: " + (data.error || 'No se pudo procesar el sílabo'));
      }
    } catch (e) { alert("Error de conexión"); }
    finally { setUploadingId(null); }
  };

  // Funcionalidad REAL: Eliminar Tarea
  const handleDeleteTask = async (taskId) => {
    if(window.confirm("¿Borrar esta tarea permanentemente?")) {
        try {
            await fetch(`/api/academic/task/${taskId}`, { method: 'DELETE' });
            setTasks(tasks.filter(t => t.id !== taskId)); // Actualizar UI optimista
        } catch (e) { alert("Error al borrar"); }
    }
  };

  // Funcionalidad REAL: Completar Tarea
  const handleToggleTask = async (taskId) => {
      // Actualización optimista UI
      setTasks(tasks.map(t => t.id === taskId ? {...t, status: t.status === 'completada' ? 'pendiente' : 'completada'} : t));
      
      try {
         await fetch(`/api/academic/task/${taskId}/toggle`, { method: 'PUT' });
      } catch(e) { console.error("Error actualizando tarea"); }
  };

  // Filtrar cursos por búsqueda
  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (course.professor && course.professor.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  // Filtrar tareas por búsqueda y filtros
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         task.course_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPriority = filterPriority === 'all' || task.priority === filterPriority;
    const matchesStatus = filterStatus === 'all' || task.status === filterStatus;
    
    return matchesSearch && matchesPriority && matchesStatus;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {errorMsg && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
          {errorMsg}
        </div>
      )}
      
      {/* Header mejorado */}
      <div className="mb-8 bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 flex items-center gap-3">
              <span className="text-5xl">📄</span> Nodo Digital
              <span className="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200 shadow-sm">
                MÓDULO 1
              </span>
            </h1>
            <p className="text-gray-500 mt-2 text-sm">Gestión inteligente de recursos académicos y análisis documental con IA</p>
          </div>
          
          {/* Barra de búsqueda global */}
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              placeholder="Buscar cursos o tareas..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            />
          </div>
        </div>
      </div>

      {/* Navegación Tabs mejorada con 6 pestañas */}
      <div className="flex gap-2 mb-8 bg-white rounded-xl shadow-sm p-2 border border-gray-200 overflow-x-auto">
        <button 
            onClick={() => setActiveTab('dashboard')} 
            className={`flex-1 min-w-[140px] py-3 px-4 font-semibold text-xs flex items-center justify-center gap-2 rounded-lg transition-all duration-200 ${activeTab === 'dashboard' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          <Calendar size={16} /> Gestión
        </button>
        <button 
            onClick={() => setActiveTab('tools')} 
            className={`flex-1 min-w-[140px] py-3 px-4 font-semibold text-xs flex items-center justify-center gap-2 rounded-lg transition-all duration-200 ${activeTab === 'tools' ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          <Brain size={16} /> Herramientas IA
        </button>
        <button 
            onClick={() => setActiveTab('timeline')} 
            className={`flex-1 min-w-[140px] py-3 px-4 font-semibold text-xs flex items-center justify-center gap-2 rounded-lg transition-all duration-200 ${activeTab === 'timeline' ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          <Calendar size={16} /> Línea Tiempo
        </button>
        <button 
            onClick={() => setActiveTab('syllabus')} 
            className={`flex-1 min-w-[140px] py-3 px-4 font-semibold text-xs flex items-center justify-center gap-2 rounded-lg transition-all duration-200 ${activeTab === 'syllabus' ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          <FileText size={16} /> Syllabus
        </button>
        <button 
            onClick={() => setActiveTab('projects')} 
            className={`flex-1 min-w-[140px] py-3 px-4 font-semibold text-xs flex items-center justify-center gap-2 rounded-lg transition-all duration-200 ${activeTab === 'projects' ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          <FolderOpen size={16} /> Proyectos
        </button>
        <button 
            onClick={() => setActiveTab('evolution')} 
            className={`flex-1 min-w-[140px] py-3 px-4 font-semibold text-xs flex items-center justify-center gap-2 rounded-lg transition-all duration-200 ${activeTab === 'evolution' ? 'bg-gradient-to-r from-teal-600 to-green-600 text-white shadow-md' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          <BarChart3 size={16} /> Evolución
        </button>
      </div>

      {activeTab === 'dashboard' ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* COLUMNA IZQUIERDA: CURSOS */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-bold text-gray-800">Mis Materias</h2>
              {!isCreating && (
                <button onClick={() => setIsCreating(true)} className="text-sm text-blue-600 font-medium hover:bg-blue-50 px-3 py-1 rounded-lg transition flex items-center gap-1">
                    <Plus size={16} /> Nueva Materia
                </button>
              )}
            </div>

            {/* Formulario de Creación Inline */}
            {isCreating && (
                <form onSubmit={handleCreateCourse} className="bg-blue-50 p-4 rounded-xl border border-blue-100 animate-in fade-in slide-in-from-top-2">
                    <div className="flex justify-between items-center mb-3">
                        <h3 className="text-sm font-bold text-blue-800">Nueva Materia</h3>
                        <button type="button" onClick={() => setIsCreating(false)} className="text-blue-400 hover:text-blue-600"><X size={16}/></button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                        <input 
                            autoFocus
                            type="text" placeholder="Nombre de la materia (Ej: Cálculo)" 
                            className="p-2 rounded border border-blue-200 text-sm outline-none focus:ring-2 focus:ring-blue-400"
                            value={newCourseName} onChange={e => setNewCourseName(e.target.value)}
                        />
                        <input 
                            type="text" placeholder="Profesor (Opcional)" 
                            className="p-2 rounded border border-blue-200 text-sm outline-none focus:ring-2 focus:ring-blue-400"
                            value={newCourseProf} onChange={e => setNewCourseProf(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded text-sm font-medium hover:bg-blue-700 transition">Guardar Materia</button>
                </form>
            )}

            {loading ? (
                <div className="text-center py-10 text-gray-400">Cargando...</div>
            ) : filteredCourses.length === 0 && !isCreating ? (
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center bg-white">
                    <BookOpen className="mx-auto text-gray-300 mb-2" size={48} />
                    <p className="text-gray-500 font-medium">
                      {searchTerm ? 'No se encontraron cursos' : 'No hay materias registradas'}
                    </p>
                    {!searchTerm && (
                      <button onClick={() => setIsCreating(true)} className="mt-4 text-blue-600 font-medium hover:underline">
                        Crear mi primera materia
                      </button>
                    )}
                </div>
            ) : (
                <div className="grid md:grid-cols-2 gap-4">
                    {filteredCourses.map(c => (
                        <div key={c.id} className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition group relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-1 h-full" style={{ backgroundColor: c.color || '#3B82F6' }}></div>
                            <h3 className="font-bold text-gray-800">{c.name}</h3>
                            <p className="text-sm text-gray-500 mb-4">{c.professor || 'Sin profesor'}</p>
                            
                            <div className="mt-auto pt-4 border-t border-gray-50">
                                {uploadingId === c.id ? (
                                    <div className="text-xs text-blue-600 flex items-center gap-2">
                                        <RefreshCw className="animate-spin" size={14} /> Analizando sílabo...
                                    </div>
                                ) : (
                                    <label className="flex items-center gap-2 text-xs text-gray-500 cursor-pointer hover:text-blue-600 transition">
                                        <Upload size={14} />
                                        <span>Subir Sílabo (PDF)</span>
                                        <input type="file" className="hidden" accept=".pdf" onChange={(e) => handleUpload(c.id, e.target.files[0])} />
                                    </label>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
          </div>

          {/* COLUMNA DERECHA: TAREAS */}
          <div>
             <div className="flex items-center justify-between mb-4">
               <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                  <Clock size={18} className="text-gray-400" /> Próximas Entregas
               </h2>
               <div className="flex gap-2">
                 <select
                   value={filterPriority}
                   onChange={(e) => setFilterPriority(e.target.value)}
                   className="text-xs px-2 py-1 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                 >
                   <option value="all">Todas</option>
                   <option value="critica">Crítica</option>
                   <option value="alta">Alta</option>
                   <option value="media">Media</option>
                   <option value="baja">Baja</option>
                 </select>
                 <select
                   value={filterStatus}
                   onChange={(e) => setFilterStatus(e.target.value)}
                   className="text-xs px-2 py-1 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                 >
                   <option value="all">Todos</option>
                   <option value="pendiente">Pendiente</option>
                   <option value="en_progreso">En progreso</option>
                   <option value="completada">Completada</option>
                 </select>
               </div>
             </div>
             <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 min-h-[300px]">
                {filteredTasks.length === 0 ? (
                    <div className="text-center py-10 text-gray-400">
                        <CheckCircle size={32} className="mx-auto mb-2 opacity-20" />
                        <p className="text-xs">
                          {searchTerm || filterPriority !== 'all' || filterStatus !== 'all' 
                            ? 'No hay tareas que coincidan con los filtros' 
                            : 'No hay tareas pendientes'}
                        </p>
                    </div>
                ) : (
                    <div className="space-y-3">
                        {filteredTasks.map(task => {
                          const priorityColors = {
                            critica: 'bg-red-50 border-red-200 text-red-700',
                            alta: 'bg-orange-50 border-orange-200 text-orange-700',
                            media: 'bg-yellow-50 border-yellow-200 text-yellow-700',
                            baja: 'bg-green-50 border-green-200 text-green-700'
                          };
                          
                          return (
                            <div key={task.id} className={`p-3 rounded-lg border transition flex gap-3 group ${task.status === 'completada' ? 'bg-gray-50 border-gray-100 opacity-60' : 'bg-white border-gray-100 hover:border-blue-200 shadow-sm'}`}>
                                <button onClick={() => handleToggleTask(task.id)} className="mt-1 text-gray-300 hover:text-blue-500 transition">
                                    {task.status === 'completada' ? <CheckSquare size={18} className="text-blue-500"/> : <Square size={18} />}
                                </button>
                                <div className="flex-1">
                                    <div className="flex items-start justify-between gap-2">
                                      <h4 className={`text-sm font-medium ${task.status === 'completada' ? 'text-gray-400 line-through' : 'text-gray-800'}`}>{task.title}</h4>
                                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${priorityColors[task.priority] || 'bg-gray-50 border-gray-200 text-gray-700'}`}>
                                        {task.priority.toUpperCase()}
                                      </span>
                                    </div>
                                    <p className="text-xs text-gray-500 mt-0.5">{task.course_name} • {new Date(task.due_date).toLocaleDateString()}</p>
                                    {task.origin === 'syllabus_ai' && <span className="inline-block mt-2 text-[10px] font-bold text-purple-600 bg-purple-50 px-1.5 py-0.5 rounded border border-purple-100">IA GENERADO</span>}
                                </div>
                                <button onClick={() => handleDeleteTask(task.id)} className="text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition">
                                    <Trash2 size={16} />
                                </button>
                            </div>
                          );
                        })}
                    </div>
                )}
             </div>
          </div>

        </div>
      ) : activeTab === 'tools' ? (
        <StudyTools />
      ) : activeTab === 'timeline' ? (
        /* 🆕 NUEVO: Creador de líneas de tiempo con IA y gestión completa */
        <TimelineCreator userId={USER_ID} />
      ) : activeTab === 'syllabus' ? (
        /* 🆕 NUEVO: Analizador de sílabos con historial y progreso */
        <SyllabusAnalyzerPro userId={USER_ID} />
      ) : activeTab === 'gestion' ? (
        /* 🆕 NUEVO: Gestor de cursos con iconos y categorías */
        <CourseManagerPro userId={USER_ID} />
      ) : activeTab === 'projects' ? (
        /* 🆕 NUEVO: Gestor de proyectos moderno con mensajes creativos y cronómetro mejorado */
        <ModernProjectManager userId={USER_ID} courses={courses} />
      ) : activeTab === 'evolution' ? (
        <EvolutionChart userId={USER_ID} courses={courses} />
      ) : null}
    </div>
  );
};

export default AcademicDashboard;