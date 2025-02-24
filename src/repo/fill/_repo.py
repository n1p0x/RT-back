from src.db import new_session, User, Collection, Nft


class Repo:
    @staticmethod
    async def fill_user():
        async with new_session() as session:
            rows = [User(id=6165565929)]

            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def fill_collection():
        async with new_session() as session:
            rows = [
                Collection(
                    id=1,
                    name='Plush Pepes',
                    address='EQCCAGc9G1zBzDYyVRE_Zu2m47jSeC0UvRoVijOg8_BcylJP',
                    img_url='https://nft.fragment.com/collection/plushpepe.webp',
                )
            ]

            session.add_all(rows)
            await session.commit()

    @staticmethod
    async def fill():
        # await Repo.fill_user()
        await Repo.fill_collection()
