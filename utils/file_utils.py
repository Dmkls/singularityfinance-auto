import json
from configs.constants import PRIVATE_KEYS_PATH, PROXIES_PATH, FILED_PATH

def read_json(path: str, encoding: str | None = None) -> list | dict:
    return json.load(open(path, encoding=encoding))


def read_file(path: str):
    with open(path, encoding='utf-8') as file:
        return [line.strip() for line in file]


def read_private_keys() -> list[str]:
    return read_file(PRIVATE_KEYS_PATH)


def read_proxies() -> list[str]:
    return read_file(PROXIES_PATH)


def write_filed_account(wallet_address: str):
    with open(FILED_PATH, 'a', encoding="utf-8") as f:
        f.write(f'{wallet_address}\n')