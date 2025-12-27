/**
 * Company About Page
 * Public page showing company information
 * URL: /:companySlug/about
 */

import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Building2, Briefcase, ArrowRight } from 'lucide-react';
import { api } from '../../lib/api';

interface CompanyAboutData {
  company: {
    id: string;
    name: string;
    slug: string;
    logo_url: string | null;
  };
  page: {
    type: string;
    title: string;
    content: string | null;
    sections: Array<{
      title: string;
      content: string;
    }>;
  };
}

export default function CompanyScopedAboutPage() {
  const { companySlug } = useParams<{ companySlug: string }>();
  const [data, setData] = useState<CompanyAboutData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (companySlug) {
      loadCompanyAbout();
    }
  }, [companySlug]);

  const loadCompanyAbout = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await api.getPublicCompanyAbout(companySlug!);
      setData(result);
    } catch (err: any) {
      setError(err.message || 'Failed to load company information');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">404</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Company Not Found</h1>
          <p className="text-gray-600 mb-4">
            {error || 'The company you are looking for does not exist.'}
          </p>
          <Link
            to="/positions"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Browse All Jobs
          </Link>
        </div>
      </div>
    );
  }

  const { company, page } = data;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            {/* Company Logo */}
            {company.logo_url ? (
              <img
                src={company.logo_url}
                alt={company.name}
                className="w-24 h-24 rounded-full mx-auto mb-6 object-cover"
              />
            ) : (
              <div className="inline-flex items-center justify-center w-24 h-24 bg-blue-100 rounded-full mb-6">
                <Building2 className="w-12 h-12 text-blue-600" />
              </div>
            )}

            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              {page.title || company.name}
            </h1>

            {/* Quick links */}
            <div className="flex justify-center gap-4 mt-6">
              <Link
                to={`/${companySlug}/positions`}
                className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Briefcase className="w-5 h-5" />
                View Open Positions
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* About Content */}
        {page.content ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8">
            <div
              className="prose prose-lg max-w-none"
              dangerouslySetInnerHTML={{ __html: page.content }}
            />
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-8 text-center">
            <Building2 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Welcome to {company.name}
            </h2>
            <p className="text-gray-600">
              We're building something great. Check out our open positions to join our team!
            </p>
          </div>
        )}

        {/* Sections */}
        {page.sections && page.sections.length > 0 && (
          <div className="space-y-6">
            {page.sections.map((section, index) => (
              <div
                key={index}
                className="bg-white rounded-lg shadow-sm border border-gray-200 p-8"
              >
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  {section.title}
                </h2>
                <div
                  className="prose max-w-none"
                  dangerouslySetInnerHTML={{ __html: section.content }}
                />
              </div>
            ))}
          </div>
        )}

        {/* CTA */}
        <div className="mt-12 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to join our team?
          </h2>
          <Link
            to={`/${companySlug}/positions`}
            className="inline-flex items-center gap-2 px-8 py-4 bg-blue-600 text-white text-lg font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Briefcase className="w-6 h-6" />
            View Open Positions
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
