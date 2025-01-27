import aiohttp
from random import choice
from utils.file_utils import read_proxies
from utils.log_utils import logger
from configs.constants import HEADERS, RANDOM_WALLETS, URL

PROXIES = read_proxies()

async def post_request(url: str, payload: dict, headers: dict, proxy: str, timeout: int = 10) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers, proxy=proxy, timeout=timeout) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error while POST request to {url}: {e}")
        except aiohttp.ContentTypeError as e:
            logger.error(f"Failed to parse JSON response from {url}: {e}")
        return {}

async def get_unlock(value: int, timeout: int = 10) -> int:
    """
    :return: Разница между датами unlockDate и lockDate в секундах.
    """
    wallet = choice(RANDOM_WALLETS)
    proxy = choice(PROXIES)
    # logger.debug(f"Selected wallet: {wallet}")

    url = URL.format(wallet=wallet)

    payload = {
        'sdao_input': str(value),
        'seconds_locked': 0
    }

    response = await post_request(url, payload, HEADERS, proxy, timeout)
    if not response:
        return -1

    try:
        return int(response['unlockDate']) - int(response['lockDate'])
    except KeyError as e:
        logger.error(f"Missing key in response: {e}")
        return -1
