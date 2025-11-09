import WorkflowsSettingsPage from '../workflow/WorkflowsSettingsPage.tsx';

export default function JobPositionWorkflowsSettingsPage() {
  return (
    <WorkflowsSettingsPage
      workflowType="PO"
      title="Job Position Workflows"
      subtitle="Manage workflows for job positions"
      createRoute="/company/workflows/create"
      editRoute={(id) => `/company/workflows/${id}/edit`}
      advancedConfigRoute={(id) => `/company/workflows/${id}/advanced-config`}
    />
  );
}

