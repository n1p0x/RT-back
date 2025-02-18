import aiohttp

from ._models import NftDeposit
from src.common import config
from src.repo.deposit import DepositRepo
from src.service.nft import NftService


class Service:
    @staticmethod
    async def get_nft_deposits() -> list[NftDeposit] | None:
        if not (deposits := await DepositRepo.get_nft_deposits()):
            return

        return [
            NftDeposit.model_validate(deposit, from_attributes=True)
            for deposit in deposits
        ]

    @staticmethod
    async def add_ton_deposit(
        user_id: int, msg_hash: str, amount: int, payload: str = 'deposit'
    ) -> None:
        await DepositRepo.add_ton_deposit(user_id, msg_hash, amount, payload)

    @staticmethod
    async def add_nft_deposit(
        user_id: int,
        sender: str,
        nft_address: str,
    ) -> None:
        await DepositRepo.add_nft_deposit(user_id, sender, nft_address)

    @staticmethod
    async def add_gift_deposit(message_id: int, user_id: int, gift_id: int) -> None:
        await DepositRepo.add_gift_deposit(message_id, user_id, gift_id)

    @staticmethod
    async def get_ton_transfer(
        destination: str, start_utime: int | None = None
    ) -> None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if config.IS_TESTNET
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/messages'
        headers = {
            'X-Api-Key': (
                config.TONCENTER_API_KEY_TESTNET
                if config.IS_TESTNET
                else config.TONCENTER_API_KEY
            )
        }
        params = {
            'destination': destination,
            'start_utime': start_utime,
            'exclude_externals': True,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

    @staticmethod
    async def get_nft_transfer(owner_address: str, item_address: str) -> int | None:
        base_url = (
            'https://testnet.toncenter.com/api/v3'
            if config.IS_TESTNET
            else 'https://toncenter.com/api/v3'
        )
        url = base_url + '/nft/transfers'
        headers = {
            'X-Api-Key': (
                config.TONCENTER_API_KEY_TESTNET
                if config.IS_TESTNET
                else config.TONCENTER_API_KEY
            )
        }
        params = {'owner_address': owner_address, 'item_address': item_address}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    return

                res = await resp.json()

                if not (txs := res['nft_transfers']) or not len(txs):
                    return

                return 1

    @staticmethod
    async def check_ton_deposit() -> None:
        pass

    @staticmethod
    async def check_nft_deposit() -> None:
        if not (deposits := await Service.get_nft_deposits()):
            return

        for deposit in deposits:
            if await Service.get_nft_transfer(
                owner_address=config.WALLET_ADDRESS, item_address=deposit.nft_address
            ):
                if not (nft := await NftService.get_nft(address=deposit.nft_address)):
                    return

                if not (
                    nft_id := await NftService.add_nft(
                        title=nft.title,
                        collectible_id=nft.collectible_id,
                        address=nft.address,
                        lottie_url=nft.lottie_url,
                        collection_id=nft.collection_id,
                    )
                ):
                    return

                await NftService.add_user_nft(user_id=deposit.user_id, nft_id=nft_id)

                await DepositRepo.update_nft_deposit(nft_deposit_id=deposit.id)
