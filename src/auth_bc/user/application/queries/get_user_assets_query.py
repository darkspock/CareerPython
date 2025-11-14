from dataclasses import dataclass
from typing import List, Optional

from src.auth_bc.user.domain.entities.user_asset import UserAsset
from src.auth_bc.user.domain.enums.asset_enums import AssetTypeEnum
from src.auth_bc.user.domain.repositories.user_asset_repository_interface import UserAssetRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetUserAssetsQuery(Query):
    user_id: UserId
    asset_type: Optional[AssetTypeEnum] = None


class GetUserAssetsQueryHandler(QueryHandler[GetUserAssetsQuery, List[UserAsset]]):
    def __init__(self, repository: UserAssetRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetUserAssetsQuery) -> List[UserAsset]:
        """Handle get user assets query"""
        if query.asset_type:
            return self.repository.get_by_user_and_type(query.user_id, query.asset_type)
        else:
            return self.repository.get_by_user_id(query.user_id)
