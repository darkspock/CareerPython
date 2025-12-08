import React from 'react';
import { Edit3, Eye, Archive, Trash2, Star, FileText, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { CompanyPage } from '../../types/companyPage';
import { PageStatus, getPageTypeLabel, getPageStatusLabel, getPageStatusColor, normalizePageStatus } from '../../types/companyPage';
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

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        {/* Header */}
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            <FileText className="w-5 h-5 text-gray-500 flex-shrink-0" />
            <CardTitle className="text-lg truncate">{page.title}</CardTitle>
            {page.is_default && (
              <Star className="w-4 h-4 text-yellow-500 fill-current flex-shrink-0" />
            )}
          </div>
          <Badge className={getPageStatusColor(page.status)}>
            {getPageStatusLabel(page.status)}
          </Badge>
        </div>
        <div className="w-full">
          <p className="text-xs text-gray-500 mb-2">{getPageTypeLabel(page.page_type)}</p>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Content Preview */}
        <div>
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
        <div className="flex items-center justify-between text-xs text-gray-500">
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
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onView(page.id)}
              title="Ver página"
            >
              <Eye className="w-5 h-5" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onEdit(page.id)}
              title="Editar página"
            >
              <Edit3 className="w-5 h-5" />
            </Button>
          </div>

          <div className="flex items-center gap-1 flex-wrap">
            {/* Status change buttons */}
            {canPublish && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onPublish(page.id)}
                title="Publicar página (cambia de Borrador a Publicado)"
                className="text-green-600 hover:text-green-800 hover:bg-green-50"
              >
                <Globe className="w-5 h-5" />
              </Button>
            )}

            {canArchive && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onArchive(page.id)}
                title="Archivar página (cambia de Publicado a Archivado)"
                className="text-orange-600 hover:text-orange-800 hover:bg-orange-50"
              >
                <Archive className="w-5 h-5" />
              </Button>
            )}

            {canSetDefault && (
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onSetDefault(page.id)}
                title="Establecer como página por defecto"
                className="text-yellow-600 hover:text-yellow-800 hover:bg-yellow-50"
              >
                <Star className="w-5 h-5" />
              </Button>
            )}

            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDelete(page.id)}
              title="Eliminar página permanentemente"
              className="text-red-600 hover:text-red-800 hover:bg-red-50"
            >
              <Trash2 className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CompanyPageCard;
