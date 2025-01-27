from core.connections import BaseConnection
from configs.constants import SEPOLIA_RPC
from web3 import AsyncWeb3
from core.account import Account
import random

from services.singularity import get_value
from utils.log_utils import logger
import asyncio

Sepolia = BaseConnection(SEPOLIA_RPC)

async def approve_on_sepolia(account: Account, value: float):
    await asyncio.sleep(random.randint(10, 20))
    try:
        contract, dict_transaction = await Sepolia.create_contract_and_txn(
            "0x9a3f60032941C91cdeF5dBB58f2cE80e47e3ddCA",
            "abis/approve_on_sepolia.json",
            account.wallet_address
        )

        txn_approve = await contract.functions.approve(
            AsyncWeb3.to_checksum_address("0x776CF4e50c7285810e4E25A79de56aA4E7116876"),
            Sepolia.w3.to_wei(value, 'ether')
        ).build_transaction(dict_transaction)

        await Sepolia.send_txn(txn_approve, account, f"approve {value} SFI on Sepolia")

    except Exception as error:
        logger.error(f"{account.wallet_address} | approve on Sepolia | {error}")
    await asyncio.sleep(random.randint(30, 50))


async def bridge_from_sepolia(account: Account):
    for _ in range(1):
        await asyncio.sleep(random.randint(10, 20))
        try:
            contract, dict_transaction = await Sepolia.create_contract_and_txn(
                "0x776CF4e50c7285810e4E25A79de56aA4E7116876",
                "abis/bridge_from_sepolia.json",
                account.wallet_address
            )
            value = get_value("bridge_sep")
            await approve_on_sepolia(account, value)

            txn_approve = await contract.functions.depositERC20Transaction(
                AsyncWeb3.to_checksum_address(account.wallet_address),
                Sepolia.w3.to_wei(value, 'ether'),
                Sepolia.w3.to_wei(value, 'ether'),
                100000,
                False,
                b"0x00"
            ).build_transaction(dict_transaction)

            await Sepolia.send_txn(txn_approve, account, f"bridge {value} SFI from Sepolia")

        except Exception as error:
            logger.error(f"{account.wallet_address} | approve on Sepolia | {error}")
        await asyncio.sleep(random.randint(10, 15))