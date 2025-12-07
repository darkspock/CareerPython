/**
 * SavedFiltersDropdown Component
 * Dropdown for managing saved filter presets
 */

import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import {
  BookmarkPlus,
  Bookmark,
  ChevronDown,
  Trash2,
  Star,
  Check,
  X,
  Filter
} from 'lucide-react';
import type { SavedFilter } from '../../hooks/useFilterState';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface SavedFiltersDropdownProps {
  savedFilters: SavedFilter[];
  onSaveFilter: (name: string) => void;
  onLoadFilter: (filterId: string) => void;
  onDeleteFilter: (filterId: string) => void;
  onSetDefault: (filterId: string | null) => void;
  onClearFilters: () => void;
  hasActiveFilters: boolean;
  activeFilterCount: number;
}

export function SavedFiltersDropdown({
  savedFilters,
  onSaveFilter,
  onLoadFilter,
  onDeleteFilter,
  onSetDefault,
  onClearFilters,
  hasActiveFilters,
  activeFilterCount
}: SavedFiltersDropdownProps) {
  const { t } = useTranslation();
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [newFilterName, setNewFilterName] = useState('');
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  const handleSave = () => {
    if (newFilterName.trim()) {
      onSaveFilter(newFilterName.trim());
      setNewFilterName('');
      setShowSaveDialog(false);
    }
  };

  const handleDelete = (filterId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirmDelete === filterId) {
      onDeleteFilter(filterId);
      setConfirmDelete(null);
    } else {
      setConfirmDelete(filterId);
      // Reset confirm state after 3 seconds
      setTimeout(() => setConfirmDelete(null), 3000);
    }
  };

  const handleSetDefault = (filterId: string, isDefault: boolean, e: React.MouseEvent) => {
    e.stopPropagation();
    onSetDefault(isDefault ? null : filterId);
  };

  const defaultFilter = savedFilters.find(f => f.isDefault);

  return (
    <div className="flex items-center gap-2">
      {/* Active Filters Badge */}
      {hasActiveFilters && (
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
            <Filter className="w-3 h-3 mr-1" />
            {activeFilterCount} {t('filters.active', 'active')}
          </span>
          <button
            onClick={onClearFilters}
            className="text-sm text-gray-500 hover:text-gray-700 underline"
          >
            {t('filters.clearAll', 'Clear all')}
          </button>
        </div>
      )}

      {/* Saved Filters Dropdown */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <Bookmark className="w-4 h-4" />
            {t('filters.savedFilters', 'Saved Filters')}
            {savedFilters.length > 0 && (
              <span className="ml-1 px-1.5 py-0.5 text-xs bg-gray-100 rounded-full">
                {savedFilters.length}
              </span>
            )}
            <ChevronDown className="w-4 h-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-64">
          {/* Save Current Filters */}
          {showSaveDialog ? (
            <div className="p-2">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={newFilterName}
                  onChange={(e) => setNewFilterName(e.target.value)}
                  placeholder={t('filters.enterName', 'Enter filter name...')}
                  className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleSave();
                    if (e.key === 'Escape') {
                      setShowSaveDialog(false);
                      setNewFilterName('');
                    }
                  }}
                />
                <button
                  onClick={handleSave}
                  disabled={!newFilterName.trim()}
                  className="p-1 text-green-600 hover:text-green-700 disabled:text-gray-400"
                >
                  <Check className="w-4 h-4" />
                </button>
                <button
                  onClick={() => {
                    setShowSaveDialog(false);
                    setNewFilterName('');
                  }}
                  className="p-1 text-gray-500 hover:text-gray-700"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            <DropdownMenuItem
              onClick={() => setShowSaveDialog(true)}
              disabled={!hasActiveFilters}
              className="gap-2"
            >
              <BookmarkPlus className="w-4 h-4" />
              {t('filters.saveCurrentFilters', 'Save current filters')}
            </DropdownMenuItem>
          )}

          {savedFilters.length > 0 && <DropdownMenuSeparator />}

          {/* List of Saved Filters */}
          {savedFilters.length === 0 ? (
            <div className="px-2 py-4 text-center text-sm text-gray-500">
              {t('filters.noSavedFilters', 'No saved filters yet')}
            </div>
          ) : (
            savedFilters.map((filter) => (
              <div
                key={filter.id}
                className="flex items-center gap-2 px-2 py-1.5 hover:bg-gray-100 cursor-pointer group"
                onClick={() => onLoadFilter(filter.id)}
              >
                <Bookmark className={`w-4 h-4 ${filter.isDefault ? 'text-yellow-500 fill-yellow-500' : 'text-gray-400'}`} />
                <span className="flex-1 text-sm truncate">{filter.name}</span>

                {/* Set as Default Button */}
                <button
                  onClick={(e) => handleSetDefault(filter.id, !!filter.isDefault, e)}
                  className={`p-1 opacity-0 group-hover:opacity-100 transition-opacity ${
                    filter.isDefault ? 'text-yellow-500' : 'text-gray-400 hover:text-yellow-500'
                  }`}
                  title={filter.isDefault ? t('filters.removeDefault', 'Remove as default') : t('filters.setAsDefault', 'Set as default')}
                >
                  <Star className={`w-3.5 h-3.5 ${filter.isDefault ? 'fill-yellow-500' : ''}`} />
                </button>

                {/* Delete Button */}
                <button
                  onClick={(e) => handleDelete(filter.id, e)}
                  className={`p-1 opacity-0 group-hover:opacity-100 transition-opacity ${
                    confirmDelete === filter.id ? 'text-red-600' : 'text-gray-400 hover:text-red-600'
                  }`}
                  title={confirmDelete === filter.id ? t('filters.confirmDelete', 'Click again to confirm') : t('filters.delete', 'Delete')}
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))
          )}

          {/* Default Filter Info */}
          {defaultFilter && (
            <>
              <DropdownMenuSeparator />
              <div className="px-2 py-1.5 text-xs text-gray-500">
                <Star className="w-3 h-3 inline-block mr-1 text-yellow-500 fill-yellow-500" />
                {t('filters.defaultInfo', 'Default filter loads automatically')}
              </div>
            </>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

export default SavedFiltersDropdown;
