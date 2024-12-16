import asyncio
import httpx
import logging
from django.core.management.base import BaseCommand
from core.models import CryptoPair
from asgiref.sync import sync_to_async

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    filename="logfile_pairs.log", level=logging.INFO, format=LOG_FORMAT, filemode="a"
)
logger = logging.getLogger(__name__)


@sync_to_async
def update_or_create_pair(symbol, base_coin, quote_coin):
    pair, created = CryptoPair.objects.update_or_create(
        name=symbol,
        defaults={
            "base_currency": base_coin,
            "quote_currency": quote_coin,
        },
    )
    logger.info(f"{'Создана' if created else 'Обновлена'} пара: {symbol}")


class Command(BaseCommand):
    help = "Загружает список всех торговых пар с Bybit API и сохраняет их в базу данных"

    async def fetch_pairs(self, client):
        url = "https://api.bybit.com/v5/market/instruments-info?category=spot"
        try:
            logger.info(f"Запрос списка пар по URL: {url}")
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            pairs = data.get("result", {}).get("list", [])
            if not pairs:
                logger.warning("Ответ API не содержит списка пар или список пуст.")
                return

            logger.info(f"Найдено {len(pairs)} пар для обновления.")
            for pair in pairs:
                symbol = pair.get("symbol")
                base_coin = pair.get("baseCoin")
                quote_coin = pair.get("quoteCoin")
                if symbol and base_coin and quote_coin:
                    await update_or_create_pair(symbol, base_coin, quote_coin)
                else:
                    logger.warning(f"Пропуск пары из-за отсутствия ключей: {pair}")

            logger.info(f"Успешно загружено {len(pairs)} пар.")
        except httpx.RequestError as e:
            logger.error(f"Ошибка сети: {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке списка пар: {e}", exc_info=True)

    async def handle_async(self):
        async with httpx.AsyncClient() as client:
            await self.fetch_pairs(client)

    def handle(self, *args, **kwargs):
        logger.info("=== Старт загрузки списка пар ===")
        asyncio.run(self.handle_async())
        logger.info("=== Завершение асинхронной загрузки списка пар ===")
