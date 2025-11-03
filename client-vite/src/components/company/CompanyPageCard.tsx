import React from 'react';
import { Edit3, Eye, Archive, Trash2, Star, FileText } from 'lucide-react';
import type { CompanyPage } from '../../types/companyPage';
import { PageStatus, PageType } from '../../types/companyPage';
import { PAGE_STATUS_OPTIONS, PAGE_TYPE_OPTIONS } from '../../types/companyPage';

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
  const getStatusColor = (status: keyof typeof PageStatus) => {
    const statusValue = PageStatus[status];
    const statusOption = PAGE_STATUS_OPTIONS.find(opt => opt.value === statusValue);
    return statusOption?.color || 'gray';
  };

  const getPageTypeLabel = (pageType: keyof typeof PageType) => {
    const typeValue = PageType[pageType];
    const typeOption = PAGE_TYPE_OPTIONS.find(opt => opt.value === typeValue);
    return typeOption?.label || pageType;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const canPublish = PageStatus[page.status] === PageStatus.DRAFT;
  const canArchive = PageStatus[page.status] === PageStatus.PUBLISHED;
  const canSetDefault = PageStatus[page.status] === PageStatus.PUBLISHED && !page.is_default;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <FileText className="w-5 h-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">{page.title}</h3>
            {page.is_default && (
              <Star className="w-4 h-4 text-yellow-500 fill-current" />
            )}
          </div>
          <p className="text-sm text-gray-600 mb-2">{getPageTypeLabel(page.page_type)}</p>
          <div className="flex items-center gap-4 text-xs text-gray-500">
            <span>Version {page.version}</span>
            <span>•</span>
            <span>{page.word_count} words</span>
            <span>•</span>
            <span>{page.language.toUpperCase()}</span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              getStatusColor(page.status) === 'green'
                ? 'bg-green-100 text-green-800'
                : getStatusColor(page.status) === 'red'
                ? 'bg-red-100 text-red-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {PAGE_STATUS_OPTIONS.find(opt => opt.value === PageStatus[page.status])?.label}
          </span>
        </div>
      </div>

      {/* Content Preview */}
      <div className="mb-4">
        <p className="text-sm text-gray-700 line-clamp-3">
          {page.plain_text || 'Sin contenido...'}
        </p>
        {page.meta_description && (
          <p className="text-xs text-gray-500 mt-2 italic">
            SEO: {page.meta_description}
          </p>
        )}
      </div>

      {/* Meta Information */}
      <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
        <div className="flex items-center gap-4">
          <span>Creado: {formatDate(page.created_at)}</span>
          <span>Actualizado: {formatDate(page.updated_at)}</span>
          {page.published_at && (
            <span>Publicado: {formatDate(page.published_at)}</span>
          )}
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
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={() => onEdit(page.id)}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors"
          >
            <Edit3 className="w-4 h-4" />
            Edit
          </button>
          <button
            onClick={() => onView(page.id)}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-50 rounded-md transition-colors"
          >
            <Eye className="w-4 h-4" />
            View
          </button>
        </div>

        <div className="flex items-center gap-1">
          {canPublish && (
            <button
              onClick={() => onPublish(page.id)}
              className="px-3 py-1.5 text-sm text-green-600 hover:text-green-800 hover:bg-green-50 rounded-md transition-colors"
            >
              Publish
            </button>
          )}
          {canArchive && (
            <button
              onClick={() => onArchive(page.id)}
              className="flex items-center gap-1 px-3 py-1.5 text-sm text-orange-600 hover:text-orange-800 hover:bg-orange-50 rounded-md transition-colors"
            >
              <Archive className="w-4 h-4" />
              Archive
            </button>
          )}
          {canSetDefault && (
            <button
              onClick={() => onSetDefault(page.id)}
              className="flex items-center gap-1 px-3 py-1.5 text-sm text-yellow-600 hover:text-yellow-800 hover:bg-yellow-50 rounded-md transition-colors"
            >
              <Star className="w-4 h-4" />
              Set as Default
            </button>
          )}
          <button
            onClick={() => onDelete(page.id)}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompanyPageCard;
