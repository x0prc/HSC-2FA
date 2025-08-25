import pytest
from brownie import accounts, HoneytokenAuth

def test_admin_and_token_setup():
    admin = accounts[0]
    user = accounts[1]
    contract = HoneytokenAuth.deploy({'from': admin})

    real = [b"real1", b"real2"]
    honey = [b"honey1"]
    
    tx1 = contract.setRealTokens(user.address, real, {'from': admin})
    tx2 = contract.setHoneyTokens(user.address, honey, {'from': admin})

    assert contract.realTokens(user.address, 0) == real[0]
    assert contract.honeyTokens(user.address, 0) == honey[0]

def test_issue_challenge_and_authentication():
    admin = accounts[0]
    user = accounts[1]
    contract = HoneytokenAuth.deploy({'from': admin})

    real = [b"real123456789abcdef123456789abcdef12"]
    honey = [b"honey123456789abcdef123456789abcdef"]
    contract.setRealTokens(user.address, real, {'from': admin})
    contract.setHoneyTokens(user.address, honey, {'from': admin})

    # Simulate challenge
    options = contract.issueChallenge(user.address, {'from': user})
    assert len(options) == 2

    # Sign the real token (for demo, use raw address)
    tx = contract.authenticate(real[0], b'0'*65, {'from': user})
    event_found = any(e['name'] == 'AuthenticationSuccess' for e in tx.events)
    assert event_found

    tx2 = contract.authenticate(honey[0], b'0'*65, {'from': user})
    event_alert = any(e['name'] == 'HoneytokenAlert' for e in tx2.events)
    assert event_alert

