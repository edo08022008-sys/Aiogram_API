import asyncio
from aiogram.types import FSInputFile, Message
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram import F, Router
import aiohttp

API_TOKEN = '5218494224:AAGCrCN70T0Swnp3t4QQa6_EZxLcINhQKMI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ---
async def get_product(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None
            
            data = await resp.json()
            return data 

# ---

@router.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! Это бот отвечающий за интернет магазин!\nВведите ID товара к примеру /product ID.")

@router.message(Command("product"))
async def get_product_cmd(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer("Используйте /product 1")
        return
    
    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer("ID должен быть числом")
        return
    
    await message.answer(f"Ищу товар с ID: {product_id}")

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer("Не удалось обратиться к серверу.")
        return
    
    if product is None:
        await message.answer("Товар не найден.")
        return
    
    title = product.get("title", "Без названия")
    price = product.get("price", "-")
    desc = product.get("description", "Без description")
    category = product.get("category", "Без category")
    image = product.get("image")

    text = (
        f"<b>{title}</b>\n\n"
        f"Категория: <i>{category}</i>\n"
        f"Цена: <b>{price}$</b>\n"
        f"{desc}"
    )
    photo = FSInputFile("belo.jpg")
    await message.answer_photo(photo= photo, caption=text, parse_mode="HTML")

async def main():
    bot = Bot(token=API_TOKEN)
    print('start...')
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())    