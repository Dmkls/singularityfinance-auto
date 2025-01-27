class Account:
    def __init__(self, private_key: str, connection):
        self.private_key: str = private_key
        self.wallet_address: str = connection.w3.eth.account.from_key(private_key).address
