/**
 * View Company Page
 * Displays a company page in read-only mode
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { ArrowLeft, Edit, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { companyPageService } from '../../services/companyPageService';
import type { CompanyPage } from '../../types/companyPage';
import { getPageTypeLabel, getPageStatusLabel, getPageStatusColor } from '../../types/companyPage';

export default function ViewCompanyPagePage() {
  const { pageId } = useParams<{ pageId: string }>();
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
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
      navigate(getPath(`pages/${pageId}/edit`));
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
        <Card className="max-w-md w-full">
          <CardContent className="pt-6">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
            <Button
              onClick={() => navigate(getPath('pages'))}
              className="w-full mt-4"
            >
              Back to Pages
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!page) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardContent className="pt-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Page not found</h2>
            <Button
              onClick={() => navigate(getPath('pages'))}
              className="w-full"
            >
              Back to Pages
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <Button
              variant="ghost"
              onClick={() => navigate(getPath('pages'))}
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back to Pages
            </Button>
            <Button onClick={handleEdit}>
              <Edit className="w-5 h-5 mr-2" />
              Edit Page
            </Button>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="text-3xl">{page.title}</CardTitle>
            </CardHeader>
            <CardContent>
              {/* Page Metadata */}
              <div className="flex flex-wrap gap-4 mb-6 text-sm text-gray-600">
                <div>
                  <span className="font-medium">Tipo:</span> {getPageTypeLabel(page.page_type)}
                </div>
                <div>
                  <span className="font-medium">Estado:</span>
                  <Badge className={`ml-2 ${getPageStatusColor(page.status)}`}>
                    {getPageStatusLabel(page.status)}
                  </Badge>
                </div>
                {page.language && (
                  <div>
                    <span className="font-medium">Language:</span> {page.language}
                  </div>
                )}
                {page.is_default && (
                  <Badge variant="secondary">
                    Default
                  </Badge>
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
                      <Badge key={index} variant="outline">
                        {keyword}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Page Content */}
        <Card>
          <CardHeader>
            <CardTitle>Content</CardTitle>
          </CardHeader>
          <CardContent>
            {page.html_content ? (
              <div
                className="prose prose-lg max-w-none"
                dangerouslySetInnerHTML={{ __html: page.html_content }}
              />
            ) : (
              <div className="text-gray-500 italic">No content available</div>
            )}
          </CardContent>
        </Card>

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
