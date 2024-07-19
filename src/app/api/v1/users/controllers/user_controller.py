from dataclasses import dataclass
from datetime import date

import advanced_alchemy
from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig
from litestar import Controller, get, post
from litestar.di import Provide
from litestar.dto import DataclassDTO
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST
from loguru import logger
from passlib.hash import bcrypt
from pydantic import BaseModel as _BaseModel

from server.api.v1.users.models import User
from server.api.v1.users.repository import UserRepository, provide_users_repo


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""

    model_config = {"from_attributes": True}


@dataclass
class UserRegistrationSchema:
    username: str
    full_name: str
    email: str
    birthdate: date
    avatar_url: str
    password: str


class UserRegistrationDTO(DataclassDTO[UserRegistrationSchema]):
    """User registration DTO."""


# class UserDTO(DataclassDTO):
#     username: str
#     full_name: str
#     birthdate: date
#     avatar_url: str


class UserReadDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"})


# class SavedUserDTO(UserDTO):
#     id: UUID | None


# class UserListItemDTO(UserDTO):
#     id: UUID
#     created_at: datetime.datetime
#     updated_at: datetime.datetime


# class UsersListDTO(RootModel):
#     root: list[UserListItemDTO]


# class RegisterUserDTO(UserDTO):
#     password: str


class UserController(Controller):
    path = "/"
    dependencies = {"users_repo": Provide(provide_users_repo)}

    # @get(
    #     path="/",
    # )
    # @logger.catch(reraise=True)
    # async def get_users(
    #     self,
    #     users_repo: UserRepository,
    # ) -> list[UserListItemDTO]:
    #     """Get an existing author."""
    #     users = await users_repo.list()
    #     return [UserListItemDTO.model_validate(user) for user in users]

    # @get(
    #     path="/{user_id:uuid}",
    # )
    # async def get_user(
    #     self,
    #     users_repo: UserRepository,
    #     user_id: UUID = Parameter(
    #         title="User ID",
    #         description="The user to retrieve.",
    #     ),
    # ) -> SavedUserDTO:
    #     """Get an existing author."""

    #     user = await users_repo.get_one_or_none(
    #         id=user_id,
    #     )

    #     if user:
    #         return SavedUserDTO.model_validate(user)

    #     raise NotFoundException(detail="User not found")

    @post(
        path="/",
        return_dto=UserReadDTO,
    )
    @logger.catch(reraise=True)
    async def register_user(
        self,
        data: UserRegistrationSchema,
        users_repo: UserRepository,
    ) -> User:
        """Get users count."""

        password_hash = bcrypt.hash(data.password)
        new_user = User(
            username=data.username,
            password_hash=password_hash,
            full_name=data.full_name,
            birthdate=data.birthdate,
            avatar_url=data.avatar_url,
        )
        try:
            await users_repo.add(
                data=new_user,
                auto_commit=True,
            )
        except advanced_alchemy.exceptions.RepositoryError as exc:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        logger.debug("User created: {user}", user=new_user)
        return new_user

    # @patch(
    #     path="/{user_id:uuid}",
    # )
    # async def update_user(
    #     self,
    #     users_repo: UserRepository,
    #     data: UserDTO,
    #     user_id: UUID = Parameter(
    #         title="User ID",
    #         description="The user to retrieve.",
    #     ),
    # ) -> SavedUserDTO:
    #     """Update an author."""
    #     raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
    #     raw_obj.update({"id": user_id})
    #     try:
    #         return SavedUserDTO.model_validate(
    #             users_repo.update(User(**raw_obj), auto_commit=True)
    #         )
    #     except advanced_alchemy.exceptions.RepositoryError as exc:
    #         raise HTTPException(
    #             status_code=HTTP_400_BAD_REQUEST,
    #             detail=str(exc),
    #         ) from exc

    @get(
        path="/count",
    )
    async def get_users_count(
        self,
        users_repo: UserRepository,
    ) -> int:
        """Get users count."""
        return await users_repo.count()
