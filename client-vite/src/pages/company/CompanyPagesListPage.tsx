import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, FileText, Grid, List } from 'lucide-react';
import { CompanyPageCard } from '../../components/company/CompanyPageCard';
import { companyPageService } from '../../services/companyPageService';
import type { CompanyPage, CompanyPageFilters } from '../../types/companyPage';
import { PageType, PageStatus } from '../../types/companyPage';
import { PAGE_TYPE_OPTIONS, PAGE_STATUS_OPTIONS } from '../../types/companyPage';

export default function CompanyPagesListPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pages, setPages] = useState<CompanyPage[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(12);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  
  // Filters
  const [filters, setFilters] = useState<CompanyPageFilters>({
    page: 1,
    page_size: 12,
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPageType, setSelectedPageType] = useState<keyof typeof PageType | ''>('');
  const [selectedStatus, setSelectedStatus] = useState<keyof typeof PageStatus | ''>('');

  useEffect(() => {
    loadPages();
  }, [filters]);

  const loadPages = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await companyPageService.getPages(filters);
      setPages(response.pages);
      setTotal(response.total);
      setCurrentPage(response.page);
    } catch (err: any) {
      setError(err.message || 'Error al cargar las páginas');
      console.error('Error loading pages:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    setFilters(prev => ({
      ...prev,
      page: 1,
      page_type: selectedPageType || undefined,
      status: selectedStatus || undefined,
    }));
  };

  const handleClearFilters = () => {
    setSearchTerm('');
    setSelectedPageType('');
    setSelectedStatus('');
    setFilters({
      page: 1,
      page_size: 12,
    });
  };

  const handlePageChange = (page: number) => {
    setFilters(prev => ({ ...prev, page }));
  };

  const handleEdit = (pageId: string) => {
    navigate(`/company/pages/${pageId}/edit`);
  };

  const handleView = (pageId: string) => {
    navigate(`/company/pages/${pageId}/view`);
  };

  const handlePublish = async (pageId: string) => {
    try {
      await companyPageService.publishPage(pageId);
      loadPages();
    } catch (err: any) {
      setError(err.message || 'Error al publicar la página');
    }
  };

  const handleArchive = async (pageId: string) => {
    try {
      await companyPageService.archivePage(pageId);
      loadPages();
    } catch (err: any) {
      setError(err.message || 'Error al archivar la página');
    }
  };

  const handleDelete = async (pageId: string) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta página?')) {
      try {
        await companyPageService.deletePage(pageId);
        loadPages();
      } catch (err: any) {
        setError(err.message || 'Error al eliminar la página');
      }
    }
  };

  const handleSetDefault = async (pageId: string) => {
    try {
      await companyPageService.setDefaultPage(pageId);
      loadPages();
    } catch (err: any) {
      setError(err.message || 'Error al establecer como página por defecto');
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Páginas de Contenido</h1>
          <p className="text-gray-600 mt-1">Gestiona las páginas de contenido de tu empresa</p>
        </div>
        <button
          onClick={() => navigate('/company/pages/create')}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Nueva Página
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Buscar páginas..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Page Type Filter */}
          <div className="lg:w-64">
            <select
              value={selectedPageType}
                    onChange={(e) => setSelectedPageType(e.target.value as keyof typeof PageType | '')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Todos los tipos</option>
              {PAGE_TYPE_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Status Filter */}
          <div className="lg:w-48">
            <select
              value={selectedStatus}
                    onChange={(e) => setSelectedStatus(e.target.value as keyof typeof PageStatus | '')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Todos los estados</option>
              {PAGE_STATUS_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <button
              onClick={handleSearch}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Search className="w-4 h-4" />
              Buscar
            </button>
            <button
              onClick={handleClearFilters}
              className="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Limpiar
            </button>
          </div>
        </div>
      </div>

      {/* View Mode Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">
            {total} página{total !== 1 ? 's' : ''} encontrada{total !== 1 ? 's' : ''}
          </span>
        </div>
        <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-md transition-colors ${
              viewMode === 'grid' ? 'bg-white shadow-sm' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <Grid className="w-4 h-4" />
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`p-2 rounded-md transition-colors ${
              viewMode === 'list' ? 'bg-white shadow-sm' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <List className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-gray-600 mt-2">Cargando páginas...</p>
          </div>
        </div>
      ) : pages.length === 0 ? (
        <div className="text-center py-12">
          <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No hay páginas</h3>
          <p className="text-gray-600 mb-4">Comienza creando tu primera página de contenido.</p>
          <button
            onClick={() => navigate('/company/pages/create')}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Crear Primera Página
          </button>
        </div>
      ) : (
        <>
          {/* Pages Grid/List */}
          <div className={
            viewMode === 'grid'
              ? 'grid grid-cols-1 md:grid-cols-2 gap-6'
              : 'space-y-4'
          }>
            {pages.map((page) => (
              <CompanyPageCard
                key={page.id}
                page={page}
                onEdit={handleEdit}
                onView={handleView}
                onPublish={handlePublish}
                onArchive={handleArchive}
                onDelete={handleDelete}
                onSetDefault={handleSetDefault}
              />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 mt-8">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-3 py-2 text-sm text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Anterior
              </button>
              
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => handlePageChange(page)}
                  className={`px-3 py-2 text-sm rounded-lg ${
                    page === currentPage
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-600 bg-white border border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {page}
                </button>
              ))}
              
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-3 py-2 text-sm text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Siguiente
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
