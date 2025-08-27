import sys
import pytest
from unittest.mock import patch

import cli.auth as auth

def test_private_key_prompt(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '0xDEADBEEF')
    monkeypatch.setattr('cli.utils.getpass', lambda _: 'dummyprivatekey')
    pk = auth.load_private_key()
    assert isinstance(pk, str)
    assert pk == 'dummyprivatekey'

def test_option_selection(monkeypatch):
    test_options = ["0x123", "0x456"]
    monkeypatch.setattr('builtins.input', lambda _: '2')
    assert auth.select_option(test_options) == test_options[1]

def test_auth_flow(monkeypatch):
    monkeypatch.setattr('builtins.input', side_effect=['0xFakeAddress', '1'])
    auth.load_private_key = lambda: '0xfakeprivatekey'

    class DummyContract:
        def functions(self):
            return self
        def issueChallenge(self, user_addr):
            return self
        def call(self):
            return [b'\x01'*32, b'\x02'*32]

    auth.Web3 = type('Web3', (), {'HTTPProvider': lambda _: None, 'toHex': lambda b: '0x'+b.hex()})
    auth.w3 = type('Web3', (), {'eth': type('Eth', (), {'contract': lambda address, abi: DummyContract()})})
    
    selected = auth.select_option(['0x01'*32, '0x02'*32])
    assert selected.startswith('0x')

