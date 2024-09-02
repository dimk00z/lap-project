# Learn Python Advanced project

This project is a web application built using the Litestar framework. It includes user registration, authentication, and profile management features. Below are the details of the functionality and setup.

## Features

- **User Registration**: Register a new user with an email and password.
- **User Authentication**: Authenticate an existing user using email and password. A JWT token is provided upon successful login.
- **User Profile**: Display user profiles with avatars and other profile data. Profiles are publicly accessible.
- **Profile Editing**: Users can edit their own profiles.

## Models

The project uses SQLAlchemy for database ORM. Below is the `User` model used in the application:

```python
class User(UUIDAuditBase):
    __tablename__ = "user_account"
    __table_args__ = {"comment": "User accounts for application access"}
    __pii_columns__ = {"name", "email", "avatar_url"}

    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    hashed_password: Mapped[str | None] = mapped_column(
        String(length=255), nullable=True, default=None
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(length=500), nullable=True, default=None
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    verified_at: Mapped[date] = mapped_column(nullable=True, default=None)
    joined_at: Mapped[date] = mapped_column(default=datetime.now)
    login_count: Mapped[int] = mapped_column(default=0)

    # ORM Relationships
    roles: Mapped[list[UserRole]] = relationship(
        back_populates="user",
        lazy="selectin",
        uselist=True,
        cascade="all, delete",
    )

    oauth_accounts: Mapped[list[UserOauthAccount]] = relationship(
        back_populates="user",
        lazy="noload",
        cascade="all, delete",
        uselist=True,
    )
```

## API Endpoints

```
/api/v1/health
/api/v1/liveness
/api/v1/access/login
/api/v1/access/logout
/api/v1/access/signup
/api/v1/me
/api/v1/users
/api/v1/users/{user_id:uuid}
/api/v1/users/{user_id:uuid}
/api/v1/users/{user_id:uuid}
/api/v1/users
```

## Setup and Deployment

### Prerequisites

- Docker
- Make

### Build and Run

To build and run the application, use the following commands:

```sh
make build
make up
```

## Project Structure

This project follows the recommended structure by the Litestar team.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact [dimk00z@gmail.com].

---

Feel free to adjust the content according to your project's specific details and requirements.