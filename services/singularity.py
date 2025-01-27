from core.connections import BaseConnection
from configs.constants import SINGULARITY_RPC
from web3 import AsyncWeb3
from core.account import Account
import random
from utils.log_utils import logger
from configs.settings import *
from configs.constants import DECIMALS
import asyncio
from utils.file_utils import write_filed_account
from core.reqs import get_unlock

Singularity = BaseConnection(SINGULARITY_RPC)

def get_value(method: str) -> float:
    """
    :param method: wrap, unwrap, stake, unstake, bridge_sfi, bridge_sep
    :return: random value
    """
    return random.randint(
        int(OPERATION_LIMITS[method][0] * DECIMALS),
        int(OPERATION_LIMITS[method][1] * DECIMALS)
    ) / DECIMALS


async def get_sfi_balance(account: Account) -> float:

    wallet_address = AsyncWeb3.to_checksum_address(AsyncWeb3.to_checksum_address(account.wallet_address))
    balance_in_wei = await Singularity.w3.eth.get_balance(wallet_address)
    balance_in_sfi = Singularity.w3.from_wei(balance_in_wei, 'ether')
    return balance_in_sfi


async def wrap(account: Account, is_first: bool = False):

    for _ in range(2):
        try:
            if is_first:
                value = float(await get_sfi_balance(account)) / (random.randint(40, 60) / 10)
            else:
                value = get_value('wrap')

            contract, dict_transaction = await Singularity.create_contract_and_txn(
                "0x6dC404EFd04B880B0Ab5a26eF461b63A12E3888D",
               "./abis/wrap.json",
                account.wallet_address)

            dict_transaction['value'] = Singularity.w3.to_wei(value, 'ether')

            txn_wrap = await contract.functions.deposit().build_transaction(dict_transaction)
            await Singularity.send_txn(txn_wrap, account, f"wrap {value} SFI")
        except Exception as error:
            logger.error(f"{account.wallet_address} | wrap | {error}")
        await asyncio.sleep(random.randint(10, 20))


