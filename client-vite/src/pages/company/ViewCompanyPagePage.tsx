/**
 * View Company Page
 * Displays a company page in read-only mode
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, AlertCircle } from 'lucide-react';
import { companyPageService } from '../../services/companyPageService';
import type { CompanyPage } from '../../types/companyPage';
import { getPageTypeLabel, getPageStatusLabel, getPageStatusColor } from '../../types/companyPage';

export default function ViewCompanyPagePage() {
  const { pageId } = useParams<{ pageId: string }>();
  const navigate = useNavigate();
  const [page, setPage] = useState<CompanyPage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (pageId) {
      loadPage();
    }
  }, [pageId]);

  const loadPage = async () => {
    try {
      setLoading(true);
      setError(null);
      if (!pageId) {
        setError('Page ID is missing');
        setLoading(false);
        return;
      }

      const pageData = await companyPageService.getPageById(pageId);
      setPage(pageData);
    } catch (err: any) {
      setError(err.message || 'Failed to load page');
      console.error('Error loading page:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    if (pageId) {
      navigate(`/company/pages/${pageId}/edit`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-6 h-6 text-red-600" />
            <h2 className="text-lg font-semibold text-gray-900">Error</h2>
          </div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/company/pages')}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Pages
          </button>
        </div>
      </div>
    );
  }

  if (!page) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Page not found</h2>
          <button
            onClick={() => navigate('/company/pages')}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Pages
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => navigate('/company/pages')}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Pages</span>
            </button>
            <button
              onClick={handleEdit}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Edit className="w-5 h-5" />
              Edit Page
            </button>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{page.title}</h1>
            
            {/* Page Metadata */}
            <div className="flex flex-wrap gap-4 mb-6 text-sm text-gray-600">
              <div>
                <span className="font-medium">Tipo:</span> {getPageTypeLabel(page.page_type)}
              </div>
              <div>
                <span className="font-medium">Estado:</span>{' '}
                <span className={`px-2 py-1 rounded-full ${getPageStatusColor(page.status)}`}>
                  {getPageStatusLabel(page.status)}
                </span>
              </div>
              {page.language && (
                <div>
                  <span className="font-medium">Language:</span> {page.language}
                </div>
              )}
              {page.is_default && (
                <div className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                  Default
                </div>
              )}
            </div>

            {/* Meta Description */}
            {page.meta_description && (
              <div className="mb-6">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Meta Description</h3>
                <p className="text-sm text-gray-600">{page.meta_description}</p>
              </div>
            )}

            {/* Meta Keywords */}
            {page.meta_keywords && page.meta_keywords.length > 0 && (
              <div className="mb-6">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Meta Keywords</h3>
                <div className="flex flex-wrap gap-2">
                  {page.meta_keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Page Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Content</h2>
          {page.html_content ? (
            <div
              className="prose prose-lg max-w-none"
              dangerouslySetInnerHTML={{ __html: page.html_content }}
            />
          ) : (
            <div className="text-gray-500 italic">No content available</div>
          )}
        </div>

        {/* Footer Info */}
        <div className="mt-6 text-sm text-gray-500 text-center">
          {page.created_at && (
            <p>Created: {new Date(page.created_at).toLocaleDateString()}</p>
          )}
          {page.updated_at && (
            <p>Last updated: {new Date(page.updated_at).toLocaleDateString()}</p>
          )}
          {page.published_at && (
            <p>Published: {new Date(page.published_at).toLocaleDateString()}</p>
          )}
        </div>
      </div>
    </div>
  );
}

