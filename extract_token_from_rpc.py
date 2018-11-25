import time

from ethereum.utils import checksum_encode
from web3 import Web3, HTTPProvider

from config import setting, ERC20_ABI, ERC20_ABI_EXCEPTION_1, ERC20_ABI_EXCEPTION_2
from pymongo import MongoClient
from project_log.my_log import setup_mylogger
from utils.eth_tool import EthContractService

logger = setup_mylogger(logfile="log/extract_token.log")




class EthRpcClient(object):

    def __init__(self, eth_url):
        self.web3 = Web3(HTTPProvider(eth_url))

    def get_contract_code(self, contract_address):
        contract_address = checksum_encode(contract_address)
        bytecode = self.web3.eth.getCode(contract_address).hex()
        return bytecode

    def get_contract_instance(self, contract_address, abi):
        '''
        获取合约实例
        '''
        contract_address = checksum_encode(contract_address)

        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        return contract

    def read_contract(self, contractAddress, method, args):
        '''
        读取合约状态
        '''
        contractAddress = checksum_encode(contractAddress)
        abi = ERC20_ABI
        contract_instance = self.get_contract_instance(contractAddress, abi)

        result = contract_instance.functions[method](*args).call()

        return result

    def read_contract_with_exception_1_abi(self, contractAddress, method, args):
        '''
        读取合约状态
        '''
        contractAddress = checksum_encode(contractAddress)
        abi = ERC20_ABI_EXCEPTION_1
        contract_instance = self.get_contract_instance(contractAddress, abi)
        result = contract_instance.functions[method](*args).call()
        return result

    def read_contract_with_exception_2_abi(self, contractAddress, method, args):
        '''
        读取合约状态
        '''
        contractAddress = checksum_encode(contractAddress)
        abi = ERC20_ABI_EXCEPTION_2
        contract_instance = self.get_contract_instance(contractAddress, abi)
        result = contract_instance.functions[method](*args).call()
        return result


class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db = self.client.eth_table
        self.db.Token.create_index([("address", 1)], unique=True)
        try:
            self.db.create_collection("HandleLogForToken", capped=True, size=10000000)
        except Exception as e:
            pass

    def get_handled_log(self, blockNumber, logIndex):
        return self.db.HandleLogForToken.find_one({"blockNumber": blockNumber, "logIndex": logIndex})

    def insert_handled_log(self, block_number, log_index):
        self.db.HandleLogForToken.create_index([("blockNumber", 1), ("logIndex", 1)], unique=True)
        self.db.HandleLogForToken.insert_one({"blockNumber": block_number, "logIndex": log_index})


    def insert_bookmark(self, block_height):
        self.db.BookmarkForToken.insert_one({"height": block_height})

    def get_bookmark(self):
        return self.db.BookmarkForToken.find_one()

    def update_bookmark(self, block_height):
        self.db.BookmarkForToken.update({}, {"$set": {"height": block_height}})


    def insert_token(self, token_address, name, symbol, decimals, total_supply, is_erc20, is_erc721):

        self.db.Token.insert_one({"address": token_address, "name": name, "symbol": symbol,
                                  "decimals": decimals, "totalSupply": total_supply, "is_erc20": is_erc20,
                                  "is_erc721": is_erc721})
        # logger.info("insert token {}".format({"address": token_address, "name": name, "symbol": symbol,
        #                                       "decimals": decimals, "totalSupply": total_supply, "is_erc20": is_erc20,
        #                                       "is_erc721": is_erc721}))

    def get_token(self, token_address):
        return self.db.Token.find_one({"address": token_address})


def check_log_handled(log):
    block_number = log.get("blockNumber")
    log_index = log.get("logIndex")
    log = mongo_client.get_handled_log(block_number, log_index)

    if log:
        return True
    return False


def mark_handled_log(log):
    block_number = log.get("blockNumber")
    log_index = log.get("logIndex")
    mongo_client.insert_handled_log(block_number, log_index)


def store_token(token_address):
    token = mongo_client.get_token(token_address)
    if token:
        pass
    else:
        token_type = check_token_type(token_address)
        is_erc20 = token_type.get("is_erc20")
        is_erc721 = token_type.get("is_erc721")
        if is_erc20 == False and is_erc721 ==False:
            return
        token_info = get_token_info(token_address, is_erc20, is_erc721)
        name = token_info.get("name")
        symbol = token_info.get("symbol")
        decimals = token_info.get("decimals")
        total_supply = str(token_info.get("totalSupply"))

        mongo_client.insert_token(token_address, name, symbol, decimals, total_supply, is_erc20, is_erc721)


