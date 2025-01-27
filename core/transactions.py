from core.connections import BaseConnection
from utils.file_utils import write_filed_account
from configs.settings import OPERATION_LIMITS
import random
from utils.log_utils import logger
from core.account import Account
from services.singularity import Singularity
from services.sepolia import Sepolia

async def execute_operation(account, connection: BaseConnection, operation: str):
    try:
        min_val, max_val = OPERATION_LIMITS.get(operation, (0, 0))
        value = random.uniform(min_val, max_val)
        # Подключить логику для каждой операции (например, wrap, stake)
        # await specific_function(account, value, connection)
    except Exception as error:
        write_filed_account(account.wallet_address)
        raise error
