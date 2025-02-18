import aiohttp

from ._models import Collection, UserNft, Nft
from src.common import config
from src.repo.nft import NftRepo


class Service:
    @staticmethod
    async def get_collections() -> list[Collection] | None:
        if not (collections := await NftRepo.get_collections()):
            return

        return [
            Collection.model_validate(collection, from_attributes=True)
            for collection in collections
        ]

    @staticmethod
    async def get_user_nft(user_nft_id: int) -> UserNft | None:
        if not (user_nft := await NftRepo.get_user_nft(user_nft_id)):
            return

        return UserNft.model_validate(user_nft, from_attributes=True)

    @staticmethod
    async def add_nft(
        title: str,
        collectible_id: int,
        address: str,
        lottie_url: str,
        collection_id: int,
    ) -> int | None:
        return await NftRepo.add_nft(
            title, collectible_id, address, lottie_url, collection_id
        )

    @staticmethod
    async def add_user_nft(user_id: int, nft_id: int) -> None:
        await NftRepo.add_user_nft(user_id, nft_id)

    @staticmethod
    async def get_wallet_nfts(wallet: str, collection_address: str) -> list[Nft] | None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if config.IS_TESTNET
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/nft/items'
        headers = {
            'X-Api-Key': (
                config.TONCENTER_API_KEY_TESTNET
                if config.IS_TESTNET
                else config.TONCENTER_API_KEY
            )
        }
        params = {'owner_address': wallet, 'collection_address': collection_address}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                if not (nft_items := res['nft_items']) or not len(nft_items):
                    return

            nfts: list[Nft] = []
            for nft_item in nft_items:
                async with session.get(url=nft_item['content']['uri']) as resp:
                    metadata = await resp.json()

                title, index = metadata['name'].split('#')

                nfts.append(
                    Nft(
                        title=title,
                        collectible_id=index,
                        address=nft_item['address'],
                        lottie_url=metadata['lottie'],
                        collection_id=1,
                    )
                )

            return nfts

    @staticmethod
    async def get_nft(address: str) -> Nft | None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if config.IS_TESTNET
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/nft/items'
        headers = {
            'X-Api-Key': (
                config.TONCENTER_API_KEY_TESTNET
                if config.IS_TESTNET
                else config.TONCENTER_API_KEY
            )
        }
        params = {
            'address': address,
            'owner_address': config.WALLET_ADDRESS,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                if not (nft_item := res['nft_items']) or not len(nft_item):
                    return

                async with session.get(url=nft_item[0]['content']['uri']) as resp:
                    metadata = await resp.json()

                title, index = metadata['name'].split(' #')

                return Nft(
                    title=title,
                    collectible_id=index,
                    address=address,
                    lottie_url=metadata['lottie'],
                    collection_id=1,
                )
