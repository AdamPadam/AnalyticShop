from datetime import datetime

from pydantic import BaseModel, Field

from uuid import UUID


class IDModelMixin(BaseModel):
    id: UUID = Field(UUID('00000000-0000-0000-0000-000000000000'), alias="id")
    created: datetime
