"""
Get Company Page By ID Query - Query para obtener página por ID
"""
from dataclasses import dataclass

from src.shared.application.query_bus import Query


@dataclass(frozen=True)
class GetCompanyPageByIdQuery(Query):
    """Query para obtener una página de empresa por ID"""

    page_id: str
