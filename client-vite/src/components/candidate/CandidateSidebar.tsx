import { useMemo, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { ArrowRight, X, CheckCircle, Clock, XCircle, Archive, AlertCircle } from 'lucide-react';
import type { CompanyCandidate } from '../../types/companyCandidate';
import type { WorkflowStage } from '../../types/workflow';
import { getCandidateStatusColor, getPriorityColor } from '../../types/companyCandidate';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

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
        return <Archive className="w-5 h-5 text-muted-foreground" />;
      default:
        return <AlertCircle className="w-5 h-5 text-muted-foreground" />;
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
    <TooltipProvider>
      <div className="lg:col-span-1 space-y-6">
        {/* Status Card */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">
              {t('company.candidates.applicationStatus')}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Current Status - Only show when inactive */}
            {candidate.status !== 'ACTIVE' && (
              <div>
                <label className="text-sm text-muted-foreground block mb-2">
                  {t('company.candidates.detail.currentStatus', { defaultValue: 'Current Status' })}
                </label>
                <div className="flex items-center gap-2">
                  {getStatusIcon(candidate.status)}
                  <Badge
                    variant="secondary"
                    className={getCandidateStatusColor(candidate.status)}
                  >
                    {candidate.status.replace('_', ' ')}
                  </Badge>
                </div>
              </div>
            )}

            {/* Priority - Only show when not MEDIUM */}
            {candidate.priority !== 'MEDIUM' && (
              <div>
                <label className="text-sm text-muted-foreground block mb-2">
                  {t('company.candidates.detail.priority', { defaultValue: 'Priority' })}
                </label>
                <Badge
                  variant="secondary"
                  className={getPriorityColor(candidate.priority)}
                >
                  {candidate.priority}
                </Badge>
              </div>
            )}

            {/* Workflow Information */}
            {(candidate.workflow_name || candidate.stage_name || candidate.phase_name) && (
              <div className="space-y-2">
                {candidate.phase_name && (
                  <div className="text-sm">
                    <span className="text-muted-foreground">{t('company.candidates.detail.phase')}:</span>{' '}
                    <span className="font-medium text-foreground">{candidate.phase_name}</span>
                  </div>
                )}
                {candidate.workflow_name && (
                  <div className="text-sm">
                    <span className="font-medium text-foreground">{candidate.workflow_name}</span>
                  </div>
                )}
                {candidate.stage_name && (
                  <div className="text-sm">
                    <span className="font-medium text-foreground">{candidate.stage_name}</span>
                  </div>
                )}
              </div>
            )}

            {/* Stage Transitions */}
            {candidate.current_workflow_id && (nextStage || failStages.length > 0) && (
              <div>
                <label className="text-sm text-muted-foreground block mb-2">
                  {t('company.candidates.detail.actions', { defaultValue: 'Actions' })}
                </label>
                <div className="flex flex-wrap gap-2">
                  {/* Next Stage Button */}
                  {nextStage && (
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button
                          size="icon"
                          onClick={() => handleChangeStage(nextStage.id)}
                          disabled={changingStage}
                          style={{
                            backgroundColor: nextStage.style?.background_color || '#3B82F6',
                            color: nextStage.style?.color || '#FFFFFF',
                          }}
                          className="hover:opacity-90"
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
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>
                        {t('company.candidates.moveToStage', { stage: nextStage.name })}
                      </TooltipContent>
                    </Tooltip>
                  )}

                  {/* Fail Stages Buttons */}
                  {failStages.map((stage) => (
                    <Tooltip key={stage.id}>
                      <TooltipTrigger asChild>
                        <Button
                          size="icon"
                          onClick={() => handleChangeStage(stage.id)}
                          disabled={changingStage}
                          style={{
                            backgroundColor: stage.style?.background_color || '#DC2626',
                            color: stage.style?.color || '#FFFFFF',
                          }}
                          className="hover:opacity-90"
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
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>
                        {t('company.candidates.moveToStage', { stage: stage.name })}
                      </TooltipContent>
                    </Tooltip>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Dates Card */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">{t('company.candidates.dates')}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div>
              <span className="text-muted-foreground">{t('company.candidates.detail.created')}:</span>
              <p className="font-medium text-foreground">{createdDate}</p>
            </div>
            <div>
              <span className="text-muted-foreground">
                {t('company.candidates.detail.lastUpdated', { defaultValue: 'Last Updated' })}:
              </span>
              <p className="font-medium text-foreground">{updatedDate}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </TooltipProvider>
  );
}
