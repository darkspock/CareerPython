import React from 'react';
import { Edit3, Eye, Archive, Trash2, Star, FileText, Globe, GlobeLock } from 'lucide-react';
import type { CompanyPage } from '../../types/companyPage';
import { PageStatus, PageType, getPageTypeLabel, getPageStatusLabel, getPageStatusColor, normalizePageStatus } from '../../types/companyPage';
import '../../components/common/WysiwygEditor.css';

interface CompanyPageCardProps {
  page: CompanyPage;
  onEdit: (pageId: string) => void;
  onView: (pageId: string) => void;
  onPublish: (pageId: string) => void;
  onArchive: (pageId: string) => void;
  onDelete: (pageId: string) => void;
  onSetDefault: (pageId: string) => void;
}

export const CompanyPageCard: React.FC<CompanyPageCardProps> = ({
  page,
  onEdit,
  onView,
  onPublish,
  onArchive,
  onDelete,
  onSetDefault,
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Determine which actions are available based on current status
  // Normalize status to handle both key and value formats
  const normalizedStatus = normalizePageStatus(page.status);
  const canPublish = normalizedStatus === PageStatus.DRAFT;
  const canArchive = normalizedStatus === PageStatus.PUBLISHED;
  const canSetDefault = normalizedStatus === PageStatus.PUBLISHED && !page.is_default;
  const isArchived = normalizedStatus === PageStatus.ARCHIVED;
  const isPublished = normalizedStatus === PageStatus.PUBLISHED;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="mb-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <FileText className="w-5 h-5 text-gray-500 flex-shrink-0" />
            <h3 className="text-lg font-semibold text-gray-900 truncate">{page.title}</h3>
            {page.is_default && (
              <Star className="w-4 h-4 text-yellow-500 fill-current flex-shrink-0" />
            )}
          </div>
          <div className="flex items-center gap-2 ml-2 flex-shrink-0">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPageStatusColor(page.status)}`}
              title={`Estado: ${getPageStatusLabel(page.status)}`}
            >
              {getPageStatusLabel(page.status)}
            </span>
          </div>
        </div>
        <div className="w-full">
          <p className="text-xs text-gray-500 mb-2">{getPageTypeLabel(page.page_type)}</p>
        </div>
      </div>

      {/* Content Preview */}
      <div className="mb-4">
        {page.html_content ? (
          <div 
            className="prose prose-sm max-w-none wysiwyg-content"
            style={{
              maxHeight: '180px',
              overflow: 'hidden',
              position: 'relative'
            }}
          >
            <div 
              className="ProseMirror"
              style={{
                marginBottom: 0,
                minHeight: 'auto',
                fontSize: '0.875rem',
                lineHeight: '1.5'
              }}
              dangerouslySetInnerHTML={{ __html: page.html_content }}
            />
            <div 
              className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-white to-transparent pointer-events-none"
            />
          </div>
        ) : (
          <p className="text-sm text-gray-700 line-clamp-3">
            {page.plain_text || 'Sin contenido...'}
          </p>
        )}
        {page.meta_description && (
          <p className="text-xs text-gray-500 mt-2 italic">
            SEO: {page.meta_description}
          </p>
        )}
      </div>

      {/* Meta Information */}
      <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-4">
            <span>Version {page.version}</span>
            <span>•</span>
            <span>{page.word_count} words</span>
            <span>•</span>
            <span>{page.language.toUpperCase()}</span>
          </div>
          <div className="flex items-center gap-4">
            <span>Creado: {formatDate(page.created_at)}</span>
            <span>Actualizado: {formatDate(page.updated_at)}</span>
            {page.published_at && (
              <span>Publicado: {formatDate(page.published_at)}</span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-1">
          {page.meta_keywords.length > 0 && (
            <span className="flex items-center gap-1">
              <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
              {page.meta_keywords.length} keywords
            </span>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <div className="flex items-center gap-2">
          <button
            onClick={() => onView(page.id)}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-md transition-colors group relative"
            title="Ver página"
          >
            <Eye className="w-5 h-5" />
            <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
              Ver página
            </span>
          </button>
          <button
            onClick={() => onEdit(page.id)}
            className="p-2 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors group relative"
            title="Editar página"
          >
            <Edit3 className="w-5 h-5" />
            <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
              Editar página
            </span>
          </button>
        </div>

        <div className="flex items-center gap-1 flex-wrap">
          {/* Status change buttons */}
          {canPublish && (
            <button
              onClick={() => onPublish(page.id)}
              className="p-2 text-green-600 hover:text-green-800 hover:bg-green-50 rounded-md transition-colors group relative"
              title="Publicar página (cambia de Borrador a Publicado)"
            >
              <Globe className="w-5 h-5" />
              <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                Publicar
              </span>
            </button>
          )}
          
          {canArchive && (
            <button
              onClick={() => onArchive(page.id)}
              className="p-2 text-orange-600 hover:text-orange-800 hover:bg-orange-50 rounded-md transition-colors group relative"
              title="Archivar página (cambia de Publicado a Archivado)"
            >
              <Archive className="w-5 h-5" />
              <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                Archivar
              </span>
            </button>
          )}
          
          {canSetDefault && (
            <button
              onClick={() => onSetDefault(page.id)}
              className="p-2 text-yellow-600 hover:text-yellow-800 hover:bg-yellow-50 rounded-md transition-colors group relative"
              title="Establecer como página por defecto"
            >
              <Star className="w-5 h-5" />
              <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                Establecer por defecto
              </span>
            </button>
          )}
          
          <button
            onClick={() => onDelete(page.id)}
            className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md transition-colors group relative"
            title="Eliminar página permanentemente"
          >
            <Trash2 className="w-5 h-5" />
            <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs text-white bg-gray-900 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
              Eliminar
            </span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompanyPageCard;
