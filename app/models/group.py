from typing import Optional

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Group(IDModelMixin):
    name: str = Field(default='Unnamed', title='name of group', max_length=30)
    permission_type: int = Field(default=0, title='permission type of group', ge=0)

    def filter(
            self,
            name: Optional[str],
            permission_type: Optional[int]
    ):
        if name is not None and name not in self.name:
            return False
        if permission_type is not None and self.permission_type != permission_type:
            return False
        return True


class InsertGroup(BaseModel):
    name: str = Field(default='Unnamed', title='name of group', max_length=30)
    permission_type: int = Field(default=0, title='permission type of group', ge=0)


class UpdateGroup(BaseModel):
    name: Optional[str] = Field(default=None, title='name of group')
    permission_type: Optional[int] = Field(default=None, title='permission type of group')
