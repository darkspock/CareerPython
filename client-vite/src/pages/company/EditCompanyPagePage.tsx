import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { ArrowLeft, Save, Eye, EyeOff, Archive, Trash2, Star } from 'lucide-react';
import { WysiwygEditor } from '../../components/common';
import { companyPageService } from '../../services/companyPageService';
import type { CompanyPage, UpdateCompanyPageRequest } from '../../types/companyPage';
import { LANGUAGE_OPTIONS, PageStatus, getPageTypeLabel, normalizePageStatus, getPageStatusLabel, getPageStatusColor } from '../../types/companyPage';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';

export default function EditCompanyPagePage() {
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
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
      navigate(getPath('pages'));
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
        navigate(getPath('pages'));
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
        <Button onClick={() => navigate(getPath('pages'))}>
          <ArrowLeft className="w-5 h-5 mr-2" />
          Volver a Páginas
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            onClick={() => navigate(getPath('pages'))}
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Volver
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Editar Página</h1>
            <p className="text-gray-600 mt-1">{page.title}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            onClick={() => setPreviewMode(!previewMode)}
          >
            {previewMode ? <EyeOff className="w-5 h-5 mr-2" /> : <Eye className="w-5 h-5 mr-2" />}
            {previewMode ? 'Editar' : 'Vista Previa'}
          </Button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Basic Information */}
            <Card>
              <CardHeader>
                <CardTitle>Información Básica</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Page Type (Read-only) */}
                <div>
                  <Label htmlFor="page_type">Tipo de Página</Label>
                  <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg text-gray-600">
                    {getPageTypeLabel(page.page_type)}
                  </div>
                </div>

                {/* Title */}
                <div>
                  <Label htmlFor="title">
                    Título <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="title"
                    type="text"
                    value={formData.title || ''}
                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                    placeholder="Título de la página"
                    required
                  />
                </div>

                {/* Language */}
                <div>
                  <Label htmlFor="language">Idioma</Label>
                  <Select
                    value={formData.language || 'es'}
                    onValueChange={(value) => setFormData(prev => ({ ...prev, language: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {LANGUAGE_OPTIONS.map(option => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Default Page */}
                <div className="flex items-center gap-3">
                  <Checkbox
                    id="is_default"
                    checked={formData.is_default || false}
                    onCheckedChange={(checked) => setFormData(prev => ({ ...prev, is_default: checked as boolean }))}
                  />
                  <Label htmlFor="is_default" className="text-sm font-medium cursor-pointer">
                    Marcar como página por defecto para este tipo
                  </Label>
                </div>
              </CardContent>
            </Card>

            {/* Content Editor */}
            <Card>
              <CardHeader>
                <CardTitle>Contenido</CardTitle>
              </CardHeader>
              <CardContent>
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
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Page Status */}
            <Card>
              <CardHeader>
                <CardTitle>Estado de la Página</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Estado:</span>
                  <Badge className={getPageStatusColor(page.status)}>
                    {getPageStatusLabel(page.status)}
                  </Badge>
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
              </CardContent>
            </Card>

            {/* SEO Settings */}
            <Card>
              <CardHeader>
                <CardTitle>Configuración SEO</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Meta Description */}
                <div>
                  <Label htmlFor="meta_description">Meta Descripción</Label>
                  <Textarea
                    id="meta_description"
                    value={formData.meta_description || ''}
                    onChange={(e) => setFormData(prev => ({ ...prev, meta_description: e.target.value }))}
                    rows={3}
                    placeholder="Description for search engines (max 160 characters)"
                    maxLength={160}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    {(formData.meta_description || '').length}/160 caracteres
                  </p>
                </div>

                {/* Keywords */}
                <div>
                  <Label htmlFor="keywords">Keywords</Label>
                  <div className="flex gap-2 mb-2">
                    <Input
                      id="keywords"
                      type="text"
                      value={keywordInput}
                      onChange={(e) => setKeywordInput(e.target.value)}
                      onKeyPress={handleKeywordKeyPress}
                      placeholder="Agregar palabra clave"
                      className="flex-1"
                    />
                    <Button
                      type="button"
                      onClick={handleAddKeyword}
                      size="sm"
                    >
                      Agregar
                    </Button>
                  </div>

                  {formData.meta_keywords && formData.meta_keywords.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {formData.meta_keywords.map((keyword, index) => (
                        <Badge key={index} variant="secondary" className="gap-1">
                          {keyword}
                          <button
                            type="button"
                            onClick={() => handleRemoveKeyword(keyword)}
                            className="text-blue-600 hover:text-blue-800"
                          >
                            ×
                          </button>
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  type="submit"
                  disabled={saving}
                  className="w-full"
                >
                  <Save className="w-5 h-5 mr-2" />
                  {saving ? 'Guardando...' : 'Guardar Cambios'}
                </Button>

                {normalizePageStatus(page.status) === PageStatus.DRAFT && (
                  <Button
                    type="button"
                    onClick={handlePublish}
                    disabled={saving}
                    className="w-full bg-green-600 hover:bg-green-700"
                  >
                    Publicar
                  </Button>
                )}

                {normalizePageStatus(page.status) === PageStatus.PUBLISHED && (
                  <Button
                    type="button"
                    onClick={handleArchive}
                    disabled={saving}
                    className="w-full bg-orange-600 hover:bg-orange-700"
                  >
                    <Archive className="w-5 h-5 mr-2" />
                    Archivar
                  </Button>
                )}

                {page.status === PageStatus.PUBLISHED && !page.is_default && (
                  <Button
                    type="button"
                    onClick={handleSetDefault}
                    disabled={saving}
                    className="w-full bg-yellow-600 hover:bg-yellow-700"
                  >
                    <Star className="w-5 h-5 mr-2" />
                    Establecer como Defecto
                  </Button>
                )}

                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate(getPath('pages'))}
                  className="w-full"
                >
                  Cancel
                </Button>

                <Button
                  type="button"
                  onClick={handleDelete}
                  disabled={saving}
                  variant="destructive"
                  className="w-full"
                >
                  <Trash2 className="w-5 h-5 mr-2" />
                  Eliminar Página
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </form>
    </div>
  );
}
