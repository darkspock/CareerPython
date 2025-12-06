/**
 * Talent Pool Page Wrapper
 * Wraps the TalentPoolPage component with company context
 */

import { useNavigate } from 'react-router-dom';
import { TalentPoolPage } from '../../components/company/talentPool/TalentPoolPage';

function getCompanyId(): string | null {
  const token = localStorage.getItem('access_token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.company_id;
  } catch {
    return null;
  }
}

export default function TalentPoolPageWrapper() {
  const navigate = useNavigate();
  const companyId = getCompanyId();

  if (!companyId) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">Company not found</p>
          <button
            onClick={() => navigate('/company/login')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <TalentPoolPage
      companyId={companyId}
      onViewEntry={(entry) => {
        // Navigate to candidate detail if candidate_id exists
        if (entry.candidate_id) {
          navigate(`/company/candidates/${entry.candidate_id}`);
        }
      }}
    />
  );
}
