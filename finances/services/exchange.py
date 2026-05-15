"""
Сервіс для роботи з Open Exchange Rates API.
Безкоштовний план дає тільки USD як base currency,
тому крос-курси (EUR↔UAH) рахуємо через USD на нашому боці.
"""

import logging
from decimal import Decimal

from django.conf import settings
from django.core.cache import cache

import requests

logger = logging.getLogger(__name__)

API_URL = "https://openexchangerates.org/api/latest.json"
CACHE_KEY = "openexchangerates:latest"
CACHE_TTL = 60 * 60 * 6  # 6 годин — Free план оновлюється раз на годину
SUPPORTED_CURRENCIES = ("UAH", "USD", "EUR")


class ExchangeRateError(Exception):
    """Сервіс не зміг отримати курси (нема ключа, API недоступний, ліміт)."""


def _fetch_rates_from_api() -> dict:
    """Йде в API і повертає курси відносно USD."""
    app_id = settings.OPENEXCHANGERATES_APP_ID
    if not app_id:
        raise ExchangeRateError("OPENEXCHANGERATES_APP_ID не налаштований у .env")

    try:
        response = requests.get(
            API_URL,
            params={"app_id": app_id, "symbols": ",".join(SUPPORTED_CURRENCIES)},
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("OpenExchangeRates request failed: %s", exc)
        raise ExchangeRateError("Не вдалося отримати курси з API") from exc

    data = response.json()
    rates = data.get("rates", {})

    # Перевіримо що є усі потрібні валюти
    missing = [c for c in SUPPORTED_CURRENCIES if c not in rates and c != "USD"]
    if missing:
        raise ExchangeRateError(f"API не повернув курси для: {missing}")

    # USD до USD = 1 (API його не повертає, бо він base)
    rates["USD"] = 1.0
    return rates


def get_rates_to_uah() -> dict:
    """
    Повертає словник {currency: rate_to_uah}, де rate_to_uah —
    скільки UAH коштує 1 одиниця валюти.

    Кешує результат на 6 годин. На помилці кидає ExchangeRateError.
    """
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached

    raw_rates = _fetch_rates_from_api()
    # raw_rates: курси відносно USD, наприклад {"UAH": 41.5, "EUR": 0.92, "USD": 1.0}
    # Треба перерахувати в UAH-base: скільки UAH коштує 1 одиниця валюти

    usd_to_uah = Decimal(str(raw_rates["UAH"]))

    rates_to_uah = {
        "UAH": Decimal("1"),
        "USD": usd_to_uah,
        "EUR": usd_to_uah / Decimal(str(raw_rates["EUR"])),
    }

    cache.set(CACHE_KEY, rates_to_uah, CACHE_TTL)
    logger.info("Refreshed exchange rates: %s", rates_to_uah)
    return rates_to_uah


def convert_to_uah(amount: Decimal, currency: str) -> Decimal:
    """Конвертує суму у вказаній валюті в UAH."""
    rates = get_rates_to_uah()
    rate = rates.get(currency)
    if rate is None:
        raise ExchangeRateError(f"Невідома валюта: {currency}")
    return (amount * rate).quantize(Decimal("0.01"))
