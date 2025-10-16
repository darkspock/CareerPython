/**
 * WYSIWYG Test Page
 *
 * Page to test the new WYSIWYG editor functionality without interfering
 * with existing resume editing functionality.
 */

import React from 'react';
import WysiwygTestPage from '../components/resume/editor/WysiwygTestPage';

const WysiwygTestPageRoute: React.FC = () => {
  return <WysiwygTestPage />;
};

export default WysiwygTestPageRoute;