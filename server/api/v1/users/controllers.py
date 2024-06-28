from datetime import date
from uuid import UUID

from advanced_alchemy.exceptions import NotFoundError
from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from loguru import logger
from passlib.hash import bcrypt
from pydantic import BaseModel as _BaseModel

from server.api.v1.users.models import User
from server.api.v1.users.repository import UserRepository, provide_users_repo


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""

    model_config = {"from_attributes": True}


class UserDTO(BaseModel):
    username: str
    full_name: str
    birthdate: date
    avatar_url: str


class SavedUserDTO(UserDTO):
    id: UUID | None


class RegisterUserDTO(UserDTO):
    password: str


class UserController(Controller):
    path = "/"
    dependencies = {"users_repo": Provide(provide_users_repo)}

    @get(
        path="/{user_id:uuid}",
    )
    async def get_user(
        self,
        users_repo: UserRepository,
        user_id: UUID = Parameter(
            title="User ID",
            description="The user to retrieve.",
        ),
    ) -> SavedUserDTO:
        """Get an existing author."""
        # acee7068-1569-402f-9155-d83d79c0e1f1

        try:
            user = await users_repo.get(user_id)
        except NotFoundError as ex:
            raise NotFoundException(detail="User not found") from ex
        return SavedUserDTO.model_validate(user)

    @post(
        path="/",
    )
    @logger.catch(reraise=True)
    async def register_user(
        self,
        data: RegisterUserDTO,
        users_repo: UserRepository,
    ) -> SavedUserDTO:
        """Get users count."""

        password_hash = bcrypt.hash(data.password)
        new_user = User(
            username=data.username,
            password_hash=password_hash,
            full_name=data.full_name,
            birthdate=data.birthdate,
            avatar_url=data.avatar_url,
        )
        await users_repo.add(
            data=new_user,
        )
        await users_repo.session.commit()

        logger.debug("User created: {user}", user=new_user)
        return SavedUserDTO.model_validate(new_user)

    @patch(
        path="/{user_id:uuid}",
    )
    async def update_author(
        self,
        users_repo: UserRepository,
        data: UserDTO,
        user_id: UUID = Parameter(
            title="User ID",
            description="The user to retrieve.",
        ),
    ) -> SavedUserDTO:
        """Update an author."""
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": user_id})
        obj = await users_repo.update(User(**raw_obj))
        await users_repo.session.commit()
        return SavedUserDTO.model_validate(obj)
