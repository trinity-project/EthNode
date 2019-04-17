#!/usr/bin/env python
# coding=utf-8
import json
from decimal import Decimal

from ethereum.utils import checksum_encode
from pymongo import MongoClient
import time
import requests
from config import setting

from project_log import setup_mylogger
logger=setup_mylogger(logfile="log/store_tx.log")


def md5_for_transfer_record(tx_id,address_from,address_to,value,contract):
    import hashlib
    src = "{}{}{}{}{}".format(tx_id,address_from,address_to,value,contract).encode()
    m1 = hashlib.md5()
    m1.update(src)
    return m1.hexdigest()


class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db= self.client.eth_table

    def insert_block_height(self,block_height):
        self.db.BlockHeightForStoreTx.insert_one({"height":block_height})

    def get_block_height(self):
        return self.db.BlockHeightForStoreTx.find_one()

    def update_block_height(self,block_height):
        self.db.BlockHeightForStoreTx.update({},{"$set":{"height":block_height}})

    def query_address(self,address):
        return self.db.AddressForTransferRecord.find_one({"address":address})

    def insert_transfer_record(self,record):
        try:
            self.db.TransferRecord.insert_one(record)
        except Exception as e:
            logger.info(e)

    def get_current_block_number(self):
        return self.db.BookmarkForToken.find_one().get("height")

def get_tx_receipt(txId):

    data = {
          "jsonrpc": "2.0",
          "method": "eth_getTransactionReceipt",
          "params": [txId],
          "id": 1
}

    try:
        res = requests.post(setting.ETH_URL,json=data).json()
        result = res["result"]
        if result:
            return result
        time.sleep(14)
        return get_tx_receipt(txId)
    except:
        time.sleep(3)
        return get_tx_receipt(txId)


def getblock(blockNumber):

    data = {
          "jsonrpc": "2.0",
          "method": "eth_getBlockByNumber",
          "params": [blockNumber,True],
          "id": 1
}

    try:
        res = requests.post(setting.ETH_URL,json=data).json()
        result = res["result"]
        if result:
            return result
        time.sleep(14)
        return getblock(blockNumber)
    except:
        time.sleep(3)
        return getblock(blockNumber)

mongo_client=MongodbEth()

blockHeight = mongo_client.get_block_height()

if blockHeight:
    block_height=blockHeight.get("height")
else:
    block_height=0

    blockHeight=mongo_client.insert_block_height(block_height)



while True:
    current_block_number = mongo_client.get_current_block_number()
    logger.info("local_block_number:{},current_block_number:{}".format(block_height, current_block_number))

    block_info=getblock(hex(int(block_height)))
    if not block_info:
        time.sleep(15)
        continue
    if block_info["transactions"]:
        for tx in block_info["transactions"]:
            tx_id=tx.get("hash")
            address_from=tx.get("from")
            address_to=tx.get("to")
            value=tx.get("value")
            gas=tx.get("gas")
            gas_price=tx.get("gasPrice")
            data=tx.get("input")
            block_number=tx.get("blockNumber")
            block_timestamp=block_info.get("timestamp")

            tmp_dict = {}
            tmp_dict["txId"] = tx_id
            tmp_dict["addressFrom"] = address_from
            tmp_dict["gas"] = str(int(gas, 16))
            tmp_dict["gasPrice"] = str(int(gas_price, 16))
            tmp_dict["blockNumber"] = str(int(block_number, 16))
            tmp_dict["blockTime"] = str(int(block_timestamp, 16))
            tmp_dict["txReceiptStatus"] = "1"

            if data == "0x":
                if mongo_client.query_address(address_to) or mongo_client.query_address(address_from):

                    tmp_dict["addressTo"] = address_to
                    tmp_dict["value"] = str(Decimal(int(value, 16)))
                    tmp_dict["asset"]="0x00000000000000000000000000000000000000"
                    tmp_dict["txMd5"] = md5_for_transfer_record(tmp_dict["txId"], tmp_dict["addressFrom"],
                                                                tmp_dict["addressTo"], tmp_dict["value"],
                                                                tmp_dict["asset"])
                    mongo_client.insert_transfer_record(tmp_dict)

            else:
                if data[:10] == "0xa9059cbb":
                    try:
                        tmp_dict["asset"] = address_to
                        tmp_dict["addressTo"] = "0x" + data[34:74]
                        tmp_dict["value"] = str(int(data[74:], 16))
                        exist_address_to = mongo_client.query_address(tmp_dict["addressTo"])
                        exist_address_from  = mongo_client.query_address(address_from)
                        if exist_address_to or exist_address_from:
                            tx_receipt = get_tx_receipt(tx_id)
                            if tx_receipt:
                                tmp_dict["txReceiptStatus"] = str(int(tx_receipt.get("status"),16))

                            tmp_dict["txMd5"] = md5_for_transfer_record(tmp_dict["txId"], tmp_dict["addressFrom"],
                                                                        tmp_dict["addressTo"], tmp_dict["value"],
                                                                        tmp_dict["asset"])

                            tmp_dict["addressFrom"] = checksum_encode(tmp_dict["addressFrom"])
                            tmp_dict["addressTo"] = checksum_encode(tmp_dict["addressTo"])
                            mongo_client.insert_transfer_record(tmp_dict)


                    except Exception as e:
                        logger.exception(e)




    block_height+=1
    mongo_client.update_block_height(block_height)








