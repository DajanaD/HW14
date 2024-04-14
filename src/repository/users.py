from typing import Union

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by their email address.

    :param email: Email address of the user.
    :param db: Database session object.
    :return: User object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user.

    :param body: User data model object.
    :param db: Database session object.
    :return: Newly created user object.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update the refresh token for a user.

    :param user: User object.
    :param token: New refresh token or None.
    :param db: Database session object.
    :return: None.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirm a user's email address.

    :param email: Email address of the user.
    :param db: Database session object.
    :return: None.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update the avatar URL for a user.

    :param email: Email address of the user.
    :param url: New avatar URL.
    :param db: Database session object.
    :return: Updated user object.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
