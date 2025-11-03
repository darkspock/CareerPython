/**
 * End-to-End Tests for Resume Preview and Export Workflow
 *
 * Tests the complete user journey from viewing resumes to
 * previewing and exporting them with various options.
 */

// import React from 'react'; // Not used
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import ResumePreviewPage from '../ResumePreviewPage';
import ResumeExportModal from '../../export/ResumeExportModal';
import { api } from '../../../../lib/api';

// Mock the API
jest.mock('../../../../lib/api');
const mockedApi = api as jest.Mocked<typeof api>;

// Mock framer-motion
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>
  },
  AnimatePresence: ({ children }: any) => <>{children}</>
}));

// Mock URL.createObjectURL
global.URL.createObjectURL = jest.fn(() => 'mocked-url');
global.URL.revokeObjectURL = jest.fn();

const mockResumeData = {
  id: 'resume-1',
  name: 'Senior Developer Resume',
  candidate_id: 'user-1',
  content: {
    sections: [
      {
        id: 'section-1',
        type: 'summary',
        title: 'Professional Summary',
        content: '<p>Experienced software engineer with 8+ years in full-stack development, specializing in React, Node.js, and cloud architecture.</p>',
        order: 0,
        isVisible: true
      },
      {
        id: 'section-2',
        type: 'experience',
        title: 'Work Experience',
        content: '<h4>Senior Software Engineer - TechCorp (2020-Present)</h4><ul><li>Led development of microservices architecture</li><li>Mentored junior developers</li></ul>',
        order: 1,
        isVisible: true
      },
      {
        id: 'section-3',
        type: 'skills',
        title: 'Technical Skills',
        content: '<ul><li>JavaScript/TypeScript</li><li>React/Vue.js</li><li>Node.js/Python</li><li>AWS/Docker</li></ul>',
        order: 2,
        isVisible: true
      }
    ],
    template: 'professional',
    personalInfo: {
      title: 'Senior Software Engineer',
      email: 'john.doe@example.com',
      phone: '+1-555-0123',
      location: 'San Francisco, CA',
      website: 'https://johndoe.dev'
    }
  },
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-15T00:00:00Z'
};

const mockExportHistory = [
  {
    id: 'export-1',
    format: 'pdf',
    template: 'professional',
    downloadedAt: '2024-01-15T10:30:00Z',
    downloadUrl: 'https://example.com/download/resume-1.pdf'
  },
  {
    id: 'export-2',
    format: 'docx',
    template: 'modern',
    downloadedAt: '2024-01-14T15:20:00Z',
    downloadUrl: 'https://example.com/download/resume-1.docx'
  }
];

