from typing import Optional, Any

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.shared_bc.customization.entity_customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field import CustomField
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field_id import CustomFieldId
from src.shared_bc.customization.entity_customization.application.commands.create_entity_customization_command import CreateEntityCustomizationCommand
from src.shared_bc.customization.entity_customization.application.commands.update_entity_customization_command import UpdateEntityCustomizationCommand
from src.shared_bc.customization.entity_customization.application.commands.delete_entity_customization_command import DeleteEntityCustomizationCommand
from src.shared_bc.customization.entity_customization.application.queries.get_entity_customization_query import GetEntityCustomizationQuery
from src.shared_bc.customization.entity_customization.application.queries.get_entity_customization_by_id_query import GetEntityCustomizationByIdQuery
from adapters.http.customization.schemas.create_entity_customization_request import CreateEntityCustomizationRequest
from adapters.http.customization.schemas.update_entity_customization_request import UpdateEntityCustomizationRequest
from adapters.http.customization.schemas.entity_customization_response import EntityCustomizationResponse
from adapters.http.customization.mappers.entity_customization_mapper import EntityCustomizationResponseMapper
from src.shared_bc.customization.entity_customization.application.dtos.entity_customization_dto import EntityCustomizationDto


class EntityCustomizationController:
    """Controller for entity customization operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_entity_customization(self, request: CreateEntityCustomizationRequest) -> EntityCustomizationResponse:
        """Create a new entity customization"""
        # Validate entity_type
        try:
            entity_type_enum = EntityCustomizationTypeEnum(request.entity_type)
        except ValueError:
            raise ValueError(
                f"Invalid entity_type: '{request.entity_type}'. "
                f"Valid values are: {', '.join([e.value for e in EntityCustomizationTypeEnum])}"
            )
        
        # Convert request fields to CustomField value objects
        fields = [
            CustomField.create(
                field_key=field.field_key,
                field_name=field.field_name,
                field_type=field.field_type,
                order_index=field.order_index,
                field_config=field.field_config
            )
            for field in request.fields
        ]

        customization_id = EntityCustomizationId.generate()

        command = CreateEntityCustomizationCommand(
            id=customization_id,
            entity_type=entity_type_enum,
            entity_id=request.entity_id,
            fields=fields,
            validation=request.validation,
            metadata=request.metadata or {}
        )

        self._command_bus.dispatch(command)

        query = GetEntityCustomizationByIdQuery(id=customization_id)
        dto: Optional[EntityCustomizationDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Entity customization not found after creation")

        return EntityCustomizationResponseMapper.dto_to_response(dto)

    def get_entity_customization(self, entity_type: str, entity_id: str) -> Optional[EntityCustomizationResponse]:
        """Get an entity customization by entity type and entity ID"""
        try:
            entity_type_enum = EntityCustomizationTypeEnum(entity_type)
        except ValueError:
            raise ValueError(
                f"Invalid entity_type: '{entity_type}'. "
                f"Valid values are: {', '.join([e.value for e in EntityCustomizationTypeEnum])}"
            )
        
        query = GetEntityCustomizationQuery(
            entity_type=entity_type_enum,
            entity_id=entity_id
        )
        dto: Optional[EntityCustomizationDto] = self._query_bus.query(query)

        if not dto:
            return None

        return EntityCustomizationResponseMapper.dto_to_response(dto)

    def get_entity_customization_by_id(self, id: str) -> Optional[EntityCustomizationResponse]:
        """Get an entity customization by ID"""
        query = GetEntityCustomizationByIdQuery(id=EntityCustomizationId.from_string(id))
        dto: Optional[EntityCustomizationDto] = self._query_bus.query(query)

        if not dto:
            return None

        return EntityCustomizationResponseMapper.dto_to_response(dto)

    def update_entity_customization(
        self,
        id: str,
        request: UpdateEntityCustomizationRequest
    ) -> EntityCustomizationResponse:
        """Update an entity customization"""
        # Convert request fields to CustomField value objects if provided
        fields = None
        if request.fields is not None:
            fields = [
                CustomField.create(
                    field_key=field.field_key,
                    field_name=field.field_name,
                    field_type=field.field_type,
                    order_index=field.order_index,
                    field_config=field.field_config
                )
                for field in request.fields
            ]

        command = UpdateEntityCustomizationCommand(
            id=EntityCustomizationId.from_string(id),
            fields=fields,
            validation=request.validation,
            metadata=request.metadata
        )

        self._command_bus.dispatch(command)

        query = GetEntityCustomizationByIdQuery(id=EntityCustomizationId.from_string(id))
        dto: Optional[EntityCustomizationDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Entity customization not found after update")

        return EntityCustomizationResponseMapper.dto_to_response(dto)

    def delete_entity_customization(self, id: str) -> None:
        """Delete an entity customization"""
        command = DeleteEntityCustomizationCommand(id=EntityCustomizationId.from_string(id))
        self._command_bus.dispatch(command)

