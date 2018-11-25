import time

from web3 import HTTPProvider, Web3

from config import setting
from pymongo import MongoClient
from project_log.my_log import setup_mylogger
from utils.utils import split_to_words

logger = setup_mylogger(logfile="log/{}.log".format(__file__[:-3]))




class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db= self.client.eth_table

        try:
            self.db.create_collection("HandledLogForBalance", capped=True,size=10000000)
        except Exception as e:
            pass

    def get_handled_log(self,blockNumber,logIndex):
        return self.db.HandledLogForBalance.find_one({"blockNumber":blockNumber,"logIndex":logIndex})

    def insert_handled_log(self,block_number, log_index):
        self.db.HandledLogForBalance.create_index([("blockNumber", 1),("logIndex",1)], unique=True)
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




    def query_balance(self,address):
        return self.db.Balance.find_one({"address":address})

    def insert_balance_of_erc20(self,address,contract_address,value):
        self.db.Balance.create_index([("address", 1)], unique=True)
        try:
            self.db.Balance.insert_one({"address":address,"balance":{contract_address:value}})
            # logger.info("insert balance:{} ".format({"address":address,"balance":{contract_address:value}}))
        except Exception as e:
            logger.error(e)



    def update_balance_of_erc20(self,address,contract_address,value):
        if value == "0":
            self.db.Balance.update({"address":address}, {"$unset": {"balance.{}".format(contract_address): ""}}, False, True)
        else:
            self.db.Balance.update({"address":address},{"$set":{"balance.{}".format(contract_address):value}})


    def insert_balance_of_erc721(self,address,contract_address,value):
        self.db.Balance.create_index([("address", 1)], unique=True)
        try:
            self.db.Balance.insert_one({"address":address,"balance":{contract_address:value}})
            # logger.info("insert balance:{} ".format({"address":address,"balance":{contract_address:value}}))
        except Exception as e:
            logger.error(e)


    def update_balance_of_erc721(self,address,contract_address,value):
        if value == []:
            self.db.Balance.update({"address":address}, {"$unset": {"balance.{}".format(contract_address): ""}}, False, True)
        else:
            self.db.Balance.update({"address":address},{"$set":{"balance.{}".format(contract_address):value}})



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


        is_erc721 = token.get("is_erc721")
        is_erc20 = token.get("is_erc20")

        if not is_erc721 and not is_erc20:
            continue

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

        balance_from = mongo_client.query_balance(address_from)
        balance_to = mongo_client.query_balance(address_to)

        if is_erc20:

            if balance_from:
                contract_balance_from = balance_from.get("balance").get(contract_address)
                if contract_balance_from:
                    contract_balance_from = int(contract_balance_from) - amount
                    mongo_client.update_balance_of_erc20(address_from,contract_address,str(contract_balance_from))


            if balance_to:
                contract_balance_to = balance_to.get("balance").get(contract_address)
                if contract_balance_to:
                    contract_balance_to = int(contract_balance_to) + amount
                    mongo_client.update_balance_of_erc20(address_to,contract_address,str(contract_balance_to))
                else:
                    mongo_client.update_balance_of_erc20(address_to,contract_address,str(amount))
            else:
                mongo_client.insert_balance_of_erc20(address_to, contract_address, str(amount))

        if is_erc721:
            if balance_from:
                contract_balance_from = balance_from.get("balance").get(contract_address)
                if contract_balance_from:
                    contract_balance_from.remove(amount)
                    mongo_client.update_balance_of_erc721(address_from, contract_address, contract_balance_from)

            if balance_to:
                contract_balance_to = balance_to.get("balance").get(contract_address)
                if contract_balance_to:
                    contract_balance_to.append(amount)
                    mongo_client.update_balance_of_erc721(address_to, contract_address, contract_balance_to)
                else:
                    mongo_client.update_balance_of_erc721(address_to, contract_address, [amount])
            else:
                mongo_client.insert_balance_of_erc721(address_to, contract_address, [amount])

        #将处理过的交易日志存起来
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









mongo_client=MongodbEth()

localBlockHeight = mongo_client.get_bookmark()

if localBlockHeight:
    local_block_height=int(localBlockHeight.get("height"))
else:
    local_block_height=0

    mongo_client.insert_bookmark(local_block_height)



if __name__ == '__main__':
    w3 = Web3(HTTPProvider(setting.ETH_URL,{"timeout":30}))
    block_interval = 2**12
    while True:
        current_block_number = mongo_client.get_current_block_number()
        logger.info("local_block_number:{},current_block_number:{}".format(local_block_height, current_block_number))
        if local_block_height + block_interval >= current_block_number:
            block_interval = int(block_interval/2)
            continue

        if local_block_height <= current_block_number:
            event_logs = get_logs(w3,local_block_height, block_interval)
            if event_logs is None:
                block_interval = int(block_interval/2)
                continue
            handle_logs(event_logs)
            # break
            local_block_height += block_interval + 1
            mongo_client.update_bookmark(local_block_height)
        else:
            time.sleep(14)
