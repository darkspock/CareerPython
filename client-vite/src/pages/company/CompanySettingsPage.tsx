import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';
import { useTranslation } from 'react-i18next';
import { Workflow, Users, Settings, Layers, RotateCcw, Building2, FileText, UserCog, Briefcase, MessageSquare } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { phaseService } from '../../services/phaseService';
import { PositionService } from '../../services/positionService';

export default function CompanySettingsPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { getPath } = useCompanyNavigation();
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetting, setResetting] = useState(false);

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

  const handleResetConfiguration = async () => {
    const companyId = getCompanyId();
    console.log('[CompanySettings] Company ID:', companyId);

    if (!companyId) {
      alert(t('company.settings.companyIdNotFound'));
      return;
    }

    try {
      setResetting(true);
      console.log('[CompanySettings] Starting initialization...');

      console.log('[CompanySettings] Initializing candidate phases...');
      const phasesResult = await phaseService.initializeDefaultPhases(companyId);
      console.log('[CompanySettings] Phases result:', phasesResult);

      console.log('[CompanySettings] Initializing job position workflows...');
      const workflowsResult = await PositionService.initializeDefaultWorkflows(companyId);
      console.log('[CompanySettings] Workflows result:', workflowsResult);

      setShowResetModal(false);

      if ((phasesResult && phasesResult.length > 0) || (workflowsResult && workflowsResult.length > 0)) {
        const message = `Configuration initialized!\n\n` +
          `- Candidate phases: ${phasesResult?.length || 0}\n` +
          `- Job position workflows: ${workflowsResult?.length || 0}`;
        alert(message);
        navigate(getPath('settings/phases'));
      } else {
        alert(t('company.settings.phasesAlreadyExist'));
      }
    } catch (error: any) {
      console.error('[CompanySettings] Error:', error);
      const errorMessage = error.message || 'Unknown error occurred';
      alert(t('company.settings.configInitializationFailed', { error: errorMessage }));
    } finally {
      setResetting(false);
    }
  };

  const settingsCards = [
    {
      title: t('company.settings.contentPages.title'),
      description: t('company.settings.contentPages.description'),
      icon: FileText,
      path: getPath('pages'),
      color: 'indigo',
    },
    {
      title: t('company.settings.phaseManagement.title'),
      description: t('company.settings.phaseManagement.description'),
      icon: Layers,
      path: getPath('settings/phases'),
      color: 'purple',
    },
    {
      title: t('company.settings.hiringPipelines.title'),
      description: t('company.settings.hiringPipelines.description'),
      icon: Workflow,
      path: getPath('settings/hiring-pipelines'),
      color: 'blue',
    },
    {
      title: t('company.settings.publicationWorkflows.title'),
      description: t('company.settings.publicationWorkflows.description'),
      icon: Briefcase,
      path: getPath('settings/publication-workflows'),
      color: 'indigo',
    },
    {
      title: t('company.settings.companyRoles.title'),
      description: t('company.settings.companyRoles.description'),
      icon: Users,
      path: getPath('settings/roles'),
      color: 'green',
    },
    {
      title: 'Usuarios',
      description: 'Gestiona los usuarios de la empresa',
      icon: UserCog,
      path: getPath('users'),
      color: 'orange',
    },
    {
      title: 'Interview Templates',
      description: 'Gestiona los interview templates para candidatos',
      icon: MessageSquare,
      path: getPath('interview-templates'),
      color: 'teal',
    },
  ];

  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600 group-hover:bg-blue-100',
    green: 'bg-green-50 text-green-600 group-hover:bg-green-100',
    purple: 'bg-purple-50 text-purple-600 group-hover:bg-purple-100',
    indigo: 'bg-indigo-50 text-indigo-600 group-hover:bg-indigo-100',
    orange: 'bg-orange-50 text-orange-600 group-hover:bg-orange-100',
    teal: 'bg-teal-50 text-teal-600 group-hover:bg-teal-100',
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Settings className="w-8 h-8 text-gray-700" />
          <h1 className="text-3xl font-bold text-gray-900">{t('company.settings.title')}</h1>
        </div>
        <p className="text-muted-foreground">
          {t('company.settings.subtitle')}
        </p>
      </div>

      {/* Settings Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Company Profile Card */}
        <Link
          to={getPath('settings/edit')}
          className="group"
        >
          <Card className="h-full hover:shadow-md transition-all duration-200 hover:border-gray-300">
            <CardContent className="p-6">
              <div className="flex items-start gap-4">
                <div className="p-3 rounded-lg bg-indigo-50 text-indigo-600 group-hover:bg-indigo-100 transition-colors">
                  <Building2 className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                    {t('company.settings.companyProfile.title')}
                  </h2>
                  <p className="text-muted-foreground text-sm">
                    {t('company.settings.companyProfile.description')}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </Link>

        {/* Other Settings Cards */}
        {settingsCards.map((card) => {
          const Icon = card.icon;

          return (
            <Link
              key={card.path}
              to={card.path}
              className="group"
            >
              <Card className="h-full hover:shadow-md transition-all duration-200 hover:border-gray-300">
                <CardContent className="p-6">
                  <div className="flex items-start gap-4">
                    <div
                      className={`p-3 rounded-lg transition-colors ${
                        colorClasses[card.color as keyof typeof colorClasses]
                      }`}
                    >
                      <Icon className="w-6 h-6" />
                    </div>
                    <div className="flex-1">
                      <h2 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                        {card.title}
                      </h2>
                      <p className="text-muted-foreground text-sm">{card.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>

      {/* Quick Access Section */}
      <Card className="mt-12 bg-gray-50">
        <CardContent className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">{t('company.settings.quickAccess.title')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link
              to={getPath('settings/hiring-pipelines/create')}
              className="flex items-center gap-3 p-4 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-colors"
            >
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold">
                +
              </div>
              <div>
                <div className="font-medium text-gray-900">{t('company.settings.quickAccess.createPipeline.title')}</div>
                <div className="text-sm text-muted-foreground">{t('company.settings.quickAccess.createPipeline.description')}</div>
              </div>
            </Link>
            <Link
              to={getPath('settings/roles')}
              className="flex items-center gap-3 p-4 bg-white rounded-lg border border-gray-200 hover:border-green-300 hover:bg-green-50 transition-colors"
            >
              <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-semibold">
                +
              </div>
              <div>
                <div className="font-medium text-gray-900">{t('company.settings.quickAccess.addRole.title')}</div>
                <div className="text-sm text-muted-foreground">{t('company.settings.quickAccess.addRole.description')}</div>
              </div>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Initialize Configuration Section */}
      <Alert className="mt-8 border-blue-200 bg-blue-50">
        <RotateCcw className="w-5 h-5 text-blue-600" />
        <AlertDescription className="flex-1">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-semibold text-blue-900 mb-2">{t('company.settings.initializePhases.title')}</h2>
              <p className="text-blue-800 text-sm mb-4">
                {t('company.settings.initializePhases.description')}
              </p>
            </div>
            <Button onClick={() => setShowResetModal(true)}>
              <RotateCcw className="w-4 h-4 mr-2" />
              {t('company.settings.initializePhases.button')}
            </Button>
          </div>
        </AlertDescription>
      </Alert>

      {/* Reset Confirmation Modal */}
      <Dialog open={showResetModal} onOpenChange={(open) => !resetting && setShowResetModal(open)}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-3">
              <div className="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
                <RotateCcw className="h-6 w-6 text-blue-600" />
              </div>
              {t('company.settings.modal.title')}
            </DialogTitle>
          </DialogHeader>

          <div className="py-4">
            <p className="text-sm text-muted-foreground mb-4">
              {t('company.settings.modal.description')}
            </p>
            <ul className="list-disc list-inside text-sm text-muted-foreground space-y-2 mb-4 ml-4">
              <li><strong>{t('company.settings.modal.phases.sourcing.name')}</strong> ({t('company.settings.modal.phases.sourcing.type')}) - {t('company.settings.modal.phases.sourcing.description')}</li>
              <li><strong>{t('company.settings.modal.phases.evaluation.name')}</strong> ({t('company.settings.modal.phases.evaluation.type')}) - {t('company.settings.modal.phases.evaluation.description')}</li>
              <li><strong>{t('company.settings.modal.phases.offer.name')}</strong> ({t('company.settings.modal.phases.offer.type')}) - {t('company.settings.modal.phases.offer.description')}</li>
              <li><strong>{t('company.settings.modal.phases.talentPool.name')}</strong> ({t('company.settings.modal.phases.talentPool.type')}) - {t('company.settings.modal.phases.talentPool.description')}</li>
            </ul>
            <p className="text-sm text-blue-700 font-medium">
              {t('company.settings.modal.note')}
            </p>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowResetModal(false)}
              disabled={resetting}
            >
              {t('common.cancel')}
            </Button>
            <Button
              onClick={handleResetConfiguration}
              disabled={resetting}
            >
              {resetting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  {t('company.settings.modal.initializing')}
                </>
              ) : (
                <>
                  <RotateCcw className="w-4 h-4 mr-2" />
                  {t('company.settings.modal.confirmButton')}
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
