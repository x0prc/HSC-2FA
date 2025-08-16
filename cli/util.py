from eth_account import Account
from web3 import Web3

def load_private_key():
    """
    Securely prompts user for Ethereum private key.
    """
    from getpass import getpass
    pk = getpass("Enter your Ethereum private key (not echoed): ")
    return pk.strip()

def address_from_private_key(private_key):
    """
    Derives Ethereum address from private key.
    """
    acct = Account.from_key(private_key)
    return acct.address

def sign_token(private_key, token: bytes) -> bytes:

    acct = Account.from_key(private_key)
    # Solidity expects "\x19Ethereum Signed Message:\n32" prefix
    message_hash = Web3.solidityKeccak(['bytes32'], [token])
    eth_prefix = b"\x19Ethereum Signed Message:\n32" + message_hash
    eth_prefixed_hash = Web3.keccak(eth_prefix)
    signed_message = acct.signHash(eth_prefixed_hash)
    return signed_message.signature

def token_hex_to_bytes(token_hex: str) -> bytes:
    token_hex = token_hex.lower()
    if token_hex.startswith('0x'):
        token_hex = token_hex[2:]
    return bytes.fromhex(token_hex.zfill(64))

def bytes_to_token_hex(token_bytes: bytes) -> str:
    """
    Converts bytes32 to hex string prefixed with '0x'.
    """
    return '0x' + token_bytes.hex()