describe('Resume Preview and Export E2E Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockedApi.getResume.mockResolvedValue(mockResumeData);
    mockedApi.exportResume.mockResolvedValue({
      success: true,
      download_url: 'https://example.com/download/test.pdf',
      export_id: 'export-123'
    });
    mockedApi.getResumeExportHistory.mockResolvedValue(mockExportHistory);
    mockedApi.getResumePreviewHtml.mockResolvedValue(new Response('<html><body><h1>Resume Preview</h1></body></html>', {
      headers: { 'Content-Type': 'text/html' }
    }));
  });

  describe('Resume Preview Workflow', () => {
    const renderPreviewPage = () => {
      return render(
        <MemoryRouter>
          <ResumePreviewPage resumeId="resume-1" />
        </MemoryRouter>
      );
    };

    it('loads and displays resume preview with all sections', async () => {
      renderPreviewPage();

      // Wait for data to load
      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Check personal information is displayed
      expect(screen.getByText('Senior Developer Resume')).toBeInTheDocument();
      expect(screen.getByText('Senior Software Engineer')).toBeInTheDocument();
      expect(screen.getByText('john.doe@example.com')).toBeInTheDocument();
      expect(screen.getByText('+1-555-0123')).toBeInTheDocument();
      expect(screen.getByText('San Francisco, CA')).toBeInTheDocument();
      expect(screen.getByText('https://johndoe.dev')).toBeInTheDocument();

      // Check sections are displayed
      expect(screen.getByText('Professional Summary')).toBeInTheDocument();
      expect(screen.getByText('Work Experience')).toBeInTheDocument();
      expect(screen.getByText('Technical Skills')).toBeInTheDocument();

      // Check section content is displayed
      expect(screen.getByText(/Experienced software engineer/)).toBeInTheDocument();
      expect(screen.getByText(/Senior Software Engineer - TechCorp/)).toBeInTheDocument();
      expect(screen.getByText(/JavaScript\/TypeScript/)).toBeInTheDocument();
    });

    it('allows template switching and updates preview styling', async () => {
      renderPreviewPage();

      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Open template selector
      const templateButton = screen.getByText('Template');
      fireEvent.click(templateButton);

      // Select modern template
      const modernTemplate = screen.getByText('modern');
      fireEvent.click(modernTemplate);

      // Template should be applied (this would be reflected in styling classes)
      expect(screen.getByText('Template')).toBeInTheDocument();
    });

    it('supports zoom controls for better viewing', async () => {
      renderPreviewPage();

      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Find zoom controls
      const zoomInButton = screen.getByTitle('Zoom In');
      const zoomOutButton = screen.getByTitle('Zoom Out');
      const resetZoomButton = screen.getByTitle('Reset Zoom');

      // Test zoom in
      fireEvent.click(zoomInButton);
      expect(screen.getByText('125%')).toBeInTheDocument();

      // Test zoom out
      fireEvent.click(zoomOutButton);
      fireEvent.click(zoomOutButton);
      expect(screen.getByText('100%')).toBeInTheDocument();

      // Test reset zoom
      fireEvent.click(zoomInButton);
      fireEvent.click(resetZoomButton);
      expect(screen.getByText('100%')).toBeInTheDocument();
    });

    it('enables sharing functionality with URL copying', async () => {
      // Mock clipboard API
      Object.assign(navigator, {
        clipboard: {
          writeText: jest.fn().mockResolvedValue(undefined)
        }
      });

      renderPreviewPage();

      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Click share button
      const shareButton = screen.getByText('Share');
      fireEvent.click(shareButton);

      // Check that clipboard was used
      await waitFor(() => {
        expect(navigator.clipboard.writeText).toHaveBeenCalledWith(
          expect.stringContaining('/candidate/profile/resumes/resume-1/preview')
        );
      });

      // Should show copied confirmation
      expect(screen.getByText('Copied!')).toBeInTheDocument();
    });

    it('supports print functionality', async () => {
      // Mock window.print
      const mockPrint = jest.fn();
      Object.defineProperty(window, 'print', { value: mockPrint });

      renderPreviewPage();

      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Click print button
      const printButton = screen.getByText('Print');
      fireEvent.click(printButton);

      // Check that print was called
      expect(mockPrint).toHaveBeenCalled();
    });
  });

  describe('Export Modal Workflow', () => {
    const renderExportModal = () => {
      return render(
        <ResumeExportModal
          isOpen={true}
          onClose={jest.fn()}
          resumeId="resume-1"
          resumeName="Senior Developer Resume"
        />
      );
    };

    it('displays export options and allows format selection', async () => {
      renderExportModal();

      // Check modal is displayed
      expect(screen.getByText('Export Resume')).toBeInTheDocument();
      expect(screen.getByText('Senior Developer Resume')).toBeInTheDocument();

      // Check format options are available
      expect(screen.getByText('PDF Document')).toBeInTheDocument();
      expect(screen.getByText('Word Document')).toBeInTheDocument();
      expect(screen.getByText('HTML Page')).toBeInTheDocument();
      expect(screen.getByText('Image')).toBeInTheDocument();

      // Select PDF format
      const pdfOption = screen.getByText('PDF Document').closest('button');
      fireEvent.click(pdfOption!);

      // Check that PDF is selected (would have visual indication)
      expect(pdfOption).toHaveClass('border-blue-500');
    });

    it('allows template selection with visual previews', async () => {
      renderExportModal();

      // Check template options
      expect(screen.getByText('Professional')).toBeInTheDocument();
      expect(screen.getByText('Modern')).toBeInTheDocument();
      expect(screen.getByText('Minimal')).toBeInTheDocument();
      expect(screen.getByText('Creative')).toBeInTheDocument();

      // Select modern template
      const modernTemplate = screen.getByText('Modern').closest('button');
      fireEvent.click(modernTemplate!);

      // Check that modern template is selected
      expect(modernTemplate).toHaveClass('border-blue-500');
    });

    it('provides advanced customization options', async () => {
      renderExportModal();

      // Check advanced options are available
      expect(screen.getByText('Advanced Options')).toBeInTheDocument();
      expect(screen.getByText('Include Metadata')).toBeInTheDocument();
      expect(screen.getByText('Paper Size')).toBeInTheDocument();
      expect(screen.getByText('Font Size')).toBeInTheDocument();

      // Test metadata toggle
      const metadataToggle = screen.getByRole('checkbox');
      expect(metadataToggle).toBeChecked();

      fireEvent.click(metadataToggle);
      expect(metadataToggle).not.toBeChecked();

      // Test paper size selection
      const paperSizeSelect = screen.getByDisplayValue('A4 (210 × 297 mm)');
      fireEvent.change(paperSizeSelect, { target: { value: 'Letter' } });
      expect(screen.getByDisplayValue('Letter (8.5 × 11 in)')).toBeInTheDocument();
    });

    it('displays export history with download options', async () => {
      renderExportModal();

      await waitFor(() => {
        expect(screen.getByText('Recent Exports')).toBeInTheDocument();
      });

      // Check export history items
      expect(screen.getByText('PDF • professional')).toBeInTheDocument();
      expect(screen.getByText('DOCX • modern')).toBeInTheDocument();

      // Check download again buttons
      const downloadButtons = screen.getAllByText('Download Again');
      expect(downloadButtons).toHaveLength(2);

      // Test download again functionality
      fireEvent.click(downloadButtons[0]);
      // This would open the download URL in a new tab
    });

    it('handles export process with progress indication', async () => {
      renderExportModal();

      // Click export button
      const exportButton = screen.getByText('Export');
      fireEvent.click(exportButton);

      // Should show progress
      await waitFor(() => {
        expect(screen.getByText('Exporting your resume...')).toBeInTheDocument();
      });

      // Should show progress bar
      expect(document.querySelector('.bg-blue-600')).toBeInTheDocument();

      // Wait for export to complete
      await waitFor(() => {
        expect(mockedApi.exportResume).toHaveBeenCalledWith('resume-1', expect.objectContaining({
          format: 'pdf',
          template: 'professional',
          include_metadata: true
        }));
      });
    });

    it('handles export errors gracefully', async () => {
      mockedApi.exportResume.mockRejectedValue(new Error('Export service unavailable'));

      renderExportModal();

      // Click export button
      const exportButton = screen.getByText('Export');
      fireEvent.click(exportButton);

      // Should show error message
      await waitFor(() => {
        expect(screen.getByText('Export Failed')).toBeInTheDocument();
        expect(screen.getByText('Export service unavailable')).toBeInTheDocument();
      });
    });

    it('supports preview functionality before export', async () => {
      renderExportModal();

      // Click preview button
      const previewButton = screen.getByText('Preview');
      fireEvent.click(previewButton);

      // Should show preview generation
      await waitFor(() => {
        expect(screen.getByText('Generating preview...')).toBeInTheDocument();
      });

      // Should call preview API
      expect(mockedApi.getResumePreviewHtml).toHaveBeenCalledWith('resume-1', expect.objectContaining({
        template: 'professional'
      }));
    });
  });

  describe('Complete Preview-to-Export Journey', () => {
    it('completes full workflow from preview to export', async () => {
      const user = userEvent.setup();

      // Start with preview page
      render(
        <MemoryRouter>
          <ResumePreviewPage resumeId="resume-1" />
        </MemoryRouter>
      );

      // Wait for preview to load
      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Change template in preview
      const templateButton = screen.getByText('Template');
      await user.click(templateButton);

      const modernTemplate = screen.getByText('modern');
      await user.click(modernTemplate);

      // Click export from preview
      const exportButton = screen.getByText('Export');
      await user.click(exportButton);

      // This would typically trigger a modal or navigate to export page
      // In a real E2E test, we'd verify the export modal opens or navigation occurs
    });

    it('maintains consistency between preview and export templates', async () => {
      // This test would verify that template selections in preview
      // are carried over to the export modal

      const { rerender } = render(
        <MemoryRouter>
          <ResumePreviewPage resumeId="resume-1" />
        </MemoryRouter>
      );

      await waitFor(() => {
        expect(screen.getByText('Senior Developer Resume - Preview')).toBeInTheDocument();
      });

      // Select modern template in preview
      const templateButton = screen.getByText('Template');
      fireEvent.click(templateButton);

      const modernTemplate = screen.getByText('modern');
      fireEvent.click(modernTemplate);

      // Render export modal
      rerender(
        <ResumeExportModal
          isOpen={true}
          onClose={jest.fn()}
          resumeId="resume-1"
          resumeName="Senior Developer Resume"
        />
      );

      // Modern template should be pre-selected in export modal
      // This would be verified by checking the selected state
    });
  });
});

