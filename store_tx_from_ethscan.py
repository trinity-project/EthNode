#!/usr/bin/env python
# coding=utf-8
import json

from etherscan.accounts import Account
from pymongo import MongoClient
import time
from config import setting

from project_log import setup_mylogger

logger=setup_mylogger(logfile="log/store_transfer_tx_from_ethscan.log")






class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db= self.client.eth_table
        self.db.TransferRecord.create_index([("addressFrom", 1)])
        self.db.TransferRecord.create_index([("addressTo", 1)])
        self.db.TransferRecord.create_index([("asset", 1)])
        self.db.TransferRecord.create_index([("txId", 1)])

    def get_address(self):
        return self.db.AddressForTransferRecord.find_one({"has_query":0})


    def update_address(self,address):
        self.db.AddressForTransferRecord.update({"address":address},{"$set":{"has_query":1}})
        logger.info("address:{} has query".format(address))

    def insert_transfer_record(self,record):
        try:
            self.db.TransferRecord.insert_one(record)
        except Exception as e:
            logger.info(e)


mongo_client=MongodbEth()

while True:
    address = mongo_client.get_address()
    if not address:
        time.sleep(15)
        continue

    my_account = Account(address=address.get("address"),
                         api_key=setting.API_KEY)
    my_account.PREFIX =setting.ETHSCAN_API_PREFIX
    try:
        res = my_account.get_transaction_page(sort="desc")
    except Exception as e:
        res = None

    if res:
        for r in res:
            tmp_dict = {}
            tmp_dict["txId"] = r.get("hash")
            tmp_dict["addressFrom"] = r.get("from")
            tmp_dict["gasUsed"] = r.get("gasUsed")
            tmp_dict["gasPrice"] = r.get("gasPrice")
            tmp_dict["gas"] = r.get("gas")
            tmp_dict["blockNumber"] = r.get("blockNumber")
            tmp_dict["blockTime"] = r.get("timeStamp")

            tmp_dict["txReceiptStatus"] = r.get("txreceipt_status")
            input_data = r.get("input")
            if input_data == "0x":

                tmp_dict["addressTo"] = r.get("to")
                tmp_dict["value"] = str(r.get("value"))
                tmp_dict["asset"] = "0x00000000000000000000000000000000000000"

            if input_data[:10] == "0xa9059cbb":
                tmp_dict["addressTo"] = "0x"+input_data[34:74]
                tmp_dict["value"] = str(int(input_data[74:],16))
                tmp_dict["asset"] = r.get("to")

            if not tmp_dict.get("addressTo"):
                continue

            mongo_client.insert_transfer_record(tmp_dict)


    mongo_client.update_address(address.get("address"))







