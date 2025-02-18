from pyrogram import filters, types

from src.common import app
from src.service.deposit import DepositService
from src.service.gift import GiftService


@app.on_message(filters.star_gift)
async def process_gift(client, message: types.Message):
    if message.gift:
        gift = message.gift

        await DepositService.add_gift_deposit(
            message_id=1,
            user_id=message.from_user.id,
            gift_id=gift.id,
        )

        await GiftService.add_gift(
            gift_id=gift.id,
            title=gift.title,
            collectible_id=gift.collectible_id,
            lottie_url='',
        )

        await GiftService.add_user_gift(user_id=message.from_user.id, gift_id=gift.id)


if __name__ == '__main__':
    app.run()
