/**
 * Variable Section Editor Component
 *
 * Manages individual variable resume sections using WYSIWYG editor.
 * Supports adding, editing, removing, and reordering sections.
 */

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import {
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import {
  Plus,
  Edit3,
  Trash2,
  GripVertical,
  ChevronDown,
  ChevronUp,
  Save,
  X,
  Settings
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import WysiwygEditor from '../../common/WysiwygEditor';
import type { VariableSection } from '../../../types/resume';

interface VariableSectionEditorProps {
  sections: VariableSection[];
  onUpdateSection: (key: string, content: string, title?: string) => void;
  onAddSection: (key: string, title: string, content: string) => void;
  onRemoveSection: (key: string) => void;
  onReorderSections: (sectionsOrder: Array<{key: string; order: number}>) => void;
  disabled?: boolean;
  className?: string;
}

interface NewSectionForm {
  key: string;
  title: string;
  content: string;
}

interface SortableSectionProps {
  section: VariableSection;
  index: number;
  totalSections: number;
  expandedSections: Set<string>;
  editingSection: string | null;
  onToggleSection: (key: string) => void;
  onContentChange: (key: string, content: string) => void;
  onTitleEdit: (key: string, title: string) => void;
  onRemoveSection: (key: string) => void;
  onMoveSection: (key: string, direction: 'up' | 'down') => void;
  onSetEditingSection: (key: string | null) => void;
  disabled: boolean;
}

const SortableSection: React.FC<SortableSectionProps> = ({
  section,
  index,
  totalSections,
  expandedSections,
  editingSection,
  onToggleSection,
  onContentChange,
  onTitleEdit,
  onRemoveSection,
  onMoveSection,
  onSetEditingSection,
  disabled
}) => {
  const { t } = useTranslation();
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: section.key });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      layout
      className="bg-white border border-gray-200 rounded-lg overflow-hidden"
    >
      {/* Section Header */}
      <div className="flex items-center justify-between p-4 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1">
            <button
              onClick={() => onMoveSection(section.key, 'up')}
              disabled={index === 0}
              className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
              title={t('resume.moveUp')}
            >
              <ChevronUp className="w-4 h-4" />
            </button>
            <button
              onClick={() => onMoveSection(section.key, 'down')}
              disabled={index === totalSections - 1}
              className="p-1 text-gray-400 hover:text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed"
              title={t('resume.moveDown')}
            >
              <ChevronDown className="w-4 h-4" />
            </button>
            <div
              {...attributes}
              {...listeners}
              className="p-1 cursor-grab active:cursor-grabbing touch-none"
              title={t('resume.dragToReorder')}
            >
              <GripVertical className="w-4 h-4 text-gray-400 hover:text-gray-600" />
            </div>
          </div>

          <div className="flex items-center gap-2">
            {editingSection === section.key ? (
              <input
                type="text"
                defaultValue={section.title}
                onBlur={(e) => onTitleEdit(section.key, e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    onTitleEdit(section.key, e.currentTarget.value);
                  } else if (e.key === 'Escape') {
                    onSetEditingSection(null);
                  }
                }}
                className="px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                autoFocus
              />
            ) : (
              <h4 className="font-medium text-gray-900">{section.title}</h4>
            )}
            <span className="text-xs text-gray-500">({section.key})</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onSetEditingSection(section.key)}
            className="p-1 text-gray-400 hover:text-gray-600"
            title={t('resume.editTitle')}
          >
            <Edit3 className="w-4 h-4" />
          </button>
          <button
            onClick={() => onRemoveSection(section.key)}
            className="p-1 text-red-400 hover:text-red-600"
            title={t('resume.removeSection')}
          >
            <Trash2 className="w-4 h-4" />
          </button>
          <button
            onClick={() => onToggleSection(section.key)}
            className="p-1 text-gray-400 hover:text-gray-600"
          >
            {expandedSections.has(section.key) ? (
              <ChevronUp className="w-4 h-4" />
            ) : (
              <ChevronDown className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>

      {/* Section Content */}
      <AnimatePresence>
        {expandedSections.has(section.key) && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="p-4"
          >
            <WysiwygEditor
              content={section.content}
              onChange={(content) => onContentChange(section.key, content)}
              placeholder={t('resume.enterContentPlaceholder', { title: section.title })}
              minHeight="150px"
              disabled={disabled}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

const VariableSectionEditor: React.FC<VariableSectionEditorProps> = ({
  sections,
  onUpdateSection,
  onAddSection,
  onRemoveSection,
  onReorderSections,
  disabled = false,
  className = ''
}) => {
  const { t } = useTranslation();
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [editingSection, setEditingSection] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newSection, setNewSection] = useState<NewSectionForm>({
    key: '',
    title: '',
    content: ''
  });

  // Sort sections by order
  const sortedSections = [...sections].sort((a, b) => a.order - b.order);

  // Drag & Drop sensors
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Handle drag end
  const handleDragEnd = (event: any) => {
    const { active, over } = event;

    if (active.id !== over?.id) {
      const oldIndex = sortedSections.findIndex(section => section.key === active.id);
      const newIndex = sortedSections.findIndex(section => section.key === over?.id);

      const reorderedSections = arrayMove(sortedSections, oldIndex, newIndex);

      // Create new order mapping
      const newOrder = reorderedSections.map((section, index) => ({
        key: section.key,
        order: index + 1
      }));

      onReorderSections(newOrder);
    }
  };

  const toggleSection = (key: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(key)) {
      newExpanded.delete(key);
    } else {
      newExpanded.add(key);
    }
    setExpandedSections(newExpanded);
  };

  const handleContentChange = (key: string, content: string) => {
    onUpdateSection(key, content);
  };

  const handleTitleEdit = (key: string, newTitle: string) => {
    const section = sections.find(s => s.key === key);
    if (section) {
      onUpdateSection(key, section.content, newTitle);
    }
    setEditingSection(null);
  };

  const handleAddSection = () => {
    if (!newSection.key || !newSection.title) return;

    // Check if key already exists
    if (sections.some(s => s.key === newSection.key)) {
      alert(t('resume.sectionAlreadyExists'));
      return;
    }

    onAddSection(newSection.key, newSection.title, newSection.content);
    setNewSection({ key: '', title: '', content: '' });
    setShowAddForm(false);
  };

  const handleRemoveSection = (key: string) => {
    if (confirm(t('resume.removeSectionConfirm'))) {
      onRemoveSection(key);
    }
  };

  const moveSection = (key: string, direction: 'up' | 'down') => {
    const sectionIndex = sortedSections.findIndex(s => s.key === key);
    if (sectionIndex === -1) return;

    const targetIndex = direction === 'up' ? sectionIndex - 1 : sectionIndex + 1;
    if (targetIndex < 0 || targetIndex >= sortedSections.length) return;

    // Create new order mapping
    const newOrder = sortedSections.map((section, index) => {
      if (index === sectionIndex) {
        return { key: sortedSections[targetIndex].key, order: index + 1 };
      } else if (index === targetIndex) {
        return { key: section.key, order: index + 1 };
      } else {
        return { key: section.key, order: index + 1 };
      }
    });

    onReorderSections(newOrder);
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 bg-gray-50 border border-gray-200 rounded-lg">
        <div className="flex items-center gap-3">
          <Settings className="w-5 h-5 text-gray-600" />
          <h4 className="font-medium text-gray-900">{t('resume.resumeSections')}</h4>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          disabled={disabled}
          className="inline-flex items-center px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Plus className="w-4 h-4 mr-1" />
          {t('resume.addSection')}
        </button>
      </div>

      {/* Add Section Form */}
      <AnimatePresence>
        {showAddForm && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-blue-50 border border-blue-200 rounded-lg p-4"
          >
            <h4 className="text-sm font-medium text-gray-900 mb-3">{t('resume.addNewSection')}</h4>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    {t('resume.sectionKey')}
                  </label>
                  <input
                    type="text"
                    value={newSection.key}
                    onChange={(e) => setNewSection({ ...newSection, key: e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, '') })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder={t('resume.sectionKeyPlaceholder')}
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    {t('resume.sectionTitle')}
                  </label>
                  <input
                    type="text"
                    value={newSection.title}
                    onChange={(e) => setNewSection({ ...newSection, title: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder={t('resume.sectionTitlePlaceholder')}
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  {t('resume.initialContent')}
                </label>
                <WysiwygEditor
                  content={newSection.content}
                  onChange={(content) => setNewSection({ ...newSection, content })}
                  placeholder={t('resume.sectionContentPlaceholder')}
                  minHeight="100px"
                />
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={handleAddSection}
                  disabled={!newSection.key || !newSection.title}
                  className="inline-flex items-center px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Save className="w-4 h-4 mr-1" />
                  {t('common.save')}
                </button>
                <button
                  onClick={() => {
                    setShowAddForm(false);
                    setNewSection({ key: '', title: '', content: '' });
                  }}
                  className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  <X className="w-4 h-4 mr-1" />
                  {t('common.cancel')}
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Sections List with Drag & Drop */}
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={sortedSections.map(section => section.key)}
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-3">
            {sortedSections.map((section, index) => (
              <SortableSection
                key={section.key}
                section={section}
                index={index}
                totalSections={sortedSections.length}
                expandedSections={expandedSections}
                editingSection={editingSection}
                onToggleSection={toggleSection}
                onContentChange={handleContentChange}
                onTitleEdit={handleTitleEdit}
                onRemoveSection={handleRemoveSection}
                onMoveSection={moveSection}
                onSetEditingSection={setEditingSection}
                disabled={disabled}
              />
            ))}
          </div>
        </SortableContext>
      </DndContext>

      {sortedSections.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>{t('resume.noSectionsFound')}</p>
        </div>
      )}
    </div>
  );
};

export default VariableSectionEditor;