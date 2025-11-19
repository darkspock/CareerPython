import { useMemo, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { ArrowRight, X, CheckCircle, Clock, XCircle, Archive, AlertCircle } from 'lucide-react';
import type { CompanyCandidate } from '../../types/companyCandidate';
import type { WorkflowStage } from '../../types/workflow';
import { getCandidateStatusColor, getPriorityColor } from '../../types/companyCandidate';

interface CandidateSidebarProps {
  candidate: CompanyCandidate;
  nextStage: WorkflowStage | null;
  failStages: WorkflowStage[];
  changingStage: boolean;
  onChangeStage: (newStageId: string) => void;
}

export default function CandidateSidebar({
  candidate,
  nextStage,
  failStages,
  changingStage,
  onChangeStage,
}: CandidateSidebarProps) {
  const { t } = useTranslation();

  const getStatusIcon = useCallback((status: string) => {
    switch (status) {
      case 'ACTIVE':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'PENDING_INVITATION':
      case 'PENDING_CONFIRMATION':
        return <Clock className="w-5 h-5 text-yellow-600" />;
      case 'REJECTED':
        return <XCircle className="w-5 h-5 text-red-600" />;
      case 'ARCHIVED':
        return <Archive className="w-5 h-5 text-gray-600" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-600" />;
    }
  }, []);

  const handleChangeStage = useCallback(
    (stageId: string) => {
      onChangeStage(stageId);
    },
    [onChangeStage]
  );

  const createdDate = useMemo(
    () => new Date(candidate.created_at).toLocaleDateString(),
    [candidate.created_at]
  );

  const updatedDate = useMemo(
    () => new Date(candidate.updated_at).toLocaleDateString(),
    [candidate.updated_at]
  );

  return (
    <div className="lg:col-span-1 space-y-6">
      {/* Status Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {t('company.candidates.applicationStatus')}
        </h3>
        <div className="space-y-4">
          {/* Current Status - Only show when inactive */}
          {candidate.status !== 'ACTIVE' && (
            <div>
              <label className="text-sm text-gray-600 block mb-2">
                {t('company.candidates.detail.currentStatus', { defaultValue: 'Current Status' })}
              </label>
              <div className="flex items-center gap-2">
                {getStatusIcon(candidate.status)}
                <span
                  className={`px-3 py-1 text-sm font-medium rounded-full ${getCandidateStatusColor(
                    candidate.status
                  )}`}
                >
                  {candidate.status.replace('_', ' ')}
                </span>
              </div>
            </div>
          )}

          {/* Priority - Only show when not MEDIUM */}
          {candidate.priority !== 'MEDIUM' && (
            <div>
              <label className="text-sm text-gray-600 block mb-2">
                {t('company.candidates.detail.priority', { defaultValue: 'Priority' })}
              </label>
              <span
                className={`inline-block px-3 py-1 text-sm font-medium rounded-full ${getPriorityColor(
                  candidate.priority
                )}`}
              >
                {candidate.priority}
              </span>
            </div>
          )}

          {/* Workflow Information */}
          {(candidate.workflow_name || candidate.stage_name || candidate.phase_name) && (
            <div>
              <div className="space-y-2">
                {candidate.phase_name && (
                  <div className="text-sm">
                    <span className="text-gray-600">{t('company.candidates.detail.phase')}:</span>{' '}
                    <span className="font-medium text-gray-900">{candidate.phase_name}</span>
                  </div>
                )}
                {candidate.workflow_name && (
                  <div className="text-sm">
                    <span className="font-medium text-gray-900">{candidate.workflow_name}</span>
                  </div>
                )}
                {candidate.stage_name && (
                  <div className="text-sm">
                    <span className="font-medium text-gray-900">{candidate.stage_name}</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Stage Transitions */}
          {candidate.current_workflow_id && (nextStage || failStages.length > 0) && (
            <div>
              <label className="text-sm text-gray-600 block mb-2">
                {t('company.candidates.detail.actions', { defaultValue: 'Actions' })}
              </label>
              <div className="flex flex-wrap gap-2">
                {/* Next Stage Button */}
                {nextStage && (
                  <div className="relative group">
                    <button
                      onClick={() => handleChangeStage(nextStage.id)}
                      disabled={changingStage}
                      className="flex items-center justify-center p-2 rounded-lg transition-colors disabled:opacity-50"
                      style={{
                        backgroundColor: nextStage.style?.background_color || '#3B82F6',
                        color: nextStage.style?.color || '#FFFFFF',
                      }}
                    >
                      {changingStage ? (
                        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                      ) : (
                        <>
                          {nextStage.style?.icon ? (
                            <span
                              className="text-base"
                              dangerouslySetInnerHTML={{ __html: nextStage.style.icon }}
                            />
                          ) : (
                            <ArrowRight className="w-4 h-4" />
                          )}
                        </>
                      )}
                    </button>
                    {/* Tooltip */}
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                      {t('company.candidates.moveToStage', { stage: nextStage.name })}
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
                        <div className="border-4 border-transparent border-t-gray-900"></div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Fail Stages Buttons */}
                {failStages.map((stage) => (
                  <div key={stage.id} className="relative group">
                    <button
                      onClick={() => handleChangeStage(stage.id)}
                      disabled={changingStage}
                      className="flex items-center justify-center p-2 rounded-lg transition-colors disabled:opacity-50"
                      style={{
                        backgroundColor: stage.style?.background_color || '#DC2626',
                        color: stage.style?.color || '#FFFFFF',
                      }}
                    >
                      {changingStage ? (
                        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                      ) : (
                        <>
                          {stage.style?.icon ? (
                            <span
                              className="text-base"
                              dangerouslySetInnerHTML={{ __html: stage.style.icon }}
                            />
                          ) : (
                            <X className="w-4 h-4" />
                          )}
                        </>
                      )}
                    </button>
                    {/* Tooltip */}
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
                      {t('company.candidates.moveToStage', { stage: stage.name })}
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
                        <div className="border-4 border-transparent border-t-gray-900"></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Dates Card */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('company.candidates.dates')}</h3>
        <div className="space-y-3 text-sm">
          <div>
            <span className="text-gray-600">{t('company.candidates.detail.created')}:</span>
            <p className="font-medium text-gray-900">{createdDate}</p>
          </div>
          <div>
            <span className="text-gray-600">
              {t('company.candidates.detail.lastUpdated', { defaultValue: 'Last Updated' })}:
            </span>
            <p className="font-medium text-gray-900">{updatedDate}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

