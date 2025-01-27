import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()


ABIS_DIR = os.path.join(ROOT_DIR, 'abis')
LOG_DIR = os.path.join(ROOT_DIR, "log")
DATA_DIR = os.path.join(ROOT_DIR, "data")

FILED_PATH = os.path.join(LOG_DIR, 'filed.txt')
LOG_PATH = os.path.join(LOG_DIR, 'log.log')
PRIVATE_KEYS_PATH = os.path.join(DATA_DIR, "private_keys.txt")
PROXIES_PATH = os.path.join(DATA_DIR, "proxies.txt")

SEPOLIA_RPC = 'https://ethereum-sepolia-rpc.publicnode.com'
SINGULARITY_RPC = 'https://rpc-testnet.singularityfinance.ai/'

DECIMALS = 5
DECIMALS = 10 ** DECIMALS

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://www.singularityfinance.ai',
    'Priority': 'u=1, i',
    'Referer:': 'https://www.singularityfinance.ai/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

RANDOM_WALLETS = [
           '0x170a8452a04828D0a2fa31b926420F1a9EA94857',
           '0x767888a515807ed320580ee25C06519C7b54Fd3a',
           '0x67Ff9D4897776158B7868044C08296475A4e0d9B',
           '0x17b3277f8691a197b5643fD6D953DAd32afDaf58',
           '0x2FB36E0442D9B37Cd900915E8f8ef625037a3145',
           '0xA8c0e7E7632FB164Cd2b60d91e76D9E2D6e8B67a',
           '0x0B511866314670E46b79F8D3eC9e4D48c35F37C2',
           '0x6943Dce04772E91161D510a1A868C0295B285d70',
           '0xf62f176A4562bce9eEe97eFC56950F93Bd589a9b',
           '0x170a8452a04828D0a2fa31b926420F1a9EA94857',
           '0xbC66FF8594077Db2e9840Cf071C2eb422c9a7a95',
           '0x13a1C7B76659CA65aD1EA15852a788182e63b7df',
           '0x767888a515807ed320580ee25C06519C7b54Fd3a']

URL = (
    'https://staking-service.singularityfinance.ai/staking/v1/pools'
    '/deposit/751/0x22Dbdc9e8dd7C5E409B014BBcb53a3ef39736515/{wallet}'
)