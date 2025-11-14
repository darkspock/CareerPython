"""
Get Company Page By Type Query - Query para obtener página por tipo
"""
from dataclasses import dataclass

from src.framework.application.query_bus import Query


@dataclass(frozen=True)
class GetCompanyPageByTypeQuery(Query):
    """Query para obtener una página de empresa por tipo"""

    company_id: str
    page_type: str
