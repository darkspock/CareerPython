/**
 * Resume Editor Component
 *
 * Main editor interface that combines section management, WYSIWYG editing,
 * and real-time preview functionality for comprehensive resume editing.
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Save,
  Eye,
  EyeOff,
  ArrowLeft,
  RotateCcw,
  Clock,
  AlertCircle
} from 'lucide-react';
import ResumePreview from './ResumePreview';
import { api } from '../../../lib/api';

interface ResumeData {
  id: string;
  name: string;
  resume_type: string;
  status: string;
  ai_enhancement_status: string;
  content: {
    experiencia_profesional: string;
    educacion: string;
    proyectos: string;
    habilidades: string;
    datos_personales: {
      name: string;
      email: string;
      phone: string;
      location: string;
      linkedin_url?: string;
    };
  };
  formatting_preferences: {
    template: string;
    color_scheme: string;
    font_family: string;
    include_photo: boolean;
    sections_order: string[];
  };
  created_at: string;
  updated_at: string;
}

interface ResumeEditorProps {
  resumeId: string;
  onBack?: () => void;
  onSave?: (resumeData: ResumeData) => void;
  className?: string;
}

const ResumeEditor: React.FC<ResumeEditorProps> = ({
  resumeId,
  onBack,
  onSave,
  className = ''
}) => {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);

  const saveTimeoutRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const initialDataRef = useRef<string>('');

  // Load resume data
  useEffect(() => {
    loadResumeData();
  }, [resumeId]);

  // Auto-save functionality
  useEffect(() => {
    if (hasUnsavedChanges && resumeData) {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }

      saveTimeoutRef.current = setTimeout(() => {
        handleAutoSave();
      }, 2000); // Auto-save after 2 seconds of inactivity
    }

    return () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, [hasUnsavedChanges, resumeData]);

  const loadResumeData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load resume data from API
      const data = await api.getResume(resumeId) as ResumeData;

      setResumeData(data);
      initialDataRef.current = JSON.stringify(data);
      setHasUnsavedChanges(false);
    } catch (error) {
      console.error('Error loading resume:', error);
      setError('Failed to load resume data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAutoSave = async () => {
    if (!resumeData || saving) return;

    try {
      setSaving(true);
      await saveResumeData(false);
    } catch (error) {
      console.error('Auto-save failed:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleManualSave = async () => {
    if (!resumeData || saving) return;

    try {
      setSaving(true);
      await saveResumeData(true);
    } catch (error) {
      setError('Failed to save resume. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const saveResumeData = async (isManual: boolean = false) => {
    if (!resumeData) return;

    try {
      const saveData = {
        experiencia_profesional: resumeData.content.experiencia_profesional,
        educacion: resumeData.content.educacion,
        proyectos: resumeData.content.proyectos,
        habilidades: resumeData.content.habilidades,
        datos_personales: resumeData.content.datos_personales,
        preserve_ai_content: true
      };

      await api.updateResumeContent(resumeId, saveData);

      setHasUnsavedChanges(false);
      setLastSaved(new Date());

      if (isManual) {
        onSave?.(resumeData);
      }
    } catch (error) {
      throw error;
    }
  };

  const handleDataChange = (newData: Partial<ResumeData>) => {
    if (!resumeData) return;

    const updatedData = { ...resumeData, ...newData };
    setResumeData(updatedData);

    const currentDataString = JSON.stringify(updatedData);
    setHasUnsavedChanges(currentDataString !== initialDataRef.current);
  };

  const handleContentChange = (field: keyof ResumeData['content'], value: string) => {
    if (!resumeData) return;

    const updatedContent = {
      ...resumeData.content,
      [field]: value
    };

    handleDataChange({ content: updatedContent });
  };

  const handlePersonalDataChange = (field: keyof ResumeData['content']['datos_personales'], value: string) => {
    if (!resumeData) return;

    const updatedDatosPersonales = {
      ...resumeData.content.datos_personales,
      [field]: value
    };

    const updatedContent = {
      ...resumeData.content,
      datos_personales: updatedDatosPersonales
    };

    handleDataChange({ content: updatedContent });
  };

  const handleTemplateChange = (template: string) => {
    if (!resumeData) return;

    const updatedFormatting = {
      ...resumeData.formatting_preferences,
      template
    };

    handleDataChange({ formatting_preferences: updatedFormatting });
  };

  const handleRevertChanges = () => {
    if (initialDataRef.current) {
      const originalData = JSON.parse(initialDataRef.current);
      setResumeData(originalData);
      setHasUnsavedChanges(false);
    }
  };

  const handleExport = async () => {
    if (!resumeData) return;

    try {
      // Save current changes before exporting
      if (hasUnsavedChanges) {
        await saveResumeData();
      }

      // Navigate to export page
      window.open(`/candidate/profile/resumes/${resumeId}/export`, '_blank');
    } catch (error) {
      setError('Failed to export resume. Please try again.');
    }
  };

  const handleShare = () => {
    // Copy resume preview link to clipboard
    const shareUrl = `${window.location.origin}/candidate/profile/resumes/${resumeId}/preview`;
    navigator.clipboard.writeText(shareUrl);
    // You could add a toast notification here
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading resume editor...</p>
        </div>
      </div>
    );
  }

  if (error || !resumeData) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error || 'Resume not found'}</p>
          <button
            onClick={loadResumeData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen bg-gray-50 ${className}`}>
      {/* Editor Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Left side */}
            <div className="flex items-center gap-4">
              {onBack && (
                <button
                  onClick={onBack}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                >
                  <ArrowLeft className="w-5 h-5" />
                </button>
              )}

              <div>
                <h1 className="text-lg font-semibold text-gray-900">{resumeData.name}</h1>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span className="capitalize">{resumeData.resume_type.toLowerCase()} • {resumeData.status}</span>
                  {lastSaved && (
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      Last saved: {lastSaved.toLocaleTimeString()}
                    </div>
                  )}
                  {hasUnsavedChanges && (
                    <span className="text-orange-600">Unsaved changes</span>
                  )}
                  {saving && (
                    <div className="flex items-center gap-1">
                      <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600"></div>
                      Saving...
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className={`p-2 rounded-lg transition-colors ${
                  showPreview ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                }`}
                title={showPreview ? 'Hide Preview' : 'Show Preview'}
              >
                {showPreview ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>

              {hasUnsavedChanges && (
                <button
                  onClick={handleRevertChanges}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                  title="Revert Changes"
                >
                  <RotateCcw className="w-5 h-5" />
                </button>
              )}

              <button
                onClick={handleManualSave}
                disabled={saving || !hasUnsavedChanges}
                className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Save className="w-4 h-4 mr-2" />
                {saving ? 'Saving...' : 'Save'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Editor Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className={`grid gap-8 ${showPreview ? 'lg:grid-cols-2' : 'grid-cols-1'}`}>
          {/* Editor Panel */}
          <div className="space-y-6">
            {/* Datos Personales */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Datos Personales</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre Completo
                  </label>
                  <input
                    type="text"
                    value={resumeData.content.datos_personales.name || ''}
                    onChange={(e) => handlePersonalDataChange('name', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    value={resumeData.content.datos_personales.email || ''}
                    onChange={(e) => handlePersonalDataChange('email', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Teléfono
                  </label>
                  <input
                    type="tel"
                    value={resumeData.content.datos_personales.phone || ''}
                    onChange={(e) => handlePersonalDataChange('phone', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Ubicación
                  </label>
                  <input
                    type="text"
                    value={resumeData.content.datos_personales.location || ''}
                    onChange={(e) => handlePersonalDataChange('location', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Ciudad, País"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    LinkedIn URL
                  </label>
                  <input
                    type="url"
                    value={resumeData.content.datos_personales.linkedin_url || ''}
                    onChange={(e) => handlePersonalDataChange('linkedin_url', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="https://linkedin.com/in/tu-perfil"
                  />
                </div>
              </div>
            </div>

            {/* Experiencia Profesional */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Experiencia Profesional</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Contenido (Markdown)
                </label>
                <textarea
                  value={resumeData.content.experiencia_profesional}
                  onChange={(e) => handleContentChange('experiencia_profesional', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  rows={8}
                  placeholder="### Cargo\n**Empresa**\n*Fechas*\n\nDescripción del puesto..."
                />
                <p className="text-xs text-gray-500 mt-1">
                  Usa Markdown para formatear: ### para títulos, **texto** para negrita, *texto* para cursiva
                </p>
              </div>
            </div>

            {/* Educación */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Educación</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Contenido (Markdown)
                </label>
                <textarea
                  value={resumeData.content.educacion}
                  onChange={(e) => handleContentChange('educacion', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  rows={6}
                  placeholder="### Título\n**Institución**\n*Fechas*\n\nDescripción..."
                />
                <p className="text-xs text-gray-500 mt-1">
                  Usa Markdown para formatear: ### para títulos, **texto** para negrita, *texto* para cursiva
                </p>
              </div>
            </div>

            {/* Habilidades */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Habilidades</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Contenido (Markdown)
                </label>
                <textarea
                  value={resumeData.content.habilidades}
                  onChange={(e) => handleContentChange('habilidades', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  rows={4}
                  placeholder="- Habilidad 1\n- Habilidad 2\n- Habilidad 3"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Usa listas con - para cada habilidad
                </p>
              </div>
            </div>

            {/* Proyectos */}
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Proyectos</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Contenido (Markdown)
                </label>
                <textarea
                  value={resumeData.content.proyectos}
                  onChange={(e) => handleContentChange('proyectos', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                  rows={6}
                  placeholder="### Nombre del Proyecto\n*Fechas*\n\n**URL:** https://proyecto.com\n\nDescripción del proyecto...\n\n**Tecnologías:** React, Node.js, MongoDB"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Usa Markdown para formatear: ### para títulos, **texto** para negrita, *texto* para cursiva
                </p>
              </div>
            </div>
          </div>

          {/* Preview Panel */}
          {showPreview && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="lg:sticky lg:top-24 lg:h-fit"
            >
              <ResumePreview
                resumeData={resumeData as any}
                template={(resumeData.formatting_preferences?.template as 'professional' | 'modern' | 'minimal' | 'creative') || 'professional'}
                onTemplateChange={handleTemplateChange}
                onExport={handleExport}
                onShare={handleShare}
              />
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResumeEditor;