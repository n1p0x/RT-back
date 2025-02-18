import asyncio

from src.repo.fill import FillRepo


async def main():
    await FillRepo.fill()


if __name__ == '__main__':
    asyncio.run(main())
