from utils.file_utils import read_private_keys
from services.singularity import *
from services.sepolia import *
from configs.settings import ENABLED_OPERATIONS, DELAY_BEFORE_START


async def process_account(private_key: str):
    account = Account(private_key, Singularity)

    if await get_sfi_balance(account) < 1:
        logger.error(f"{account.wallet_address} | Insufficient balance, please request test tokens on the faucet")
        write_filed_account(account.wallet_address)
        return

    if DELAY_BEFORE_START:
        await asyncio.sleep(random.randint(1, 12 * 60 * 60))

    await asyncio.sleep(random.randint(1, 60))

    while True:

        logger.success(f"{account.wallet_address} | Starting account..")

        tasks = []

        if ENABLED_OPERATIONS['wrap']:
            tasks.append(wrap)

        if ENABLED_OPERATIONS['unwrap']:
            tasks.append(unwrap)

        if ENABLED_OPERATIONS['claim']:
            tasks.append(claim)

        if ENABLED_OPERATIONS['stake']:
            tasks.append(stake)

        if ENABLED_OPERATIONS['unstake']:
            tasks.append(unstake)

        if ENABLED_OPERATIONS['bridge_sfi']:
            tasks.append(bridge_to_sepolia)

        if ENABLED_OPERATIONS['bridge_sep']:
            tasks.append(bridge_from_sepolia)

        random.shuffle(tasks)

        for task in tasks:
            await task(account)

        logger.success(f"{account.wallet_address} | all transactions have been successfully completed for today!")

        await asyncio.sleep(random.randint(22 * 60 * 60, 26 * 60 * 60))


async def main():
    private_keys = read_private_keys()
    tasks = [process_account(private_key) for private_key in private_keys]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())