import time
from web3 import HTTPProvider, Web3

from project_log import setup_mylogger

INFURA_URL = "https://mainnet.infura.io/pZc5ZTRYM8wYfRPtoQal"
LOCAL_ETHNODE_URL = "http://127.0.0.1:8545"

logger = setup_mylogger(logfile="log/watch_eth_node.log")


def execute_shell_command(command):
    import os
    os.system(command)


def compare_block_number():
    infura_w3 = Web3(HTTPProvider(INFURA_URL, {"timeout": 30}))
    local_w3 = Web3(HTTPProvider(LOCAL_ETHNODE_URL, {"timeout": 30}))
    while True:
        try:
            infura_block_number = infura_w3.eth.blockNumber
            local_block_number = local_w3.eth.blockNumber
            logger.info("local_block_number:{},infura_block_number:{}".format(local_block_number, infura_block_number))
            if infura_block_number - local_block_number >= 10:
                # execute_shell_command("supervisorctl restart geth")
                logger.warning("restart geth")
        except:
            pass

        finally:
            time.sleep(120)


if __name__ == "__main__":
    compare_block_number()