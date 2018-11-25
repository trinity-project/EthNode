
import time
from web3 import HTTPProvider, Web3
from config import setting
from pymongo import MongoClient
from project_log.my_log import setup_mylogger
from utils.utils import split_to_words

logger = setup_mylogger(logfile="log/extract_token_holding.log")




class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db= self.client.eth_table
        self.db.HandledLogForBalance.create_index([("blockNumber", 1), ("logIndex", 1)], unique=True)
        self.db.Balance.create_index([("address", 1)], unique=True)
        # self.db.TokensOfOwner.create_index([("address", 1)])
        # self.db.TokensOfOwner.create_index([("asset", 1)])
        try:
            self.db.create_collection("HandledLogForBalance", capped=True,size=10000000)
        except Exception as e:
            pass

    def get_handled_log(self,blockNumber,logIndex):
        return self.db.HandledLogForBalance.find_one({"blockNumber":blockNumber,"logIndex":logIndex})

    def insert_handled_log(self,block_number, log_index):

        self.db.HandledLogForBalance.insert_one({"blockNumber":block_number,"logIndex":log_index})

    def get_token(self,token_address):
        return self.db.Token.find_one({"address":token_address})

    def insert_bookmark(self,block_height):
        self.db.BookmarkForBalance.insert_one({"height":block_height})

    def get_bookmark(self):
        return self.db.BookmarkForBalance.find_one()

    def update_bookmark(self,block_height):
        self.db.BookmarkForBalance.update({},{"$set":{"height":block_height}})


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

    def query_tokens_of_owner(self,address,contract_address):
        return self.db.TokensOfOwner.find_one({"address":address,"asset":contract_address})

    def insert_tokens_of_owner(self,address,contract_address,value):
        try:
            self.db.TokensOfOwner.insert_one({"address":address,"asset":contract_address,"tokens":value})
            # logger.info("insert balance:{} ".format({"address":address,"balance":{contract_address:value}}))
        except Exception as e:
            logger.error(e)



    def update_tokens_of_owner(self,address,contract_address,value):
        if value == []:
            self.db.TokensOfOwner.remove({"address":address,"asset":contract_address})
        else:
            self.db.TokensOfOwner.update({"address":address},{"$set":{"tokens":value}})



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




def handle_logs(logs):
    logger.info("logs len:{}".format(len(logs)))
    for item in logs:
        # logger.info(item)
        has_handled = check_log_handled(item)
        if has_handled:
            logger.error("{}  {} has been hander".format(item.get("blockNumber"),item.get("logIndex")))
            continue

        contract_address = item.get("address").lower()
        token = mongo_client.get_token(contract_address)
        if not token:
            continue


        # is_erc721 = token.get("is_erc721")
        # is_erc20 = token.get("is_erc20")
        #
        # if not is_erc721 and not is_erc20:
        #     continue

        topics = [topic.hex() for topic in item.get("topics")]
        data = item.get("data")

        topics_with_data = topics + split_to_words(data)
        if len(topics_with_data) != 4:
            continue

        address_from="0x" + topics_with_data[1][-40:]
        address_to= "0x" +topics_with_data[2][-40:]
        # amount = int(topics_with_data[3], 16)



        #通过交易日志更新余额
        if address_to == address_from:
            continue

        balance_from = mongo_client.query_token_holding(address_from)
        balance_to = mongo_client.query_token_holding(address_to)

        # # if is_erc20:

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

        # if is_erc721:

        # tokens_of_from = mongo_client.query_tokens_of_owner(address_from,contract_address)
        # tokens_of_to = mongo_client.query_tokens_of_owner(address_to,contract_address)
        #
        # if tokens_of_from:
        #     tokens_from = tokens_of_from.get("tokens")
        #     try:
        #         tokens_from.remove(amount)
        #         mongo_client.update_tokens_of_owner(address_from, contract_address, tokens_from)
        #     except Exception as e:
        #         logger.error(e)
        #
        #
        # if tokens_of_to:
        #     tokens_to = tokens_of_to.get("tokens")
        #     tokens_to.append(amount)
        #     mongo_client.update_tokens_of_owner(address_to, contract_address, tokens_to)
        # else:
        #     mongo_client.insert_tokens_of_owner(address_to, contract_address, [amount])



        #将处理过的交易日志存起来
        # mark_handled_log(item)


def get_logs(web3,local_block_number,block_interval,contractAddressList=[]):
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

localBlockHeight = mongo_client.get_bookmark()

if localBlockHeight:
    local_block_height=int(localBlockHeight.get("height"))
else:
    local_block_height=0

    mongo_client.insert_bookmark(local_block_height)



if __name__ == '__main__':
    w3 = Web3(HTTPProvider(setting.ETH_URL,{"timeout":30}))
    block_interval = 2**10

    while True:
        current_block_number = mongo_client.get_current_block_number()
        # current_block_number = 6557000
        logger.info("local_block_number:{},current_block_number:{}".format(local_block_height, current_block_number))
        if local_block_height + block_interval > current_block_number:
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