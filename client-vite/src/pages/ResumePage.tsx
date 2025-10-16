/**
 * Resume Page Component
 *
 * Main page for resume management functionality.
 * Integrates all resume-related components and features.
 */

import React, { useEffect } from 'react';
import ResumeManagement from '../components/resume/ResumeManagement';

const ResumePage: React.FC = () => {
  useEffect(() => {
    document.title = 'Resume Management - CareerPython';
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <ResumeManagement />
      </div>
    </div>
  );
};

export default ResumePage;