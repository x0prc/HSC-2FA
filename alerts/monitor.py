import json
import time
from web3 import Web3
from notifier import send_email_alert, send_slack_alert
from config import PROVIDER_URL, CONTRACT_ADDRESS, ABI_PATH

# === Load contract ABI
with open(ABI_PATH, 'r') as f:
    contract_abi = json.load(f)

# === Set up web3
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# === Notification settings (REPLACE with secure env vars in production)
NOTIFY_EMAIL = "admin@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 465
SMTP_USER = "your@email.com"
SMTP_PASSWORD = "your-smtp-password"
SLACK_WEBHOOK = "https://hooks.slack.com/services/XXXX/YYYY/ZZZZ"

def handle_honeytoken_alert(event):
    user = event['args']['user']
    token = event['args']['token']
    body = f"Honeytoken ALERT!\nUser: {user}\nToken: {Web3.toHex(token)}"
    print("[Monitor] Honeytoken alert detected.")
    send_email_alert(
        subject="Honeytoken Triggered!",
        body=body,
        recipient=NOTIFY_EMAIL,
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        smtp_user=SMTP_USER,
        smtp_password=SMTP_PASSWORD
    )
    send_slack_alert(SLACK_WEBHOOK, body)

def handle_auth_success(event):
    user = event['args']['user']
    print(f"[Monitor] Successful authentication for user {user}.")

def main():
    print("[Monitor] Listening for contract events...")
    last_block = w3.eth.block_number

    while True:
        # Query new blocks (simple polling)
        latest_block = w3.eth.block_number
        if latest_block > last_block:
            for block in range(last_block + 1, latest_block + 1):
                # HoneytokenAlert Events
                events = contract.events.HoneytokenAlert().get_logs(fromBlock=block, toBlock=block)
                for event in events:
                    handle_honeytoken_alert(event)
                events = contract.events.AuthenticationSuccess().get_logs(fromBlock=block, toBlock=block)
                for event in events:
                    handle_auth_success(event)
            last_block = latest_block
        time.sleep(5)  # Polling interval

if __name__ == '__main__':
    main()
