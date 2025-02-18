from tonutils.wallet import HighloadWalletV3
from tonutils.client import ToncenterClient
from tonutils.utils import to_amount

from src.common import app, config
from src.repo.withdraw import WithdrawRepo


class Service:
    @staticmethod
    async def add_ton_withdraw(user_id: int, destination: str, amount: int) -> None:
        await Service.send_ton(destination=destination, amount=amount)

        await WithdrawRepo.add_ton_withdraw(user_id, destination, amount)

    @staticmethod
    async def add_nft_withdraw(
        user_id: int, destination: str, nft_address: str
    ) -> None:
        await Service.send_nft(destination=destination, nft_address=nft_address)

        await WithdrawRepo.add_nft_withdraw(user_id, destination, nft_address)

    @staticmethod
    async def add_gift_withdraw(user_id: int, gift_id: int) -> None:
        await Service.send_gift(user_id=user_id, gift_id=gift_id)

        await WithdrawRepo.add_gift_withdraw(user_id, gift_id)

    @staticmethod
    async def get_client() -> ToncenterClient:
        return ToncenterClient(
            api_key=(
                config.TONCENTER_API_KEY_TESTNET
                if config.IS_TESTNET
                else config.TONCENTER_API_KEY
            ),
            is_testnet=config.IS_TESTNET,
        )

    @staticmethod
    async def get_wallet() -> HighloadWalletV3:
        wallet, _, _, _ = HighloadWalletV3.from_mnemonic(
            client=ToncenterClient(
                api_key=(
                    config.TONCENTER_API_KEY_TESTNET
                    if config.IS_TESTNET
                    else config.TONCENTER_API_KEY
                ),
                is_testnet=config.IS_TESTNET,
            ),
            mnemonic=[],
        )

        return wallet

    @staticmethod
    async def send_ton(destination: str, amount: int) -> None:
        wallet = await Service.get_wallet()

        await wallet.transfer(destination=destination, amount=to_amount(amount))

    @staticmethod
    async def send_nft(destination: str, nft_address: str) -> None:
        wallet = await Service.get_wallet()

        await wallet.transfer_nft(
            destination=destination,
            nft_address=nft_address,
            response_address=config.WALLET_ADDRESS,
        )

    @staticmethod
    async def send_gift(user_id: int, gift_id: int) -> None:
        await app.connect()

        await app.send_gift(chat_id=user_id, gift_id=gift_id)
