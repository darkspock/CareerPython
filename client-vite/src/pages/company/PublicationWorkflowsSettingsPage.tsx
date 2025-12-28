import { useTranslation } from 'react-i18next';
import WorkflowsSettingsPage from '../workflow/WorkflowsSettingsPage.tsx';
import { useCompanyNavigation } from '../../hooks/useCompanyNavigation';

export default function PublicationWorkflowsSettingsPage() {
  const { t } = useTranslation();
  const { getPath } = useCompanyNavigation();

  return (
    <WorkflowsSettingsPage
      workflowType="PO"
      title={t('company.settings.publicationWorkflows.title')}
      subtitle={t('company.settings.publicationWorkflows.description')}
      createRoute={getPath('settings/publication-workflows/create')}
      editRoute={(id) => getPath(`workflows/${id}/edit`)}
      advancedConfigRoute={(id) => getPath(`workflows/${id}/advanced-config`)}
    />
  );
}
