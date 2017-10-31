import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from dtmid import DtmiDaemon
from dtmi_config import DtmiConfig


def test_dtmid():
    config_text = DtmiConfig.slurp_config_file(config.dtmi_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000f5c816dff0e8e5a35384719db01b101cbda99b1545a24b69c5a549b0de4'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000512bd5dc37e69980b6cea52d847c6da6e00886ab12f1bb16d8d07ae8af7'

    creds = DtmiConfig.get_rpc_creds(config_text, network)
    dtmid = DtmiDaemon(**creds)
    assert dtmid.rpc_command is not None

    assert hasattr(dtmid, 'rpc_connection')

    # Dtmi testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = dtmid.rpc_command('getinfo')
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
    assert dtmid.rpc_command('getblockhash', 0) == genesis_hash
