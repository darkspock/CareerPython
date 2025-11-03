/**
 * Talent Pool Page Component
 * Phase 8: Main page for managing company talent pool
 */

import React, { useState, useEffect } from 'react';
import type { TalentPoolEntry, TalentPoolStatus } from '../../../types/talentPool';
import { TalentPoolStatus as StatusEnum, getTalentPoolStatusLabel } from '../../../types/talentPool';
import { TalentPoolCard } from './TalentPoolCard';
import { TalentPoolService } from '../../../services/talentPoolService';

interface TalentPoolPageProps {
  companyId: string;
  onAddCandidate?: () => void;
  onViewEntry?: (entry: TalentPoolEntry) => void;
  onEditEntry?: (entry: TalentPoolEntry) => void;
}

type FilterTab = 'all' | TalentPoolStatus;

export const TalentPoolPage: React.FC<TalentPoolPageProps> = ({
  companyId,
  onAddCandidate,
  onViewEntry,
  onEditEntry
}) => {
  const [entries, setEntries] = useState<TalentPoolEntry[]>([]);
  const [filteredEntries, setFilteredEntries] = useState<TalentPoolEntry[]>([]);
  const [activeTab, setActiveTab] = useState<FilterTab>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [minRating, setMinRating] = useState<number | undefined>();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  // Get unique tags from all entries
  const allTags = Array.from(
    new Set(entries.flatMap((entry) => entry.tags))
  ).sort();

  // Load entries
  const loadEntries = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const filters = {
        search_term: searchTerm || undefined,
        tags: selectedTags.length > 0 ? selectedTags : undefined,
        min_rating: minRating
      };

      const fetchedEntries = searchTerm
        ? await TalentPoolService.searchEntries(companyId, filters)
        : await TalentPoolService.listEntries(companyId, filters);

      setEntries(fetchedEntries);
    } catch (err) {
      setError('Failed to load talent pool entries');
      console.error('Error loading entries:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadEntries();
  }, [companyId, searchTerm, selectedTags, minRating]);

  // Filter entries based on active tab
  useEffect(() => {
    let filtered = entries;

    if (activeTab !== 'all') {
      filtered = filtered.filter((e) => e.status === activeTab);
    }

    setFilteredEntries(filtered);
  }, [entries, activeTab]);

  // Handle remove from talent pool
  const handleRemove = async (entry: TalentPoolEntry) => {
    try {
      setActionLoading(entry.id);
      await TalentPoolService.removeFromTalentPool(entry.id);
      await loadEntries();
    } catch (err) {
      alert('Failed to remove entry');
      console.error('Error removing entry:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Handle change status
  const handleChangeStatus = async (entry: TalentPoolEntry) => {
    const newStatus = prompt(
      'Enter new status (active, contacted, hired, not_interested, archived):'
    );
    if (!newStatus) return;

    try {
      setActionLoading(entry.id);
      await TalentPoolService.changeStatus(entry.id, { status: newStatus as TalentPoolStatus });
      await loadEntries();
    } catch (err) {
      alert('Failed to change status');
      console.error('Error changing status:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Calculate stats
  const stats = {
    total: entries.length,
    active: entries.filter((e) => e.status === StatusEnum.ACTIVE).length,
    contacted: entries.filter((e) => e.status === StatusEnum.CONTACTED).length,
    hired: entries.filter((e) => e.status === StatusEnum.HIRED).length,
    archived: entries.filter((e) => e.status === StatusEnum.ARCHIVED).length
  };

  if (isLoading && entries.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading talent pool...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 font-medium">{error}</p>
          <button
            onClick={loadEntries}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Talent Pool</h1>
          <p className="text-sm text-gray-600 mt-1">
            Manage your pool of talented candidates for future opportunities
          </p>
        </div>
        {onAddCandidate && (
          <button
            onClick={onAddCandidate}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Add Candidate
          </button>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <p className="text-sm text-gray-600">Total</p>
          <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-green-200 p-4">
          <p className="text-sm text-gray-600">Active</p>
          <p className="text-2xl font-bold text-green-600">{stats.active}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-blue-200 p-4">
          <p className="text-sm text-gray-600">Contacted</p>
          <p className="text-2xl font-bold text-blue-600">{stats.contacted}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-purple-200 p-4">
          <p className="text-sm text-gray-600">Hired</p>
          <p className="text-2xl font-bold text-purple-600">{stats.hired}</p>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-yellow-200 p-4">
          <p className="text-sm text-gray-600">Archived</p>
          <p className="text-2xl font-bold text-yellow-600">{stats.archived}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        {/* Filter Tabs */}
        <div className="flex flex-wrap items-center gap-2 mb-4">
          <button
            onClick={() => setActiveTab('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All ({stats.total})
          </button>
          <button
            onClick={() => setActiveTab(StatusEnum.ACTIVE)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === StatusEnum.ACTIVE
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Active ({stats.active})
          </button>
          <button
            onClick={() => setActiveTab(StatusEnum.CONTACTED)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === StatusEnum.CONTACTED
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Contacted ({stats.contacted})
          </button>
          <button
            onClick={() => setActiveTab(StatusEnum.HIRED)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === StatusEnum.HIRED
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Hired ({stats.hired})
          </button>
          <button
            onClick={() => setActiveTab(StatusEnum.ARCHIVED)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === StatusEnum.ARCHIVED
                ? 'bg-yellow-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Archived ({stats.archived})
          </button>
        </div>

        {/* Search and additional filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <input
            type="text"
            placeholder="Search notes and reasons..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          {/* Min Rating Filter */}
          <select
            value={minRating || ''}
            onChange={(e) => setMinRating(e.target.value ? parseInt(e.target.value) : undefined)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Ratings</option>
            <option value="5">5 stars</option>
            <option value="4">4+ stars</option>
            <option value="3">3+ stars</option>
            <option value="2">2+ stars</option>
            <option value="1">1+ stars</option>
          </select>

          {/* Tags Filter (simplified) */}
          <div className="flex items-center gap-2">
            <select
              value=""
              onChange={(e) => {
                const tag = e.target.value;
                if (tag && !selectedTags.includes(tag)) {
                  setSelectedTags([...selectedTags, tag]);
                }
              }}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Add tag filter...</option>
              {allTags.map((tag) => (
                <option key={tag} value={tag}>
                  {tag}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Selected Tags */}
        {selectedTags.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4">
            {selectedTags.map((tag) => (
              <span
                key={tag}
                className="px-3 py-1 bg-blue-100 text-blue-800 border border-blue-200 rounded-full text-sm flex items-center gap-2"
              >
                {tag}
                <button
                  onClick={() => setSelectedTags(selectedTags.filter((t) => t !== tag))}
                  className="hover:text-blue-900"
                >
                  ×
                </button>
              </span>
            ))}
            <button
              onClick={() => setSelectedTags([])}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Entries Grid */}
      {filteredEntries.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
          <p className="text-gray-500 mb-4">
            {searchTerm || selectedTags.length > 0 || minRating
              ? 'No entries match your filters'
              : activeTab === 'all'
              ? 'No talent pool entries yet'
              : `No ${getTalentPoolStatusLabel(activeTab as TalentPoolStatus)} entries`}
          </p>
          {!searchTerm && activeTab === 'all' && onAddCandidate && (
            <button
              onClick={onAddCandidate}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Add Your First Candidate
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredEntries.map((entry) => (
            <TalentPoolCard
              key={entry.id}
              entry={entry}
              onView={onViewEntry}
              onEdit={onEditEntry}
              onChangeStatus={handleChangeStatus}
              onRemove={handleRemove}
              isLoading={actionLoading === entry.id}
            />
          ))}
        </div>
      )}
    </div>
  );
};
