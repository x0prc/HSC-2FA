# HSC-2FA
Honeytoken Driven Smart Contract 2FA Implementation

A minimal yet powerful proof-of-concept demo for two-factor authentication using honeytokens (decoy credentials/actions) and blockchain smart contracts, fully operated via the terminal/CLI. Selecting a decoy triggers real-time alerts for enhanced security in sensitive cloud or administrative environments.

## Features

- **Blockchain-Enforced 2FA:** Authentication flows via smart contracts (Ethereum-compatible).
- **Honeytoken Security:** Randomized decoy options mixed with real choices in each session.
- **CLI:** No web interface—just pure terminal for sysadmins and engineers.
- **Instant Alerts:** Decoy/honeytoken selection emits blockchain events, triggers notifications.


## Security Notes

- Always keep private keys secure.
- Prefer hardware wallets for maximum security.
- Rotate honeytoken options periodically.

> [!NOTE]
> Addresses & Keys: <p> The `CONTRACT_ADDRESS` in `config.py` and any private keys or test account references are placeholders for demonstration only. Always use your own smart contract deployment, endpoints, ABI, and private keys when setting up this POC. Never commit secrets to the repository. </p>
> Security: <p> This project is for internal concept demonstration only. The randomness/shuffling logic in Solidity is not suitable for production; a secure VRF or oracle is required for real deployments. Never use real funds or production accounts with this prototype. </p>
> Notifications: <p> Email and Slack integrations require your own configuration and credentials. </p>
