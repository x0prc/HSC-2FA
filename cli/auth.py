import sys
import json
from web3 import Web3
from eth_account import Account
from getpass import getpass
from config import CONTRACT_ADDRESS, PROVIDER_URL, ABI_PATH

# Load contract ABI
with open(ABI_PATH, 'r') as abi_file:
    contract_abi = json.load(abi_file)

# Set up Web3 connection
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

def load_private_key():
    pk = getpass("Enter your Ethereum private key (not echoed): ")
    return pk

def select_option(options):
    print("\n[Options]")
    for idx, opt in enumerate(options):
        print(f"{idx + 1}. {opt}")
    while True:
        try:
            choice = int(input("\nSelect option (number): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except Exception:
            pass
        print("Invalid input. Try again.")

def main():
    user_addr = input("Enter your Ethereum address: ").strip()
    pk = load_private_key()
    acct = Account.from_key(pk)

    if acct.address.lower() != user_addr.lower():
        print("Private key does not match provided address.")
        sys.exit(1)

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

    # Issue challenge: fetch challenge tokens from smart contract
    print("Fetching authentication challenge...")
    tx = contract.functions.issueChallenge(user_addr).call()
    token_opts = [w3.toHex(token) for token in tx]

    selected_token_hex = select_option(token_opts)
    selected_token_bytes = bytes.fromhex(selected_token_hex[2:])  

    # Sign token
    message_hash = w3.solidityKeccak(['bytes32'], [selected_token_bytes])
    signed = acct.sign_message(
        Web3.solidityKeccak(['string'], [f"\x19Ethereum Signed Message:\n32{selected_token_bytes.hex()}"])
    )
    signature = signed.signature

    # Submit authentication
    try:
        tx = contract.functions.authenticate(selected_token_bytes, signature).build_transaction({
            'from': user_addr,
            'nonce': w3.eth.get_transaction_count(user_addr),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
        })
        signed_tx = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Submitted auth tx: {tx_hash.hex()}")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Authentication submitted. Checking result...")

        logs = contract.events.AuthenticationSuccess().process_receipt(receipt)
        if logs:
            print("[SUCCESS] Authentication successful! Welcome.")
        else:
            logs = contract.events.HoneytokenAlert().process_receipt(receipt)
            if logs:
                print("[ALERT] Decoy/honeytoken selected! Security team notified.")
                sys.exit(10) 
            else:
                print("Authentication failed or unknown error.")
                sys.exit(2)
    except Exception as e:
        print(f"Error submitting authentication: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
