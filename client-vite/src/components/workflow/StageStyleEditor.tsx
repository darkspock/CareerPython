import React, { useState } from 'react';
import { Palette, Type, Image, Check, X } from 'lucide-react';
import type { StageStyle, UpdateStageStyleRequest } from '../../types/stageStyle';

interface StageStyleEditorProps {
  stageStyle: StageStyle;
  onSave: (style: UpdateStageStyleRequest) => void;
  onCancel: () => void;
  isOpen: boolean;
}

const PREDEFINED_COLORS = [
  '#374151', '#6B7280', '#9CA3AF', '#D1D5DB', '#F3F4F6', // Grays
  '#065F46', '#10B981', '#34D399', '#6EE7B7', '#D1FAE5', // Greens
  '#991B1B', '#DC2626', '#F87171', '#FCA5A5', '#FEE2E2', // Reds
  '#1E40AF', '#3B82F6', '#60A5FA', '#93C5FD', '#DBEAFE', // Blues
  '#92400E', '#F59E0B', '#FBBF24', '#FDE68A', '#FEF3C7', // Ambers
  '#7C2D12', '#EA580C', '#FB923C', '#FDBA74', '#FED7AA', // Oranges
  '#581C87', '#8B5CF6', '#A78BFA', '#C4B5FD', '#EDE9FE', // Purples
];

const PREDEFINED_ICONS = [
  '📋', '📝', '📄', '📊', '📈', '📉', '📌', '📍', '🔍', '👀',
  '✅', '✔️', '❌', '❎', '⚠️', '⚡', '🔥', '💡', '🎯', '🚀',
  '⚙️', '🔧', '🛠️', '🔨', '⚒️', '🔩', '💻', '📱', '💾', '🎮',
  '👤', '👥', '👨‍💼', '👩‍💼', '👨‍💻', '👩‍💻', '🎓', '🎖️', '🏆', '⭐',
  '📞', '📧', '💬', '📢', '📣', '🔔', '📬', '📭', '📮', '📪',
];

export const StageStyleEditor: React.FC<StageStyleEditorProps> = ({
  stageStyle,
  onSave,
  onCancel,
  isOpen
}) => {
  const [icon, setIcon] = useState(stageStyle.icon);
  const [color, setColor] = useState(stageStyle.color);
  const [backgroundColor, setBackgroundColor] = useState(stageStyle.background_color);
  const [customIcon, setCustomIcon] = useState('');
  const [showCustomIcon, setShowCustomIcon] = useState(false);

  const handleSave = () => {
    const updatedStyle: UpdateStageStyleRequest = {
      icon: icon !== stageStyle.icon ? icon : undefined,
      color: color !== stageStyle.color ? color : undefined,
      background_color: backgroundColor !== stageStyle.background_color ? backgroundColor : undefined,
    };

    // Only save if there are actual changes
    if (updatedStyle.icon || updatedStyle.color || updatedStyle.background_color) {
      onSave(updatedStyle);
    } else {
      onCancel();
    }
  };

  const handleIconSelect = (selectedIcon: string) => {
    setIcon(selectedIcon);
    setShowCustomIcon(false);
  };

  const handleCustomIconSubmit = () => {
    if (customIcon.trim()) {
      setIcon(customIcon.trim());
      setCustomIcon('');
      setShowCustomIcon(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <Palette className="w-5 h-5" />
            Edit Stage Style
          </h3>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Preview */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-gray-700 mb-3">Preview</h4>
            <div 
              className="p-4 rounded-lg border-2 border-dashed border-gray-300"
              style={{ 
                backgroundColor: backgroundColor,
                color: color 
              }}
            >
              <div className="flex items-center gap-2">
                <span 
                  className="text-lg"
                  dangerouslySetInnerHTML={{ __html: icon }}
                />
                <span className="font-semibold">Stage Name</span>
                <span 
                  className="px-2 py-1 text-xs font-medium rounded-full"
                  style={{ 
                    backgroundColor: color + '20',
                    color: color 
                  }}
                >
                  (5)
                </span>
              </div>
            </div>
          </div>

          {/* Icon Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              <Image className="w-4 h-4 inline mr-1" />
              Icon
            </label>
            
            <div className="grid grid-cols-10 gap-2 mb-4">
              {PREDEFINED_ICONS.map((predefinedIcon) => (
                <button
                  key={predefinedIcon}
                  onClick={() => handleIconSelect(predefinedIcon)}
                  className={`p-2 text-lg rounded border-2 transition-colors ${
                    icon === predefinedIcon
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {predefinedIcon}
                </button>
              ))}
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => setShowCustomIcon(!showCustomIcon)}
                className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
              >
                {showCustomIcon ? 'Hide' : 'Custom Icon'}
              </button>
              {showCustomIcon && (
                <div className="flex gap-2 flex-1">
                  <input
                    type="text"
                    value={customIcon}
                    onChange={(e) => setCustomIcon(e.target.value)}
                    placeholder="Enter emoji, HTML icon, or SVG"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <button
                    onClick={handleCustomIconSubmit}
                    className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    Add
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Color Selection */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Text Color */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                <Type className="w-4 h-4 inline mr-1" />
                Text Color
              </label>
              
              <div className="space-y-3">
                <div className="grid grid-cols-5 gap-2">
                  {PREDEFINED_COLORS.map((predefinedColor) => (
                    <button
                      key={predefinedColor}
                      onClick={() => setColor(predefinedColor)}
                      className={`w-8 h-8 rounded border-2 transition-all ${
                        color === predefinedColor
                          ? 'border-gray-900 scale-110'
                          : 'border-gray-200 hover:border-gray-400'
                      }`}
                      style={{ backgroundColor: predefinedColor }}
                    />
                  ))}
                </div>
                
                <div className="flex gap-2">
                  <input
                    type="color"
                    value={color}
                    onChange={(e) => setColor(e.target.value)}
                    className="w-12 h-8 border border-gray-300 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={color}
                    onChange={(e) => setColor(e.target.value)}
                    placeholder="#000000"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Background Color */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                <Palette className="w-4 h-4 inline mr-1" />
                Background Color
              </label>
              
              <div className="space-y-3">
                <div className="grid grid-cols-5 gap-2">
                  {PREDEFINED_COLORS.map((predefinedColor) => (
                    <button
                      key={predefinedColor}
                      onClick={() => setBackgroundColor(predefinedColor)}
                      className={`w-8 h-8 rounded border-2 transition-all ${
                        backgroundColor === predefinedColor
                          ? 'border-gray-900 scale-110'
                          : 'border-gray-200 hover:border-gray-400'
                      }`}
                      style={{ backgroundColor: predefinedColor }}
                    />
                  ))}
                </div>
                
                <div className="flex gap-2">
                  <input
                    type="color"
                    value={backgroundColor}
                    onChange={(e) => setBackgroundColor(e.target.value)}
                    className="w-12 h-8 border border-gray-300 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={backgroundColor}
                    onChange={(e) => setBackgroundColor(e.target.value)}
                    placeholder="#ffffff"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-200">
          <button
            onClick={onCancel}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 flex items-center gap-2"
          >
            <Check className="w-4 h-4" />
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};
