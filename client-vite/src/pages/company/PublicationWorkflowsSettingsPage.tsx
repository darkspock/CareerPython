import { useTranslation } from 'react-i18next';
import WorkflowsSettingsPage from '../workflow/WorkflowsSettingsPage.tsx';

export default function PublicationWorkflowsSettingsPage() {
  const { t } = useTranslation();

  return (
    <WorkflowsSettingsPage
      workflowType="PO"
      title={t('company.settings.publicationWorkflows.title')}
      subtitle={t('company.settings.publicationWorkflows.description')}
      createRoute="/company/settings/publication-workflows/create"
      editRoute={(id) => `/company/workflows/${id}/edit`}
      advancedConfigRoute={(id) => `/company/workflows/${id}/advanced-config`}
    />
  );
}
