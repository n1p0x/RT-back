from pyrogram import filters, types

from src.common import app
from src.service.deposit import DepositService
from src.service.gift import GiftService


@app.on_message(filters.star_gift)
async def process_gift(client, message: types.Message):
    print(message.id)
    if message.gift:
        gift = message.gift

        await DepositService.add_gift_deposit(
            message_id=gift.message_id,
            # user_id=gift.from_user.id,
            user_id=6165565929,
            gift_id=gift.id,
        )

        await GiftService.add_gift(
            gift_id=gift.id,
            title=gift.title,
            collectible_id=gift.collectible_id,
            lottie_url='https://nft.fragment.com/gift/evileye-215.lottie.json',
        )

        await GiftService.add_user_gift(
            # user_id=message.from_user.id,
            user_id=6165565929,
            gift_id=gift.id,
            message_id=gift.message_id,
        )


if __name__ == '__main__':
    app.run()
