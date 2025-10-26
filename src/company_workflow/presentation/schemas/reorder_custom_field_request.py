from pydantic import BaseModel, Field


class ReorderCustomFieldRequest(BaseModel):
    """Request schema for reordering a custom field"""
    new_order_index: int = Field(..., description="New position in field list")

    class Config:
        json_schema_extra = {
            "example": {
                "new_order_index": 3
            }
        }
