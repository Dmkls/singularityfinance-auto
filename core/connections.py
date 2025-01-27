from web3 import AsyncWeb3, AsyncHTTPProvider
from utils.log_utils import logger
from web3.eth.eth import ChecksumAddress
from utils.file_utils import read_json


class BaseConnection:
    def __init__(self, rpc_url: str):
        self.w3: AsyncWeb3 = AsyncWeb3(provider=AsyncHTTPProvider(endpoint_uri=rpc_url))

    async def is_connected(self) -> bool:
        return await self.w3.is_connected()

    async def create_dict_transaction(self, wallet_address: str, multiplier: float = 1.3) -> dict:
        last_block = await self.w3.eth.get_block('latest')
        wallet_address = AsyncWeb3.to_checksum_address(wallet_address)
        max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        base_fee = int(last_block['baseFeePerGas'] * multiplier)
        max_fee_per_gas = base_fee + max_priority_fee_per_gas

        return {
            'chainId': await self.w3.eth.chain_id,
            'from': wallet_address,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'maxFeePerGas': max_fee_per_gas,
            'nonce': await self.w3.eth.get_transaction_count(wallet_address),
        }

    async def send_txn(self, txn: dict, account, func: str | None = None):
        try:
            signed_txn = self.w3.eth.account.sign_transaction(txn, account.private_key)
            txn_hash = await self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            logger.info(f"{account.wallet_address} | {func} | {txn_hash.hex()}")
        except Exception as error:
            logger.error(f"{account.wallet_address} | {func} | {error}")

    async def create_contract_and_txn(
    self,
    address: str | ChecksumAddress,
    abi_path: str,
    wallet_address: str | ChecksumAddress
    ):
        contract_address = AsyncWeb3.to_checksum_address(address)
        abi = read_json(abi_path)

        return self.w3.eth.contract(contract_address, abi=abi), await self.create_dict_transaction(wallet_address)
