import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from volkshashd import VolkshashDaemon
from volkshash_config import VolkshashConfig


def test_volkshashd():
    config_text = VolkshashConfig.slurp_config_file(config.volkshash_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000035502f6f464645ff5caa344484f01089f2020712fbd76b79a82ed92d91f'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000009dc62e5bc38bae3e5fa53b5e667c06a2066d32c12343d76bc540772b732'

    creds = VolkshashConfig.get_rpc_creds(config_text, network)
    volkshashd = VolkshashDaemon(**creds)
    assert volkshashd.rpc_command is not None

    assert hasattr(volkshashd, 'rpc_connection')

    # Volkshash testnet block 0 hash == 000009dc62e5bc38bae3e5fa53b5e667c06a2066d32c12343d76bc540772b732
    # test commands without arguments
    info = volkshashd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert volkshashd.rpc_command('getblockhash', 0) == genesis_hash
