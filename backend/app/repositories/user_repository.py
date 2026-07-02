from app.models.user import User


class UserRepository:

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        return await User.find_one(
            User.email == email
        )

    async def get_by_id(
        self,
        user_id: str,
    ) -> User | None:

        return await User.get(user_id)

    async def create(
        self,
        user: User,
    ) -> User:

        await user.insert()

        return user

    async def update(
        self,
        user: User,
    ) -> User:

        await user.save()

        return user


user_repository = UserRepository()