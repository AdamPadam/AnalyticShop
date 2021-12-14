from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class User(IDModelMixin):
    username: str = Field(default='Unknown', title='username of user', max_length=30)
    password: str = Field(default='', title='password of user', max_length=20)
    first_name: Optional[str] = Field(default=None, title='first name of user', max_length=30)
    last_name: Optional[str] = Field(default=None, title='last name of user', max_length=30)
    birth_date: Optional[date] = Field(default=None, title='birth date of user')

    def filter(
            self,
            username: Optional[str],
            first_name: Optional[str],
            last_name: Optional[str],
            birth_date: Optional[date]
    ):
        if username is not None and username not in self.username:
            return False
        if first_name is not None and self.first_name != first_name:
            return False
        if last_name is not None and self.last_name != last_name:
            return False
        if birth_date is not None and self.birth_date != birth_date:
            return False
        return True


class InsertUser(BaseModel):
    username: str = Field(default='Unknown', title='username of user', max_length=30)
    password: str = Field(default='', title='password of user', max_length=20)
    first_name: Optional[str] = Field(default=None, title='first name of user', max_length=30)
    last_name: Optional[str] = Field(default=None, title='last name of user', max_length=30)
    birth_date: Optional[date] = Field(default=None, title='birth date of user')


class UpdateUser(BaseModel):
    password: Optional[str] = Field(default=None, title='password of user')
    first_name: Optional[str] = Field(default=None, title='first name of user')
    last_name: Optional[str] = Field(default=None, title='last name of user')
    birth_date: Optional[date] = Field(default=None, title='birth date of user')
