/**
 * Company Public Positions Page
 * Public page showing open positions for a specific company
 * No authentication required
 */

import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Briefcase,
  MapPin,
  DollarSign,
  Clock,
  Search,
  Filter,
  Building2,
  AlertCircle
} from 'lucide-react';
import { publicPositionService, type PublicPositionFilters } from '../../services/publicPositionService';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import { companyPageService } from '../../services/companyPageService';
import type { Position } from '../../types/position';
import type { CompanyPage } from '../../types/companyPage';
import { PageType } from '../../types/companyPage';
import '../../components/common/WysiwygEditor.css';

export default function CompanyPublicPositionsPage() {
  const navigate = useNavigate();
  const { companySlug } = useParams<{ companySlug: string }>();
  const [positions, setPositions] = useState<Position[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [companyName, setCompanyName] = useState<string>('');
  const [companyId, setCompanyId] = useState<string | null>(null);
  const [companyPage, setCompanyPage] = useState<CompanyPage | null>(null);
  const [filters, setFilters] = useState<PublicPositionFilters>({
    page: 1,
    page_size: 12
  });
  const [totalPages, setTotalPages] = useState(0);
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    if (companySlug) {
      loadCompanyBySlug();
    }
  }, [companySlug]);

  useEffect(() => {
    if (companyId) {
      setFilters(prev => ({ ...prev, company_id: companyId }));
      loadPositions();
    }
  }, [companyId, filters.page]);

  const loadCompanyBySlug = async () => {
    try {
      setLoading(true);
      if (!companySlug) {
        setError('Company slug is missing');
        setLoading(false);
        return;
      }

      const company = await recruiterCompanyService.getCompanyBySlug(companySlug);
      setCompanyId(company.id);
      setCompanyName(company.name);
      
      // Load company page if exists
      try {
        const page = await companyPageService.getPublicPage(company.id, 'PUBLIC_COMPANY_DESCRIPTION');
        if (page) {
          setCompanyPage(page);
        }
      } catch (pageErr) {
        // Company page not found, that's okay - we'll use default title
        console.log('No company page found, using default title');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load company');
      setLoading(false);
    }
  };

  const loadPositions = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await publicPositionService.listPublicPositions(filters);
      setPositions(response.positions);
      setTotalPages(response.total_pages);
    } catch (err: any) {
      setError(err.message || 'Failed to load positions');
      console.error('Error loading positions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    setFilters({ ...filters, page: 1 });
    loadPositions();
  };

  const handleFilterChange = (key: keyof PublicPositionFilters, value: any) => {
    setFilters({ ...filters, [key]: value, page: 1 });
  };

  const handleApplyFilters = () => {
    loadPositions();
    setShowFilters(false);
  };

  const handleClearFilters = () => {
    setFilters({ company_id: companyId || undefined, page: 1, page_size: 12 });
    loadPositions();
  };

  const getEmploymentTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      FULL_TIME: 'Full-time',
      PART_TIME: 'Part-time',
      CONTRACT: 'Contract',
      TEMPORARY: 'Temporary',
      INTERNSHIP: 'Internship'
    };
    return labels[type] || type;
  };

  const getExperienceLevelLabel = (level: string) => {
    const labels: Record<string, string> = {
      ENTRY: 'Entry Level',
      INTERMEDIATE: 'Intermediate',
      SENIOR: 'Senior',
      LEAD: 'Lead',
      EXECUTIVE: 'Executive'
    };
    return labels[level] || level;
  };

  if (loading && positions.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className={companyPage && companyPage.html_content ? 'text-left' : 'text-center'}>
            {/* Company Logo/Icon - Only show when there's no company page content */}
            {!companyPage || !companyPage.html_content ? (
              <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-4">
                <Building2 className="w-10 h-10 text-blue-600" />
              </div>
            ) : null}

            {/* Show company page content if available, otherwise show default title */}
            {companyPage && companyPage.html_content ? (
              <div 
                className="prose prose-lg prose-slate max-w-4xl mx-auto wysiwyg-content mb-6"
                style={{
                  maxWidth: '100%'
                }}
              >
                <div 
                  className="ProseMirror [&>*:last-child]:!mb-0"
                  style={{
                    marginBottom: 0,
                    minHeight: 'auto'
                  }}
                  dangerouslySetInnerHTML={{ __html: companyPage.html_content }}
                />
              </div>
            ) : (
              <>
                <h1 className="text-4xl font-bold text-gray-900 mb-2">
                  {companyName ? `${companyName} - Open Positions` : 'Open Positions'}
                </h1>
                <p className="text-lg text-gray-600">
                  Browse our current job openings and join our team
                </p>
              </>
            )}
          </div>

          {/* Search Bar */}
          <div className={`${companyPage && companyPage.html_content ? 'mt-6' : 'mt-8'} max-w-3xl mx-auto`}>
            <div className="flex gap-3">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by title or keyword..."
                  value={filters.search || ''}
                  onChange={(e) => handleFilterChange('search', e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-2"
              >
                <Filter className="w-5 h-5" />
                Filters
              </button>
              <button
                onClick={handleSearch}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Search
              </button>
            </div>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                  <input
                    type="text"
                    placeholder="e.g. New York, Remote"
                    value={filters.location || ''}
                    onChange={(e) => handleFilterChange('location', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
                  <input
                    type="text"
                    placeholder="e.g. Engineering, Sales"
                    value={filters.department || ''}
                    onChange={(e) => handleFilterChange('department', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Experience Level</label>
                  <select
                    value={filters.experience_level || ''}
                    onChange={(e) => handleFilterChange('experience_level', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">All Levels</option>
                    <option value="ENTRY">Entry Level</option>
                    <option value="INTERMEDIATE">Intermediate</option>
                    <option value="SENIOR">Senior</option>
                    <option value="LEAD">Lead</option>
                    <option value="EXECUTIVE">Executive</option>
                  </select>
                </div>
              </div>
              <div className="mt-4 flex items-center gap-3">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={filters.is_remote || false}
                    onChange={(e) => handleFilterChange('is_remote', e.target.checked)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700">Remote Only</span>
                </label>
                <div className="flex-1"></div>
                <button
                  onClick={handleClearFilters}
                  className="px-4 py-2 text-gray-600 hover:text-gray-900"
                >
                  Clear Filters
                </button>
                <button
                  onClick={handleApplyFilters}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Apply Filters
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            {loading ? 'Loading...' : `${positions.length} position${positions.length !== 1 ? 's' : ''} found`}
          </p>
        </div>

        {/* Position Cards Grid */}
        {positions.length === 0 && !loading ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
            <Briefcase className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No positions found</h3>
            <p className="text-gray-600 mb-4">
              We don't have any open positions matching your criteria at the moment
            </p>
            <button
              onClick={handleClearFilters}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {positions.map((position) => (
              <div
                key={position.id}
                onClick={() => navigate(`/positions/${position.public_slug || position.id}`)}
                className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
              >
                <div className="p-6">
                  {/* Position Title */}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                    {position.title}
                  </h3>

                  {/* Position Details */}
                  <div className="space-y-2 mb-4">
                    {position.location && (
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <MapPin className="w-4 h-4" />
                        {position.location}
                        {position.is_remote && <span className="text-blue-600">(Remote)</span>}
                      </div>
                    )}
                    {position.employment_type && (
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Clock className="w-4 h-4" />
                        {getEmploymentTypeLabel(position.employment_type)}
                      </div>
                    )}
                    {position.salary_range?.max_amount && (
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <DollarSign className="w-4 h-4" />
                        {position.salary_range.min_amount && `$${position.salary_range.min_amount.toLocaleString()} - `}
                        ${position.salary_range.max_amount.toLocaleString()}
                      </div>
                    )}
                  </div>

                  {/* Description Preview */}
                  {position.description && (
                    <p className="text-sm text-gray-600 line-clamp-3 mb-4">
                      {position.description}
                    </p>
                  )}

                  {/* Tags */}
                  <div className="flex flex-wrap gap-2">
                    {position.experience_level && (
                      <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                        {getExperienceLevelLabel(position.experience_level)}
                      </span>
                    )}
                    {position.department && (
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full">
                        {position.department}
                      </span>
                    )}
                  </div>
                </div>

                {/* Footer */}
                <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                  <button className="text-blue-600 font-medium text-sm hover:text-blue-700">
                    View Details →
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="mt-8 flex items-center justify-center gap-2">
            <button
              onClick={() => handleFilterChange('page', (filters.page || 1) - 1)}
              disabled={filters.page === 1}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="px-4 py-2 text-gray-700">
              Page {filters.page} of {totalPages}
            </span>
            <button
              onClick={() => handleFilterChange('page', (filters.page || 1) + 1)}
              disabled={filters.page === totalPages}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
