import time

from web3 import HTTPProvider, Web3

from config import setting
from pymongo import MongoClient
from project_log.my_log import setup_mylogger
from utils.utils import split_to_words

logger = setup_mylogger(logfile="log/add_token_holding.log")




class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db= self.client.eth_table







    def get_current_block_number(self):
        return self.db.BookmarkForToken.find_one().get("height")


    def query_token_holding(self,address):
        return self.db.Balance.find_one({"address":address})

    def insert_token_holding(self,address,tokens):

        try:
            self.db.Balance.insert_one({"address":address,"tokenHolding":tokens})
        except Exception as e:
            logger.error(e)



    def update_token_holding(self,address,tokens):
        self.db.Balance.update({"address":address},{"$set":{"tokenHolding":tokens}})









def handle_logs(logs):
    logger.info("logs len:{}".format(len(logs)))
    for item in logs:
        contract_address = item.get("address").lower()

        topics = [topic.hex() for topic in item.get("topics")]
        data = item.get("data")

        topics_with_data = topics + split_to_words(data)
        if len(topics_with_data) != 4:
            continue

        address_from="0x" + topics_with_data[1][-40:]
        address_to= "0x" +topics_with_data[2][-40:]
        amount = int(topics_with_data[3], 16)



        #通过交易日志更新余额
        if address_to == address_from:
            continue

        balance_from = mongo_client.query_token_holding(address_from)
        balance_to = mongo_client.query_token_holding(address_to)



        if balance_from:
            tokens = balance_from.get("tokenHolding")
            if contract_address not in tokens:
                tokens.append(contract_address)
                mongo_client.update_token_holding(address_from,tokens)
        else:
            mongo_client.insert_token_holding(address_from,[contract_address])

        if balance_to:
            tokens = balance_to.get("tokenHolding")
            if contract_address not in tokens:
                tokens.append(contract_address)
                mongo_client.update_token_holding(address_to,tokens)
        else:
            mongo_client.insert_token_holding(address_to,[contract_address])






def get_logs(web3,local_block_number,block_interval,contractAddressList):
    try:
        event_logs = web3.eth.getLogs({
            "fromBlock": hex(local_block_number),
            "toBlock": hex(local_block_number+block_interval),
            "address": contractAddressList,
            "topics": [setting.TOPICS_OF_ERC_TRANSFER]
        })
        return event_logs
    except Exception as e:
        logger.error(e)

    return None









mongo_client=MongodbEth()



if __name__ == '__main__':
    w3 = Web3(HTTPProvider(setting.ETH_URL,{"timeout":30}))
    block_interval = 2**15
    tokens_list = [token.get("address") for token in  mongo_client.db.BalanceHandledToken.find({"handled":False})]
    logger.info(len(tokens_list))
    tokens = tokens_list
    # tokens = tokens_list[250:500]
    # tokens = tokens_list[500:]
    # for tokens in [list_1,list_2,list_3]:
    # tokens = ["0x86e4dc25259ee2191cd8ae40e1865b9f0319646c"]
    local_block_height = 1000000
    current_block_number = mongo_client.get_current_block_number()
    while True:
        # current_block_number = mongo_client.get_current_block_number()
        # current_block_number = 6565717
        logger.info("local_block_number:{},current_block_number:{}".format(local_block_height, current_block_number))
        if local_block_height > current_block_number:
            break
        if local_block_height + block_interval > current_block_number:
            block_interval = int(block_interval/2)
            continue

        if local_block_height <= current_block_number:
            event_logs = get_logs(w3,local_block_height, block_interval,tokens)
            if event_logs is None:
                block_interval = int(block_interval/2)
                continue
            handle_logs(event_logs)
            if local_block_height == current_block_number:
                break
            local_block_height += block_interval + 1
            # mongo_client.update_bookmark(local_block_height)

