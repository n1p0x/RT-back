import asyncio

from src.service.deposit import DepositService


async def main():
    await DepositService.check_nft_deposit()


if __name__ == '__main__':
    asyncio.run(main())
