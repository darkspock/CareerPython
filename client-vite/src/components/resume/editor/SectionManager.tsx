/**
 * Section Manager Component
 *
 * Manages resume sections with drag-and-drop reordering,
 * section editing capabilities, and section type management.
 */

import React, { useState, useCallback } from 'react';
import {
  GripVertical,
  Plus,
  Trash2,
  Edit2,
  Eye,
  ChevronDown,
  ChevronRight,
  User,
  Briefcase,
  GraduationCap,
  Code,
  Award,
  Users,
  Globe,
  FileText
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import WYSIWYGEditor from './WYSIWYGEditor';

interface ResumeSection {
  id: string;
  type: SectionType;
  title: string;
  content: string;
  order: number;
  isVisible: boolean;
  isExpanded?: boolean;
}

type SectionType =
  | 'summary'
  | 'experience'
  | 'education'
  | 'skills'
  | 'projects'
  | 'certifications'
  | 'languages'
  | 'references'
  | 'custom';

interface SectionManagerProps {
  sections: ResumeSection[];
  onSectionsChange: (sections: ResumeSection[]) => void;
  onSectionContentChange: (sectionId: string, content: string) => void;
  className?: string;
  saving?: boolean;
}

const SECTION_ICONS: Record<SectionType, React.ComponentType<any>> = {
  summary: User,
  experience: Briefcase,
  education: GraduationCap,
  skills: Code,
  projects: FileText,
  certifications: Award,
  languages: Globe,
  references: Users,
  custom: FileText
};

const SECTION_TEMPLATES: Record<SectionType, string> = {
  summary: 'Write a compelling professional summary that highlights your key strengths and career objectives.',
  experience: 'Describe your work experience, including job titles, companies, dates, and key accomplishments.',
  education: 'List your educational background, including degrees, institutions, and graduation dates.',
  skills: 'Highlight your technical and soft skills relevant to your target position.',
  projects: 'Showcase significant projects you\'ve worked on, including technologies used and outcomes achieved.',
  certifications: 'List relevant certifications, licenses, and professional credentials.',
  languages: 'Indicate your language proficiencies and fluency levels.',
  references: 'Provide professional references or indicate they are available upon request.',
  custom: 'Add any additional information relevant to your application.'
};

const SectionManager: React.FC<SectionManagerProps> = ({
  sections,
  onSectionsChange,
  onSectionContentChange,
  className = '',
  saving = false
}) => {
  const [draggedSection, setDraggedSection] = useState<string | null>(null);
  const [editingSection, setEditingSection] = useState<string | null>(null);
  const [showAddSection, setShowAddSection] = useState(false);

  const handleDragStart = (e: React.DragEvent, sectionId: string) => {
    setDraggedSection(sectionId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = useCallback((e: React.DragEvent, targetSectionId: string) => {
    e.preventDefault();

    if (!draggedSection || draggedSection === targetSectionId) return;

    const draggedIndex = sections.findIndex(s => s.id === draggedSection);
    const targetIndex = sections.findIndex(s => s.id === targetSectionId);

    if (draggedIndex === -1 || targetIndex === -1) return;

    const newSections = [...sections];
    const [removed] = newSections.splice(draggedIndex, 1);
    newSections.splice(targetIndex, 0, removed);

    // Update order values
    const updatedSections = newSections.map((section, index) => ({
      ...section,
      order: index
    }));

    onSectionsChange(updatedSections);
    setDraggedSection(null);
  }, [sections, draggedSection, onSectionsChange]);

  const toggleSectionVisibility = (sectionId: string) => {
    const updatedSections = sections.map(section =>
      section.id === sectionId
        ? { ...section, isVisible: !section.isVisible }
        : section
    );
    onSectionsChange(updatedSections);
  };

  const toggleSectionExpansion = (sectionId: string) => {
    const updatedSections = sections.map(section =>
      section.id === sectionId
        ? { ...section, isExpanded: !section.isExpanded }
        : section
    );
    onSectionsChange(updatedSections);
  };

  const deleteSection = (sectionId: string) => {
    const updatedSections = sections.filter(section => section.id !== sectionId);
    onSectionsChange(updatedSections);
  };

  const addSection = (type: SectionType, title: string) => {
    const newSection: ResumeSection = {
      id: `section-${Date.now()}`,
      type,
      title,
      content: SECTION_TEMPLATES[type],
      order: sections.length,
      isVisible: true,
      isExpanded: true
    };

    onSectionsChange([...sections, newSection]);
    setShowAddSection(false);
  };

  const updateSectionTitle = (sectionId: string, newTitle: string) => {
    const updatedSections = sections.map(section =>
      section.id === sectionId
        ? { ...section, title: newTitle }
        : section
    );
    onSectionsChange(updatedSections);
  };

  const sortedSections = [...sections].sort((a, b) => a.order - b.order);

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Resume Sections</h3>
        <button
          onClick={() => setShowAddSection(true)}
          className="inline-flex items-center px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Section
        </button>
      </div>

      {/* Sections List */}
      <div className="space-y-2">
        <AnimatePresence>
          {sortedSections.map((section) => {
            const IconComponent = SECTION_ICONS[section.type];
            const isEditing = editingSection === section.id;
            const isExpanded = section.isExpanded !== false;

            return (
              <motion.div
                key={section.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`border rounded-lg ${
                  section.isVisible ? 'border-gray-200 bg-white' : 'border-gray-100 bg-gray-50'
                } ${draggedSection === section.id ? 'opacity-50' : ''}`}
                draggable
                onDragStart={(e) => handleDragStart(e, section.id)}
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, section.id)}
              >
                {/* Section Header */}
                <div className="flex items-center gap-3 p-4">
                  <div className="cursor-move text-gray-400 hover:text-gray-600">
                    <GripVertical className="w-5 h-5" />
                  </div>

                  <div className={`p-2 rounded-lg ${section.isVisible ? 'bg-blue-100' : 'bg-gray-100'}`}>
                    <IconComponent className={`w-4 h-4 ${section.isVisible ? 'text-blue-600' : 'text-gray-400'}`} />
                  </div>

                  <div className="flex-1">
                    {isEditing ? (
                      <input
                        type="text"
                        value={section.title}
                        onChange={(e) => updateSectionTitle(section.id, e.target.value)}
                        onBlur={() => setEditingSection(null)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') setEditingSection(null);
                          if (e.key === 'Escape') setEditingSection(null);
                        }}
                        className="w-full px-2 py-1 text-base font-medium border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        autoFocus
                      />
                    ) : (
                      <h4 className={`text-base font-medium ${section.isVisible ? 'text-gray-900' : 'text-gray-500'}`}>
                        {section.title}
                      </h4>
                    )}
                    <p className="text-sm text-gray-500 capitalize">{section.type} section</p>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => toggleSectionExpansion(section.id)}
                      className="p-1 text-gray-400 hover:text-gray-600 rounded"
                      title={isExpanded ? 'Collapse' : 'Expand'}
                    >
                      {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                    </button>

                    <button
                      onClick={() => setEditingSection(section.id)}
                      className="p-1 text-gray-400 hover:text-gray-600 rounded"
                      title="Edit Title"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>

                    <button
                      onClick={() => toggleSectionVisibility(section.id)}
                      className={`p-1 rounded transition-colors ${
                        section.isVisible
                          ? 'text-blue-600 hover:text-blue-700'
                          : 'text-gray-400 hover:text-gray-600'
                      }`}
                      title={section.isVisible ? 'Hide Section' : 'Show Section'}
                    >
                      <Eye className="w-4 h-4" />
                    </button>

                    <button
                      onClick={() => deleteSection(section.id)}
                      className="p-1 text-gray-400 hover:text-red-600 rounded"
                      title="Delete Section"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Section Content Editor */}
                {isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-t border-gray-200"
                  >
                    <div className="p-4">
                      <WYSIWYGEditor
                        content={section.content}
                        onChange={(content) => onSectionContentChange(section.id, content)}
                        placeholder={SECTION_TEMPLATES[section.type]}
                        showPreview={false}
                        saving={saving}
                      />
                    </div>
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Add Section Modal */}
      {showAddSection && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg shadow-xl w-full max-w-md"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Add New Section</h3>
                <button
                  onClick={() => setShowAddSection(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>

              <div className="space-y-3">
                {Object.entries(SECTION_ICONS).map(([type, Icon]) => (
                  <button
                    key={type}
                    onClick={() => addSection(type as SectionType, type.charAt(0).toUpperCase() + type.slice(1))}
                    className="w-full flex items-center gap-3 p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <Icon className="w-5 h-5 text-gray-600" />
                    <div>
                      <div className="font-medium text-gray-900 capitalize">{type}</div>
                      <div className="text-sm text-gray-500">{SECTION_TEMPLATES[type as SectionType].substring(0, 50)}...</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default SectionManager;