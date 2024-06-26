import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# prices
PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500*100)  # в копейках(руб)


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if config.PAYMENTS_TOKEN.split(":")[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на 1 месяц",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency='rub',
                           photo_url='https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg',
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkpoint_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_info(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошёл успешно!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
