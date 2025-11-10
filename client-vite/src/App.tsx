import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Import pages (we'll create these)
import HomePage from './pages/HomePage';
import LandingPage from './pages/LandingPage';
import CandidatesPage from './pages/CandidatesPage';
// REMOVED: LoginPage - using specific CandidateLoginPage, AdminLoginPage, and CompanyLoginPage instead
import CandidateLoginPage from './pages/CandidateLoginPage';
import AdminLoginPage from './pages/AdminLoginPage';
import CompanyLoginPage from './pages/CompanyLoginPage';
import CompanyDashboardPage from './pages/CompanyDashboardPage';
import RegisterPage from './pages/RegisterPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import CompleteProfilePage from './pages/CompleteProfilePage';
import PDFProcessingPage from './pages/PDFProcessingPage';

// Import onboarding pages
import OnboardingExperiencePage from './pages/onboarding/OnboardingExperiencePage';
import OnboardingEducationPage from './pages/onboarding/OnboardingEducationPage';
import OnboardingProjectsPage from './pages/onboarding/OnboardingProjectsPage';
import OnboardingResumesPage from './pages/onboarding/OnboardingResumesPage';
// REMOVED: WorkExperiencePage - using /candidate/profile/experience instead
// REMOVED: EducationPage - using /candidate/profile/education instead
// REMOVED: ProjectsPage - using /candidate/profile/projects instead
// REMOVED: Resume pages - using /candidate/profile/resumes/* instead
// import ResumePage from './pages/ResumePage';
// import ResumeEditorPage from './pages/ResumeEditorPage';
// import ResumePreviewPageRoute from './pages/ResumePreviewPage';
// import ResumeExportPage from './pages/ResumeExportPage';
import InterviewPage from './pages/InterviewPage';

// Import candidate profile pages
import CandidateProfilePage from './pages/CandidateProfilePage';
import {
  EditBasicInfoPage,
  EditExperiencePage,
  EditEducationPage,
  EditProjectsPage
} from './pages/candidate-profile';
import ResumesPage from './pages/candidate-profile/ResumesPage';
import CreateResumePage from './pages/candidate-profile/CreateResumePage';
import ResumePreviewPageRoute from './pages/ResumePreviewPage';
import ResumeEditorPage from './pages/ResumeEditorPage';
import WysiwygTestPageRoute from './pages/WysiwygTestPage';
import HybridEditorTestPage from './pages/HybridEditorTestPage';
import SimpleWysiwygTest from './pages/SimpleWysiwygTest';
import EditorDiagnosticPage from './pages/EditorDiagnosticPage';
import SaveTestPage from './pages/SaveTestPage';
import AITestPage from './pages/AITestPage';
import TooltipTestPage from './pages/TooltipTestPage';
// Temporarily disabled interview pages
// import InterviewSchedulingPage from './pages/InterviewSchedulingPage';
// import InterviewConductPage from './pages/InterviewConductPage';
// import InterviewAnalyticsPage from './pages/InterviewAnalyticsPage';
// import InterviewTemplatesPage from './pages/InterviewTemplatesPage';

// Import admin components
import ProtectedAdminRoute from './components/admin/ProtectedAdminRoute';
import AdminLayout from './components/admin/AdminLayout';

// Import company components
import ProtectedCompanyRoute from './components/company/ProtectedCompanyRoute';
import CompanyLayout from './components/company/CompanyLayout';
import CandidatesListPage from './pages/company/CandidatesListPage';
import AddCandidatePage from './pages/company/AddCandidatePage';
import CandidateDetailPage from './pages/company/CandidateDetailPage';
import EditCandidatePage from './pages/company/EditCandidatePage';
import WorkflowsSettingsPage from './pages/workflow/WorkflowsSettingsPage.tsx';
import WorkflowAdvancedConfigPage from './pages/workflow/WorkflowAdvancedConfigPage.tsx';
import CompanySettingsPage from './pages/company/CompanySettingsPage';
import CompanyRolesPage from './pages/company/CompanyRolesPage';
import PositionsListPage from './pages/company/PositionsListPage';
import JobPositionWorkflowsSettingsPage from './pages/company/JobPositionWorkflowsSettingsPage.tsx';
import CreateJobPositionWorkflowPage from './pages/company/CreateJobPositionWorkflowPage';
import WorkflowBoardPage from './pages/workflow/WorkflowBoardPage.tsx';
import CreatePositionPage from './pages/company/CreatePositionPage';
import CreateWorkflowPage from './pages/workflow/CreateWorkflowPage.tsx';
import EditWorkflowPage from './pages/workflow/EditWorkflowPage.tsx';
import PositionDetailPage from './pages/company/PositionDetailPage';
import EditPositionPage from './pages/company/EditPositionPage';
import PhasesPage from './pages/company/PhasesPage';
import EditCompanyPage from './pages/company/EditCompanyPage';
import CompanyPagesListPage from './pages/company/CompanyPagesListPage';
import CreateCompanyPagePage from './pages/company/CreateCompanyPagePage';
import EditCompanyPagePage from './pages/company/EditCompanyPagePage';
import ViewCompanyPagePage from './pages/company/ViewCompanyPagePage';
import UsersManagementPage from './pages/company/UsersManagementPage';
import PublicPositionsPage from './pages/public/PublicPositionsPage';
import PublicPositionDetailPage from './pages/public/PublicPositionDetailPage';
import CompanyPublicPositionsPage from './pages/public/CompanyPublicPositionsPage';
import AcceptInvitationPage from './pages/public/AcceptInvitationPage';
import CompanyLandingPage from './pages/public/CompanyLandingPage';
import CompanyRegisterPage from './pages/public/CompanyRegisterPage';
import AdminDashboard from './components/admin/AdminDashboard';
import UsersManagement from './components/admin/UsersManagement';
import CandidatesManagement from './components/admin/CandidatesManagement';
import CompaniesManagement from './components/admin/CompaniesManagement';
import PositionsManagement from './components/admin/PositionsManagement';
import InterviewTemplatesManagement from './components/admin/InterviewTemplatesManagement';
import InterviewTemplateEditor from './components/admin/InterviewTemplateEditor';

// Import providers
import { RefreshProvider } from './context/RefreshContext';
import { I18nProvider } from './components/i18n/I18nProvider';
import { ToastProvider } from './components/realtime/ToastProvider';
import { RealTimeProvider } from './context/RealTimeContext';
import {
  ErrorProvider,
  ConnectionProvider,
  MonitoringProvider
} from './components/error-handling';

// Import common components
import LanguageSwitcher from './components/common/LanguageSwitcher';

function App() {
  return (
    <I18nProvider>
      <ErrorProvider>
        <ConnectionProvider>
          <MonitoringProvider
            onErrorReport={async (report) => {
              console.error('Error reported to monitoring service:', report);
            }}
          >
            <RefreshProvider>
              <ToastProvider>
                <RealTimeProvider userId="demo-user">
                  <Router>
                    <div className="min-h-screen bg-gray-50">
                      {/* Language Switcher - available on all pages */}
                      <LanguageSwitcher />

                      <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/candidate/landing" element={<LandingPage />} />
                        <Route path="/positions" element={<PublicPositionsPage />} />
                        <Route path="/positions/:slugOrId" element={<PublicPositionDetailPage />} />
                        <Route path="/companies/:companySlug/open-positions" element={<CompanyPublicPositionsPage />} />
                        <Route path="/invitations/accept" element={<AcceptInvitationPage />} />
                        <Route path="/company/landing" element={<CompanyLandingPage />} />
                        <Route path="/company/register" element={<CompanyRegisterPage />} />
                        <Route path="/candidate/dashboard" element={<HomePage />} />
                        <Route path="/candidate/search" element={<CandidatesPage />} />
                        {/* REMOVED: /auth/login - using specific /candidate/auth/login, /admin/auth/login, and /company/auth/login instead */}
                        <Route path="/candidate/auth/login" element={<CandidateLoginPage />} />
                        <Route path="/admin/auth/login" element={<AdminLoginPage />} />
                        <Route path="/company/auth/login" element={<CompanyLoginPage />} />
                        {/* Redirect common login paths for convenience */}
                        <Route path="/admin/login" element={<Navigate to="/admin/auth/login" replace />} />
                        <Route path="/candidate/login" element={<Navigate to="/candidate/auth/login" replace />} />
                        <Route path="/company/login" element={<Navigate to="/company/auth/login" replace />} />
                        <Route path="/candidate/auth/register" element={<RegisterPage />} />
                        <Route path="/candidate/reset-password" element={<ResetPasswordPage />} />
                        <Route path="/candidate/onboarding" element={<Navigate to="/candidate/onboarding/complete-profile" replace />} />
                        <Route path="/candidate/onboarding/complete-profile" element={<CompleteProfilePage />} />
                        <Route path="/candidate/onboarding/pdf-processing" element={<PDFProcessingPage />} />
                        <Route path="/candidate/onboarding/experience" element={<OnboardingExperiencePage />} />
                        <Route path="/candidate/onboarding/education" element={<OnboardingEducationPage />} />
                        <Route path="/candidate/onboarding/projects" element={<OnboardingProjectsPage />} />
                        <Route path="/candidate/onboarding/resumes" element={<OnboardingResumesPage />} />
                        {/* REMOVED: /work-experience - using /candidate/profile/experience instead */}
                        {/* REMOVED: /education - using /candidate/profile/education instead */}
                        {/* REMOVED: /projects - using /candidate/profile/projects instead */}
                        {/* REMOVED: /resumes/* routes - using /candidate/profile/resumes/* instead */}
                        <Route path="/interviews" element={<InterviewPage />} />

                        {/* Candidate Profile Dashboard Routes */}
                        <Route path="/candidate/profile" element={<CandidateProfilePage />} />
                        <Route path="/candidate/profile/edit" element={<EditBasicInfoPage />} />
                        <Route path="/candidate/profile/experience" element={<EditExperiencePage />} />
                        <Route path="/candidate/profile/education" element={<EditEducationPage />} />
                        <Route path="/candidate/profile/projects" element={<EditProjectsPage />} />
                        <Route path="/candidate/profile/resumes" element={<ResumesPage />} />
                        <Route path="/candidate/profile/resumes/create" element={<CreateResumePage />} />
                        <Route path="/candidate/profile/resumes/:id/preview" element={<ResumePreviewPageRoute />} />
                        <Route path="/candidate/profile/resumes/:id/edit" element={<ResumeEditorPage />} />
                        {/* Test routes for WYSIWYG editor */}
                        <Route path="/test/wysiwyg" element={<WysiwygTestPageRoute />} />
                        <Route path="/test/simple-wysiwyg" element={<SimpleWysiwygTest />} />
                        <Route path="/test/hybrid-editor" element={<HybridEditorTestPage />} />
                        <Route path="/test/save" element={<SaveTestPage />} />
                        <Route path="/test/ai" element={<AITestPage />} />
                        <Route path="/test/tooltip" element={<TooltipTestPage />} />
                        <Route path="/diagnostic-editor/:id" element={<EditorDiagnosticPage />} />
                        {/* Temporarily disabled interview routes */}
                        <Route path="/interviews/schedule" element={<div>Interview Scheduling - Temporarily Disabled</div>} />
                        <Route path="/interviews/analytics" element={<div>Interview Analytics - Temporarily Disabled</div>} />
                        <Route path="/interviews/templates" element={<div>Interview Templates - Temporarily Disabled</div>} />
                        <Route path="/interviews/:interviewId/conduct" element={<div>Interview Conduct - Temporarily Disabled</div>} />

                        {/* Admin Routes */}
                        <Route path="/admin/*" element={
                          <ProtectedAdminRoute>
                            <AdminLayout />
                          </ProtectedAdminRoute>
                        }>
                          <Route path="dashboard" element={<AdminDashboard />} />
                          <Route path="users" element={<UsersManagement />} />
                          <Route path="candidates" element={<CandidatesManagement />} />
                          <Route path="companies" element={<CompaniesManagement />} />
                          <Route path="positions" element={<PositionsManagement />} />
                          <Route path="job-positions" element={<PositionsManagement />} />
                          <Route path="interview-templates" element={<InterviewTemplatesManagement />} />
                          <Route path="interview-templates/create" element={<InterviewTemplateEditor />} />
                          <Route path="interview-templates/edit/:templateId" element={<InterviewTemplateEditor />} />
                          <Route index element={<AdminDashboard />} />
                        </Route>

                        {/* Company Routes */}
                        <Route path="/company/*" element={
                          <ProtectedCompanyRoute>
                            <CompanyLayout />
                          </ProtectedCompanyRoute>
                        }>
                          <Route path="dashboard" element={<CompanyDashboardPage />} />
                          <Route path="candidates" element={<CandidatesListPage />} />
                          <Route path="candidates/add" element={<AddCandidatePage />} />
                          <Route path="candidates/:id" element={<CandidateDetailPage />} />
                          <Route path="candidates/:id/edit" element={<EditCandidatePage />} />
                          <Route path="workflow-board" element={<WorkflowBoardPage />} />
                          <Route path="positions" element={<PositionsListPage />} />
                          <Route path="positions/create" element={<CreatePositionPage />} />
                          <Route path="positions/:id" element={<PositionDetailPage />} />
                          <Route path="positions/:id/edit" element={<EditPositionPage />} />
                          <Route path="workflows/create" element={<CreateWorkflowPage />} />
                          <Route path="workflows/:workflowId/edit" element={<EditWorkflowPage />} />
                          <Route path="workflows/:workflowId/advanced-config" element={<WorkflowAdvancedConfigPage />} />
                          <Route path="pages" element={<CompanyPagesListPage />} />
                          <Route path="pages/create" element={<CreateCompanyPagePage />} />
                          <Route path="pages/:pageId/view" element={<ViewCompanyPagePage />} />
                          <Route path="pages/:pageId/edit" element={<EditCompanyPagePage />} />
                          <Route path="settings" element={<CompanySettingsPage />} />
                          <Route path="settings/edit" element={<EditCompanyPage />} />
                          <Route path="settings/workflows" element={<WorkflowsSettingsPage />} />
                          <Route path="settings/workflows/create" element={<CreateWorkflowPage />} />
                          <Route path="settings/job-position-workflows" element={<JobPositionWorkflowsSettingsPage />} />
                          <Route path="settings/phases" element={<PhasesPage />} />
                          <Route path="settings/roles" element={<CompanyRolesPage />} />
                          <Route path="users" element={<UsersManagementPage />} />
                          <Route index element={<CompanyDashboardPage />} />
                        </Route>
                      </Routes>
                    </div>
                  </Router>
                  <ToastContainer />
                </RealTimeProvider>
              </ToastProvider>
            </RefreshProvider>
          </MonitoringProvider>
        </ConnectionProvider>
      </ErrorProvider>
    </I18nProvider>
  );
}

export default App;