from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RawUser:
    id: str
    email: str
    name: str
    password: str
    is_superuser: bool
    is_active: bool


SUPER_USER_EMAIL = "superuser@example.com"
COMMON_USER_EMAIl = "user@example.com"


RAW_USERS: list[RawUser] = [
    RawUser(
        **{
            "id": "97108ac1-ffcb-411d-8b1e-d9183399f63b",
            "email": SUPER_USER_EMAIL,
            "name": "Super User",
            "password": "Test_Password1!",
            "is_superuser": True,
            "is_active": True,
        }
    ),
    RawUser(
        **{
            "id": "5ef29f3c-3560-4d15-ba6b-a2e5c721e4d2",
            "email": COMMON_USER_EMAIl,
            "name": "Example User",
            "password": "Test_Password2!",
            "is_superuser": False,
            "is_active": True,
        }
    ),
    RawUser(
        **{
            "id": "5ef29f3c-3560-4d15-ba6b-a2e5c721e999",
            "email": "test@test.com",
            "name": "Test User",
            "password": "Test_Password3!",
            "is_superuser": False,
            "is_active": True,
        }
    ),
    RawUser(
        **{
            "id": "6ef29f3c-3560-4d15-ba6b-a2e5c721e4d3",
            "email": "another@example.com",
            "name": "The User",
            "password": "Test_Password3!",
            "is_superuser": False,
            "is_active": True,
        }
    ),
    RawUser(
        **{
            "id": "7ef29f3c-3560-4d15-ba6b-a2e5c721e4e1",
            "email": "inactive@example.com",
            "name": "Inactive User",
            "password": "Old_Password2!",
            "is_superuser": False,
            "is_active": False,
        }
    ),
]
