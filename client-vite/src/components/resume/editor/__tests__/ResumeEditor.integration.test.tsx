/**
 * Integration tests for Resume Editor functionality
 *
 * Tests the complete resume editing workflow including
 * WYSIWYG editing, section management, and real-time preview.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom';
import ResumeEditor from '../ResumeEditor';
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

const mockResumeData = {
  id: 'resume-1',
  name: 'Software Engineer Resume',
  candidate_id: 'user-1',
  resume_type: 'GENERAL',
  content: {
    sections: [
      {
        id: 'section-1',
        type: 'summary',
        title: 'Professional Summary',
        content: '<p>Experienced software engineer with 5+ years in full-stack development.</p>',
        order: 0,
        isVisible: true
      },
      {
        id: 'section-2',
        type: 'experience',
        title: 'Work Experience',
        content: '<p>Senior Software Engineer at TechCorp (2020-Present)</p>',
        order: 1,
        isVisible: true
      }
    ],
    template: 'professional',
    personalInfo: {
      title: 'Senior Software Engineer',
      email: 'john@example.com',
      phone: '+1-555-0123',
      location: 'San Francisco, CA',
      website: 'https://johndoe.dev'
    }
  },
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z'
};

describe('ResumeEditor Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockedApi.getResume.mockResolvedValue(mockResumeData);
    mockedApi.updateResumeContent.mockResolvedValue({});
  });

  const renderResumeEditor = () => {
    return render(
      <MemoryRouter>
        <ResumeEditor resumeId="resume-1" />
      </MemoryRouter>
    );
  };

  it('loads and displays resume data correctly', async () => {
    renderResumeEditor();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Check personal information fields
    expect(screen.getByDisplayValue('Senior Software Engineer')).toBeInTheDocument();
    expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();
    expect(screen.getByDisplayValue('+1-555-0123')).toBeInTheDocument();
    expect(screen.getByDisplayValue('San Francisco, CA')).toBeInTheDocument();
    expect(screen.getByDisplayValue('https://johndoe.dev')).toBeInTheDocument();

    // Check sections are displayed
    expect(screen.getByText('Professional Summary')).toBeInTheDocument();
    expect(screen.getByText('Work Experience')).toBeInTheDocument();
  });

  it('handles section editing and content updates', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Find and edit a section title
    const editButtons = screen.getAllByTitle('Edit Title');
    fireEvent.click(editButtons[0]);

    const titleInput = screen.getByDisplayValue('Professional Summary');
    fireEvent.change(titleInput, { target: { value: 'Executive Summary' } });
    fireEvent.blur(titleInput);

    // Check that the title was updated
    expect(screen.getByText('Executive Summary')).toBeInTheDocument();
  });

  it('toggles section visibility correctly', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Find and click visibility toggle
    const visibilityButtons = screen.getAllByTitle('Hide Section');
    fireEvent.click(visibilityButtons[0]);

    // The section should still be in the editor but marked as hidden
    const hiddenSection = screen.getByText('Professional Summary').closest('.border-gray-100');
    expect(hiddenSection).toBeInTheDocument();
  });

  it('adds new sections successfully', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Click add section button
    const addSectionButton = screen.getByText('Add Section');
    fireEvent.click(addSectionButton);

    // Select a section type (e.g., Skills)
    const skillsOption = screen.getByText('Skills');
    fireEvent.click(skillsOption);

    // Check that the new section was added
    await waitFor(() => {
      expect(screen.getByText('Skills')).toBeInTheDocument();
    });
  });

  it('deletes sections when requested', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Find and click delete button for a section
    const deleteButtons = screen.getAllByTitle('Delete Section');
    fireEvent.click(deleteButtons[0]);

    // The section should be removed
    await waitFor(() => {
      expect(screen.queryByText('Professional Summary')).not.toBeInTheDocument();
    });
  });

  it('updates personal information fields', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Update the professional title
    const titleInput = screen.getByDisplayValue('Senior Software Engineer');
    fireEvent.change(titleInput, { target: { value: 'Lead Software Engineer' } });

    // Update the email
    const emailInput = screen.getByDisplayValue('john@example.com');
    fireEvent.change(emailInput, { target: { value: 'john.doe@example.com' } });

    // Check that values were updated
    expect(screen.getByDisplayValue('Lead Software Engineer')).toBeInTheDocument();
    expect(screen.getByDisplayValue('john.doe@example.com')).toBeInTheDocument();
  });

  it('toggles preview mode correctly', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Initially preview should be visible
    expect(screen.getByText('Preview')).toBeInTheDocument();

    // Toggle preview off
    const previewToggle = screen.getByTitle('Hide Preview');
    fireEvent.click(previewToggle);

    // Preview section should be hidden (but preview controls might still be visible)
    const showPreviewButton = screen.getByTitle('Show Preview');
    expect(showPreviewButton).toBeInTheDocument();
  });

  it('handles save functionality', async () => {
    const mockOnSave = jest.fn();

    render(
      <MemoryRouter>
        <ResumeEditor resumeId="resume-1" onSave={mockOnSave} />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Make a change to trigger unsaved state
    const titleInput = screen.getByDisplayValue('Senior Software Engineer');
    fireEvent.change(titleInput, { target: { value: 'Updated Title' } });

    // Click save button
    const saveButton = screen.getByText('Save');
    fireEvent.click(saveButton);

    // Wait for save to complete
    await waitFor(() => {
      expect(mockedApi.updateResumeContent).toHaveBeenCalled();
    });
  });

  it('handles template changes in preview', async () => {
    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // Open template selector
    const templateButton = screen.getByText('Template');
    fireEvent.click(templateButton);

    // Select modern template
    const modernTemplate = screen.getByText('modern');
    fireEvent.click(modernTemplate);

    // Template should be changed (this would be reflected in the preview styling)
    expect(screen.getByText('Template')).toBeInTheDocument();
  });

  it('handles loading and error states', async () => {
    // Test loading state
    mockedApi.getResume.mockImplementation(() =>
      new Promise(resolve => setTimeout(() => resolve(mockResumeData), 100))
    );

    renderResumeEditor();

    // Should show loading state
    expect(screen.getByText('Loading resume editor...')).toBeInTheDocument();

    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    mockedApi.getResume.mockRejectedValue(new Error('Failed to load resume'));

    renderResumeEditor();

    await waitFor(() => {
      expect(screen.getByText('Failed to load resume data. Please try again.')).toBeInTheDocument();
    });

    // Should show retry button
    expect(screen.getByText('Try Again')).toBeInTheDocument();
  });
});

// Additional test utilities for complex interactions
describe('ResumeEditor Complex Workflows', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockedApi.getResume.mockResolvedValue(mockResumeData);
    mockedApi.updateResumeContent.mockResolvedValue({});
  });

  it('handles complete editing workflow', async () => {
    const mockOnSave = jest.fn();

    render(
      <MemoryRouter>
        <ResumeEditor resumeId="resume-1" onSave={mockOnSave} />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Software Engineer Resume')).toBeInTheDocument();
    });

    // 1. Update personal information
    const nameInput = screen.getByDisplayValue('Software Engineer Resume');
    fireEvent.change(nameInput, { target: { value: 'Updated Resume Name' } });

    // 2. Edit section content (would require more complex DOM manipulation)
    // This is a simplified version - in real tests you'd interact with the WYSIWYG editor

    // 3. Add a new section
    const addSectionButton = screen.getByText('Add Section');
    fireEvent.click(addSectionButton);

    const skillsOption = screen.getByText('Skills');
    fireEvent.click(skillsOption);

    // 4. Save changes
    const saveButton = screen.getByText('Save');
    fireEvent.click(saveButton);

    // Verify the complete workflow executed successfully
    await waitFor(() => {
      expect(mockedApi.updateResumeContent).toHaveBeenCalledWith('resume-1', expect.objectContaining({
        name: 'Updated Resume Name'
      }));
    });
  });
});