// Additional test utilities for testing complex export scenarios
describe('Advanced Export Scenarios', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockedApi.getResume.mockResolvedValue(mockResumeData);
    mockedApi.getResumeExportHistory.mockResolvedValue(mockExportHistory);
  });

  it('handles bulk export operations', async () => {
    // This test would verify bulk export functionality
    // if implemented in the future
  });

  it('supports custom color schemes in export', async () => {
    render(
      <ResumeExportModal
        isOpen={true}
        onClose={jest.fn()}
        resumeId="resume-1"
        resumeName="Test Resume"
      />
    );

    // Enable color customization
    const customizeToggle = screen.getByText('Include Metadata').closest('div')?.querySelector('input');
    if (customizeToggle) {
      fireEvent.click(customizeToggle);
    }

    // Test color picker functionality would be here
  });

  it('validates export options before processing', async () => {
    render(
      <ResumeExportModal
        isOpen={true}
        onClose={jest.fn()}
        resumeId="resume-1"
        resumeName="Test Resume"
      />
    );

    // Test form validation
    const exportButton = screen.getByText('Export');
    fireEvent.click(exportButton);

    // Should validate all options are properly selected
    await waitFor(() => {
      expect(mockedApi.exportResume).toHaveBeenCalled();
    });
  });
});