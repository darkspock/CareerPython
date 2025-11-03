import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Briefcase, MapPin, DollarSign, Users, Eye, Edit, Trash2, ExternalLink, Globe, GlobeLock } from 'lucide-react';
import { PositionService } from '../../services/positionService';
import { recruiterCompanyService } from '../../services/recruiterCompanyService';
import type { Position } from '../../types/position';
import { getStatusColor, getContractTypeLabel } from '../../types/position';

export default function PositionsListPage() {
  const navigate = useNavigate();
  const [positions, setPositions] = useState<Position[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [companySlug, setCompanySlug] = useState<string | null>(null);

  const getCompanyId = () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.company_id;
    } catch {
      return null;
    }
  };

  useEffect(() => {
    loadCompanyData();
    loadPositions();
  }, []);

  const loadCompanyData = async () => {
    try {
      const companyId = getCompanyId();
      if (!companyId) return;

      const company = await recruiterCompanyService.getCompany(companyId);
      setCompanySlug(company.slug);
    } catch (err) {
      console.error('Error loading company data:', err);
    }
  };

  const loadPositions = async () => {
    try {
      setLoading(true);
      const companyId = getCompanyId();
      console.log('[PositionsList] Company ID:', companyId);

      if (!companyId) {
        setError('Company ID not found');
        return;
      }

      const response = await PositionService.getPositions({ company_id: companyId });
      console.log('[PositionsList] API Response:', response);
      console.log('[PositionsList] Positions:', response.positions);
      console.log('[PositionsList] Positions count:', response.positions?.length);

      setPositions(response.positions || []);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load positions');
      console.error('[PositionsList] Error loading positions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (positionId: string) => {
    if (!confirm('Are you sure you want to delete this position?')) return;

    try {
      await PositionService.deletePosition(positionId);
      loadPositions();
    } catch (err: any) {
      alert('Failed to delete position: ' + err.message);
    }
  };

  const handleTogglePublish = async (position: Position) => {
    const action = position.is_public ? 'unpublish' : 'publish';
    if (!confirm(`Are you sure you want to ${action} this position?`)) return;

    try {
      // When publishing (is_public=true), the backend will automatically approve and open the position
      // so it appears in public listings
      await PositionService.updatePosition(position.id, {
        is_public: !position.is_public
      });
      loadPositions();
    } catch (err: any) {
      alert(`Failed to ${action} position: ` + err.message);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const publicUrl = companySlug ? `/companies/${companySlug}/open-positions` : null;

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Job Positions</h1>
            <p className="text-gray-600 mt-1">Manage your open positions and vacancies</p>
          </div>
          <div className="flex items-center gap-3">
            {publicUrl && (
              <a
                href={publicUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
              >
                <ExternalLink className="w-5 h-5" />
                View Public Page
              </a>
            )}
            <button
              onClick={() => navigate('/company/positions/create')}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-5 h-5" />
              Create Position
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Positions List */}
      {positions.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No positions yet</h3>
          <p className="text-gray-600 mb-6">
            Create your first job position to start attracting candidates
          </p>
          <button
            onClick={() => navigate('/company/positions/create')}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Create Position
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {positions.map((position) => (
            <div
              key={position.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                {/* Header */}
                <div className="mb-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 flex-1">
                      {position.title}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(position.status)}`}>
                      {position.status}
                    </span>
                  </div>
                  {position.department && (
                    <p className="text-sm text-gray-600">{position.department}</p>
                  )}
                </div>

                {/* Details */}
                <div className="space-y-2 mb-4 text-sm text-gray-600">
                  {position.location && (
                    <div className="flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-gray-400" />
                      <span>{position.location}</span>
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <Briefcase className="w-4 h-4 text-gray-400" />
                    <span>{getContractTypeLabel(position.contract_type as any)}</span>
                  </div>
                  {position.salary_range && (
                    <div className="flex items-center gap-2">
                      <DollarSign className="w-4 h-4 text-gray-400" />
                      <span>
                        {position.salary_range.currency} {position.salary_range.min_amount.toLocaleString()} - {position.salary_range.max_amount.toLocaleString()}
                      </span>
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4 text-gray-400" />
                    <span>{position.number_of_openings} opening{position.number_of_openings !== 1 ? 's' : ''}</span>
                  </div>
                </div>

                {/* Public Status Badge */}
                {position.is_public && (
                  <div className="mb-3 flex items-center gap-1 text-xs text-green-700 bg-green-50 px-2 py-1 rounded">
                    <Globe className="w-3 h-3" />
                    <span>Published</span>
                  </div>
                )}

                {/* Actions */}
                <div className="flex items-center gap-2 pt-4 border-t border-gray-200">
                  <button
                    onClick={() => navigate(`/company/positions/${position.id}`)}
                    className="flex-1 px-3 py-2 text-sm bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
                    title="View details"
                  >
                    <Eye className="w-4 h-4 mx-auto" />
                  </button>
                  <button
                    onClick={() => navigate(`/company/positions/${position.id}/edit`)}
                    className="flex-1 px-3 py-2 text-sm bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
                    title="Edit"
                  >
                    <Edit className="w-4 h-4 mx-auto" />
                  </button>
                  <button
                    onClick={() => handleTogglePublish(position)}
                    className={`flex-1 px-3 py-2 text-sm rounded-lg transition-colors ${
                      position.is_public
                        ? 'bg-orange-50 text-orange-700 hover:bg-orange-100'
                        : 'bg-purple-50 text-purple-700 hover:bg-purple-100'
                    }`}
                    title={position.is_public ? 'Unpublish' : 'Publish'}
                  >
                    {position.is_public ? (
                      <GlobeLock className="w-4 h-4 mx-auto" />
                    ) : (
                      <Globe className="w-4 h-4 mx-auto" />
                    )}
                  </button>
                  <button
                    onClick={() => handleDelete(position.id)}
                    className="flex-1 px-3 py-2 text-sm bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4 mx-auto" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Info Box */}
      <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-start gap-3">
          <Briefcase className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-green-900 mb-1">About Job Positions</h4>
            <p className="text-green-800 text-sm">
              Job positions help you organize your open vacancies. You can create positions
              with details like title, department, location, salary range, and requirements.
              Link candidates to specific positions to track applications and hiring progress.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
