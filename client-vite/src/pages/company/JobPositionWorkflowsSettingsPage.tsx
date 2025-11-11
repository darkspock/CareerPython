import WorkflowsSettingsPage from '../workflow/WorkflowsSettingsPage.tsx';

export default function JobPositionWorkflowsSettingsPage() {
  return (
    <WorkflowsSettingsPage
      workflowType="PO"
      title="Flujos de publicación de ofertas"
      subtitle="Gestiona workflows para posiciones de trabajo"
      createRoute="/company/workflows/create"
      editRoute={(id) => `/company/workflows/${id}/edit`}
      advancedConfigRoute={(id) => `/company/workflows/${id}/advanced-config`}
    />
  );
}