async def unwrap(account: Account):
    for _ in range(2):
        try:
            contract, dict_transaction = await Singularity.create_contract_and_txn(
                "0x6dC404EFd04B880B0Ab5a26eF461b63A12E3888D",
               "./abis/wrap.json",
                account.wallet_address)

            value = get_value('unwrap')

            txn_unwrap = await contract.functions.withdraw(
                Singularity.w3.to_wei(value, 'ether')
            ).build_transaction(dict_transaction)

            await Singularity.send_txn(txn_unwrap, account, f"unwrap {value} wSFI")
        except Exception as error:
            if 'insufficient funds for transfer' in str(error):
                logger.error(
                    f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
                write_filed_account(account.wallet_address)
                return
            elif "0xe450d38c0" in str(error):
                await wrap(account, is_first=True)
            else:
                logger.error(f"{account.wallet_address} | unwrap | {error}")
        await asyncio.sleep(random.randint(10, 20))


async def claim(account: Account):
    for _ in range(2):
        try:
            contract, dict_transaction = await Singularity.create_contract_and_txn(
                "0x22Dbdc9e8dd7C5E409B014BBcb53a3ef39736515",
                "abis/stake.json",
                account.wallet_address)

            txn_claim = await contract.functions.claim().build_transaction(dict_transaction)

            await Singularity.send_txn(txn_claim, account, f"claim")
        except Exception as error:
            if 'insufficient funds for transfer' in str(error):
                logger.error(
                    f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
                write_filed_account(account.wallet_address)
                return
            else:
                logger.error(f"{account.wallet_address} | claim | {error}")
        await asyncio.sleep(random.randint(100, 200))


async def approve(account: Account, value: int):
    try:
        contract, dict_transaction = await Singularity.create_contract_and_txn(
            "0x6dC404EFd04B880B0Ab5a26eF461b63A12E3888D",
            "abis/wrap.json",
            account.wallet_address)

        txn_claim = await contract.functions.approve(
            Singularity.w3.to_checksum_address("0x22Dbdc9e8dd7C5E409B014BBcb53a3ef39736515"),
            value
        ).build_transaction(dict_transaction)

        await Singularity.send_txn(txn_claim, account, f"approve for stake")
    except Exception as error:
        if 'insufficient funds for transfer' in str(error):
            logger.error(
                f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
            write_filed_account(account.wallet_address)
            return
        else:
            logger.error(f"{account.wallet_address} | approve for stake | {error}")

    time_to_sleep = random.randint(10, 15)
    await asyncio.sleep(time_to_sleep)
    return time_to_sleep


async def stake(account: Account):
    for _ in range(2):
        try:
            value = get_value('stake')

            unlock = await get_unlock(Singularity.w3.to_wei(value, 'ether'))

            time_to_sleep = await approve(account, Singularity.w3.to_wei(value, 'ether'))
            unlock -= time_to_sleep

            contract, dict_transaction = await Singularity.create_contract_and_txn(
                "0x22Dbdc9e8dd7C5E409B014BBcb53a3ef39736515",
                "abis/stake.json",
                account.wallet_address)

            txn_stake = await contract.functions.deposit(
                Singularity.w3.to_wei(value, 'ether'),
                unlock
            ).build_transaction(dict_transaction)

            await Singularity.send_txn(txn_stake, account, f"stake {value} wSFI")

        except Exception as error:
            if 'insufficient funds for transfer' in str(error):
                logger.error(
                    f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
                write_filed_account(account.wallet_address)
                return
            elif "0xe450d38c0" in str(error):
                await wrap(account, is_first=True)
            else:
                logger.error(f"{account.wallet_address} | stake | {error}")
        await asyncio.sleep(random.randint(55, 80))


async def unstake(account: Account):
    await asyncio.sleep(random.randint(5, 10))
    try:
        contract, dict_transaction = await Singularity.create_contract_and_txn(
            "0x22Dbdc9e8dd7C5E409B014BBcb53a3ef39736515",
            "abis/stake.json",
            account.wallet_address)

        value = get_value("unstake")

        txn_unstake = await contract.functions.withdrawAndClaim(
            Singularity.w3.to_wei(value, 'ether'),
        ).build_transaction(dict_transaction)

        await Singularity.send_txn(txn_unstake, account, f"unstake {value} wSFI")

    except Exception as error:
        if 'insufficient funds for transfer' in str(error):
            logger.error(
                f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
            write_filed_account(account.wallet_address)
            return
        elif "0xcd777af3" in str(error):
            logger.error(
                f"{account.wallet_address} | Can't do unstake, doing stake now...")
            await stake(account)
        else:
            logger.error(f"{account.wallet_address} | unstake | {error}")
    await asyncio.sleep(random.randint(5, 10))


async def bridge_to_sepolia(account: Account):
    for _ in range(5):
        await asyncio.sleep(random.randint(10, 20))
        try:
            value = get_value("bridge_sfi")

            contract, dict_transaction = await Singularity.create_contract_and_txn(
                "0x4200000000000000000000000000000000000016",
                "abis/bridge_to_sepolia.json",
                account.wallet_address)

            dict_transaction['value'] = Singularity.w3.to_wei(value, 'ether')

            txn_bridge = await contract.functions.initiateWithdrawal(
                AsyncWeb3.to_checksum_address(account.wallet_address),
                21000,
                '0x'
            ).build_transaction(dict_transaction)

            await Singularity.send_txn(txn_bridge, account, f"bridge {value} SFI to Sepolia")

        except Exception as error:
            if 'insufficient funds for transfer' in str(error):
                logger.error(
                    f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
                write_filed_account(account.wallet_address)
                return
            else:
                logger.error(f"{account.wallet_address} | bridge to Sepolia | {error}")
        await asyncio.sleep(random.randint(5, 30))
