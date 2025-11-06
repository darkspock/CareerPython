"""
List Company Pages Query - Query para listar páginas de empresa
"""
from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query


@dataclass(frozen=True)
class ListCompanyPagesQuery(Query):
    """Query para listar páginas de una empresa"""

    company_id: str
    page_type: Optional[str] = None
    status: Optional[str] = None
