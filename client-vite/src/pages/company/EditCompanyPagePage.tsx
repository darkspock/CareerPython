import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Eye, EyeOff, Archive, Trash2, Star } from 'lucide-react';
import { WysiwygEditor } from '../../components/common';
import { companyPageService } from '../../services/companyPageService';
import type { CompanyPage, UpdateCompanyPageRequest } from '../../types/companyPage';
import { LANGUAGE_OPTIONS, PageStatus, getPageTypeLabel, normalizePageStatus, getPageStatusLabel, getPageStatusColor } from '../../types/companyPage';

export default function EditCompanyPagePage() {
  const navigate = useNavigate();
  const { pageId } = useParams<{ pageId: string }>();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewMode, setPreviewMode] = useState(false);
  const [page, setPage] = useState<CompanyPage | null>(null);

  const [formData, setFormData] = useState<UpdateCompanyPageRequest>({
    title: '',
    html_content: '',
    meta_description: '',
    meta_keywords: [],
    language: 'es',
    is_default: false,
  });

  const [keywordInput, setKeywordInput] = useState('');

  useEffect(() => {
    if (pageId) {
      loadPage();
    }
  }, [pageId]);

  const loadPage = async () => {
    if (!pageId) return;

    try {
      setLoading(true);
      setError(null);
      
      const pageData = await companyPageService.getPageById(pageId);
      setPage(pageData);
      setFormData({
        title: pageData.title,
        html_content: pageData.html_content,
        meta_description: pageData.meta_description || '',
        meta_keywords: pageData.meta_keywords || [],
        language: pageData.language,
        is_default: pageData.is_default,
      });
    } catch (err: any) {
      setError(err.message || 'Error al cargar la página');
      console.error('Error loading page:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!pageId) return;
    if (!formData.title?.trim()) {
      setError('El título es obligatorio');
      return;
    }
    if (!formData.html_content?.trim()) {
      setError('El contenido es obligatorio');
      return;
    }

    try {
      setSaving(true);
      setError(null);

      await companyPageService.updatePage(pageId, formData);
      navigate('/company/pages');
    } catch (err: any) {
      setError(err.message || 'Error al actualizar la página');
      console.error('Error updating page:', err);
    } finally {
      setSaving(false);
    }
  };

  const handlePublish = async () => {
    if (!pageId) return;

    try {
      setSaving(true);
      setError(null);
      await companyPageService.publishPage(pageId);
      await loadPage(); // Reload to get updated status
    } catch (err: any) {
      setError(err.message || 'Error al publicar la página');
    } finally {
      setSaving(false);
    }
  };

  const handleArchive = async () => {
    if (!pageId) return;

    try {
      setSaving(true);
      setError(null);
      await companyPageService.archivePage(pageId);
      await loadPage(); // Reload to get updated status
    } catch (err: any) {
      setError(err.message || 'Error al archivar la página');
    } finally {
      setSaving(false);
    }
  };

  const handleSetDefault = async () => {
    if (!pageId) return;

    try {
      setSaving(true);
      setError(null);
      await companyPageService.setDefaultPage(pageId);
      await loadPage(); // Reload to get updated status
    } catch (err: any) {
      setError(err.message || 'Error al establecer como página por defecto');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!pageId) return;

    if (window.confirm('¿Estás seguro de que quieres eliminar esta página? Esta acción no se puede deshacer.')) {
      try {
        setSaving(true);
        setError(null);
        await companyPageService.deletePage(pageId);
        navigate('/company/pages');
      } catch (err: any) {
        setError(err.message || 'Error al eliminar la página');
      } finally {
        setSaving(false);
      }
    }
  };

  const handleAddKeyword = () => {
    if (keywordInput.trim() && !formData.meta_keywords?.includes(keywordInput.trim())) {
      setFormData(prev => ({
        ...prev,
        meta_keywords: [...(prev.meta_keywords || []), keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const handleRemoveKeyword = (keyword: string) => {
    setFormData(prev => ({
      ...prev,
      meta_keywords: prev.meta_keywords?.filter(k => k !== keyword) || []
    }));
  };

  const handleKeywordKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddKeyword();
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-gray-600 mt-2">Cargando página...</p>
        </div>
      </div>
    );
  }

  if (!page) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Página no encontrada</h3>
        <p className="text-gray-600 mb-4">La página que buscas no existe o ha sido eliminada.</p>
        <button
          onClick={() => navigate('/company/pages')}
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Volver a Páginas
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/company/pages')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="w-5 h-5" />
            Volver
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Editar Página</h1>
            <p className="text-gray-600 mt-1">{page.title}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPreviewMode(!previewMode)}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            {previewMode ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            {previewMode ? 'Editar' : 'Vista Previa'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Información Básica</h2>
              
              <div className="space-y-4">
                {/* Page Type (Read-only) */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de Página
                  </label>
                  <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-gray-600">
                    {getPageTypeLabel(page.page_type)}
                  </div>
                </div>

                {/* Title */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Título <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.title || ''}
                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Título de la página"
                    required
                  />
                </div>

                {/* Language */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Idioma
                  </label>
                  <select
                    value={formData.language || 'es'}
                    onChange={(e) => setFormData(prev => ({ ...prev, language: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    {LANGUAGE_OPTIONS.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Default Page */}
                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    id="is_default"
                    checked={formData.is_default || false}
                    onChange={(e) => setFormData(prev => ({ ...prev, is_default: e.target.checked }))}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  <label htmlFor="is_default" className="text-sm font-medium text-gray-700">
                    Marcar como página por defecto para este tipo
                  </label>
                </div>
              </div>
            </div>

            {/* Content Editor */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Contenido</h2>
              
              {previewMode ? (
                <div 
                  className="prose max-w-none min-h-[400px] p-4 border border-gray-200 rounded-lg bg-gray-50"
                  dangerouslySetInnerHTML={{ __html: formData.html_content || '<p class="text-gray-500 italic">No hay contenido para mostrar</p>' }}
                />
              ) : (
                <WysiwygEditor
                  value={formData.html_content || ''}
                  onChange={(content) => setFormData(prev => ({ ...prev, html_content: content }))}
                  placeholder="Escribe el contenido de tu página aquí..."
                  height={400}
                />
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Page Status */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Estado de la Página</h3>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Estado:</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPageStatusColor(page.status)}`}>
                    {getPageStatusLabel(page.status)}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Versión:</span>
                  <span className="text-sm font-medium">{page.version}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Palabras:</span>
                  <span className="text-sm font-medium">{page.word_count}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Creado:</span>
                  <span className="text-sm font-medium">
                    {new Date(page.created_at).toLocaleDateString('es-ES')}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Actualizado:</span>
                  <span className="text-sm font-medium">
                    {new Date(page.updated_at).toLocaleDateString('es-ES')}
                  </span>
                </div>
              </div>
            </div>

            {/* SEO Settings */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Configuración SEO</h3>
              
              <div className="space-y-4">
                {/* Meta Description */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Meta Descripción
                  </label>
                  <textarea
                    value={formData.meta_description || ''}
                    onChange={(e) => setFormData(prev => ({ ...prev, meta_description: e.target.value }))}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Description for search engines (max 160 characters)"
                    maxLength={160}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    {(formData.meta_description || '').length}/160 caracteres
                  </p>
                </div>

                {/* Keywords */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Keywords
                  </label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      value={keywordInput}
                      onChange={(e) => setKeywordInput(e.target.value)}
                      onKeyPress={handleKeywordKeyPress}
                      placeholder="Agregar palabra clave"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <button
                      type="button"
                      onClick={handleAddKeyword}
                      className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Agregar
                    </button>
                  </div>
                  
                  {formData.meta_keywords && formData.meta_keywords.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {formData.meta_keywords.map((keyword, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                        >
                          {keyword}
                          <button
                            type="button"
                            onClick={() => handleRemoveKeyword(keyword)}
                            className="text-blue-600 hover:text-blue-800"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
              
              <div className="space-y-3">
                <button
                  type="submit"
                  disabled={saving}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Save className="w-5 h-5" />
                  {saving ? 'Guardando...' : 'Guardar Cambios'}
                </button>

                {normalizePageStatus(page.status) === PageStatus.DRAFT && (
                  <button
                    type="button"
                    onClick={handlePublish}
                    disabled={saving}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Publicar
                  </button>
                )}

                {normalizePageStatus(page.status) === PageStatus.PUBLISHED && (
                  <button
                    type="button"
                    onClick={handleArchive}
                    disabled={saving}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Archive className="w-5 h-5" />
                    Archivar
                  </button>
                )}

                {page.status === PageStatus.PUBLISHED && !page.is_default && (
                  <button
                    type="button"
                    onClick={handleSetDefault}
                    disabled={saving}
                    className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Star className="w-5 h-5" />
                    Establecer como Defecto
                  </button>
                )}
                
                <button
                  type="button"
                  onClick={() => navigate('/company/pages')}
                  className="w-full px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={handleDelete}
                  disabled={saving}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Trash2 className="w-5 h-5" />
                  Eliminar Página
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
