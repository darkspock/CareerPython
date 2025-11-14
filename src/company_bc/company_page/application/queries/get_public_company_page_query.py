"""
Get Public Company Page Query - Query para obtener página pública
"""
from dataclasses import dataclass

from src.framework.application.query_bus import Query


@dataclass(frozen=True)
class GetPublicCompanyPageQuery(Query):
    """Query para obtener una página pública de empresa"""

    company_id: str
    page_type: str
