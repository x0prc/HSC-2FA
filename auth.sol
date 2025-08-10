// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract Auth {
    using ECDSA for bytes32;

    // Define maps for tokens and challenge.
    mapping(address => bytes32[]) private realTokens;
    mapping(address => bytes32[]) private honeyTokens;
    mapping(address => bytes32[]) private currentChallenge;

    event HoneytokenAlert(address indexed user, bytes32 token);
    event AuthenticationSuccess(address indexed user, bytes32 token);
    event TokensSet(address indexed user, bool isReal);
    event ChallengeIssued(address indexed user, bytes32[] tokens);

    // To reserve admin access.
    address public admin;

    error OnlyAdmin();
    error SignatureMismatch();
    error TokenNotInChallenge();
    error TokenNotRecognized();

    // Admin configuration
    modifier onlyAdmin() {
        if (msg.sender != admin) {
            revert OnlyAdmin();
        }
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    // Generate actual tokens for authentication.
    function setRealTokens(address user, bytes32[] memory tokens) public onlyAdmin {
        realTokens[user] = tokens;
        emit TokensSet(user, true);
    }

    // Generate secret tokens for obfuscation.
    function setHoneyTokens(address user, bytes32[] memory tokens) public onlyAdmin {
        honeyTokens[user] = tokens;
        emit TokensSet(user, false);
    }

    // Shuffle tokens to increase discovering difficulty.
    function shuffleTokens(bytes32[] memory combined) internal view returns (bytes32[] memory) {
        uint length = combined.length;
        for (uint i = 0; i < length; i++) {
            uint n = i + uint(keccak256(abi.encodePacked(block.timestamp, block.prevrandao, i))) % (length - i); // difficulty' is now deprecated
            (combined[i], combined[n]) = (combined[n], combined[i]);
        }
        return combined;
    }

    // Challenge configuration
    function issueChallenge(address user) public returns (bytes32[] memory) {
        bytes32[] memory rTokens = realTokens[user];
        bytes32[] memory hTokens = honeyTokens[user];
        bytes32[] memory combined = new bytes32[](rTokens.length + hTokens.length);

        for (uint i = 0; i < rTokens.length; i++) {
            combined[i] = rTokens[i];
        }
        for (uint j = 0; j < hTokens.length; j++) {
            combined[rTokens.length + j] = hTokens[j];
        }

        bytes32[] memory shuffled = shuffleTokens(combined);
        currentChallenge[user] = shuffled;
        emit ChallengeIssued(user, shuffled);
        return shuffled;
    }

    function recoverSigner(bytes32 message, bytes memory sig) public pure returns (address) {
        bytes32 ethSignedMessageHash = getEthSignedMessageHash(message);
        return ethSignedMessageHash.recover(sig);
    }

    function getEthSignedMessageHash(bytes32 message) public pure returns (bytes32) {
        return message.toEthSignedMessageHash();
    }

    function tokenExists(bytes32 token, bytes32[] memory tokens) internal pure returns (bool) {
        return tokens.contains(token);
    }


    // Authentication using actual tokens.
    function authenticate(bytes32 selectedToken, bytes memory signature) public {
        address signer = recoverSigner(selectedToken, signature);
        if (signer != msg.sender) {
            revert SignatureMismatch();
        }

        bytes32[] memory challengeTokens = currentChallenge[signer];
        if (!tokenExists(selectedToken, challengeTokens)) {
            revert TokenNotInChallenge();
        }

        if (tokenExists(selectedToken, honeyTokens[signer])) {
            emit HoneytokenAlert(signer, selectedToken);
        } else if (tokenExists(selectedToken, realTokens[signer])) {
            emit AuthenticationSuccess(signer, selectedToken);
        } else {
            revert TokenNotRecognized();
        }
    }
}