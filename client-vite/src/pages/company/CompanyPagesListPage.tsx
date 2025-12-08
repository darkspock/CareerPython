import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, FileText, Grid, List } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
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
          <p className="text-muted-foreground mt-1">Gestiona las páginas de contenido de tu empresa</p>
        </div>
        <Button onClick={() => navigate('/company/pages/create')}>
          <Plus className="w-4 h-4 mr-2" />
          Nueva Página
        </Button>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  type="text"
                  placeholder="Buscar páginas..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            {/* Page Type Filter */}
            <div className="lg:w-64">
              <Select
                value={selectedPageType}
                onValueChange={(value) => setSelectedPageType(value as keyof typeof PageType | '')}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Todos los tipos" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos los tipos</SelectItem>
                  {PAGE_TYPE_OPTIONS.map(option => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Status Filter */}
            <div className="lg:w-48">
              <Select
                value={selectedStatus}
                onValueChange={(value) => setSelectedStatus(value as keyof typeof PageStatus | '')}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Todos los estados" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos los estados</SelectItem>
                  {PAGE_STATUS_OPTIONS.map(option => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2">
              <Button onClick={handleSearch}>
                <Search className="w-4 h-4 mr-2" />
                Buscar
              </Button>
              <Button variant="outline" onClick={handleClearFilters}>
                Limpiar
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* View Mode Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">
            {total} página{total !== 1 ? 's' : ''} encontrada{total !== 1 ? 's' : ''}
          </span>
        </div>
        <div className="flex items-center gap-1 bg-muted rounded-lg p-1">
          <Button
            variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
            size="icon"
            onClick={() => setViewMode('grid')}
          >
            <Grid className="w-4 h-4" />
          </Button>
          <Button
            variant={viewMode === 'list' ? 'secondary' : 'ghost'}
            size="icon"
            onClick={() => setViewMode('list')}
          >
            <List className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-muted-foreground mt-2">Cargando páginas...</p>
          </div>
        </div>
      ) : pages.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No hay páginas</h3>
            <p className="text-muted-foreground mb-4">Comienza creando tu primera página de contenido.</p>
            <Button onClick={() => navigate('/company/pages/create')}>
              <Plus className="w-4 h-4 mr-2" />
              Crear Primera Página
            </Button>
          </CardContent>
        </Card>
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
              <Button
                variant="outline"
                size="sm"
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
              >
                Anterior
              </Button>

              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <Button
                  key={page}
                  variant={page === currentPage ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => handlePageChange(page)}
                >
                  {page}
                </Button>
              ))}

              <Button
                variant="outline"
                size="sm"
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                Siguiente
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