def handle_logs(logs):
    logger.info("logs len:{}".format(len(logs)))
    for item in logs:
        # logger.info(item)
        has_handled = check_log_handled(item)
        if has_handled:
            logger.error("has been hander")
            continue

        contract_address = item.get("address").lower()

        # 将token存起来
        store_token(contract_address)

        # 将处理过的交易日志存起来
        mark_handled_log(item)


def get_logs(web3,local_block_number,block_interval):
    try:
        event_logs = web3.eth.getLogs({
            "fromBlock": hex(local_block_number),
            "toBlock": hex(local_block_number+block_interval),
            "address": [],
            "topics": [setting.TOPICS_OF_ERC_TRANSFER]
        })
        return event_logs
    except Exception as e:
        logger.error(e)

    return None


def check_token_type(token_address):
    '''
    检查token是erc20还是erc721
    '''
    eth_service = EthContractService()
    bytecode = eth_client.get_contract_code(token_address)
    func_hashes = eth_service.get_function_sighashes(bytecode)
    is_erc20 = eth_service.is_erc20_contract(func_hashes)
    is_erc721 = eth_service.is_erc721_contract(func_hashes)

    return {
        "is_erc20": is_erc20,
        "is_erc721": is_erc721
    }


def get_token_info(token_address, is_erc20, is_erc721):
    try:
        name = eth_client.read_contract(token_address, "name", [])
    except OverflowError as e:
        # logger.error(e)
        # logger.error(token_address)
        name = eth_client.read_contract_with_exception_2_abi(token_address, "name", []).decode().replace("\x00", "")
    except Exception as e:
        # logger.error(e)
        # logger.error(token_address)
        try:
            name = eth_client.read_contract_with_exception_1_abi(token_address, "NAME", [])
        except Exception as e:
            # logger.error(e)
            # logger.error(token_address)
            name = None

    try:
        symbol = eth_client.read_contract(token_address, "symbol", [])
    except OverflowError as e:
        # logger.error(e)
        symbol = eth_client.read_contract_with_exception_2_abi(token_address, "symbol", []).decode().replace("\x00", "")

    except Exception as e:
        # logger.error(e)
        # logger.error(token_address)
        try:
            symbol = eth_client.read_contract_with_exception_1_abi(token_address, "SYMBOL", [])
        except Exception as e:
            # logger.error(e)
            # logger.error(token_address)
            symbol = None
    if is_erc20 and not is_erc721:
        try:
            decimals = eth_client.read_contract(token_address, "decimals", [])
        except Exception as e:
            # logger.info(e)
            # logger.error(token_address)
            try:

                decimals = eth_client.read_contract_with_exception_1_abi(token_address, "DECIMALS", [])
            except Exception as e:
                # logger.error(e)
                # logger.error(token_address)
                decimals = None
    else:
        decimals = None

    try:
        total_supply = eth_client.read_contract(token_address, "totalSupply", [])
    except Exception as e:
        # logger.error(e)
        # logger.error(token_address)
        total_supply = None

    return {
        "name": name,
        "symbol": symbol,
        "decimals": decimals,
        "totalSupply": total_supply
    }


eth_client = EthRpcClient(setting.ETH_URL)

mongo_client = MongodbEth()

localBlockHeight = mongo_client.get_bookmark()

if localBlockHeight:
    local_block_height = int(localBlockHeight.get("height"))
else:
    local_block_height = 0

    mongo_client.insert_bookmark(local_block_height)

if __name__ == '__main__':

    w3 = Web3(HTTPProvider(setting.ETH_URL,{"timeout":30}))
    block_interval = 2 ** 10
    while True:
        try:
            current_block_number = w3.eth.blockNumber
        except:
            time.sleep(10)
            continue
        logger.info("local_block_number:{},current_block_number:{}".format(local_block_height, current_block_number))
        if local_block_height + block_interval >= current_block_number:
            block_interval = 0

        if local_block_height < current_block_number:
            event_logs = get_logs(w3,local_block_height, block_interval)
            if event_logs is None:
                block_interval = int(block_interval/2)
                continue
            handle_logs(event_logs)
            local_block_height += block_interval + 1
            mongo_client.update_bookmark(local_block_height)

        else:
            time.sleep(14)
