#!/usr/bin/env python
# encoding: utf-8
"""
@author: Maiganne

"""
from pymongo import MongoClient
from config import setting
class MongodbEth(object):
    def __init__(self):
        self.client = MongoClient(setting.MONGO_URI)
        self.db= self.client.eth_table
        self.db.AddressForTransferRecord.create_index([("address", 1)], unique=True)

    def insert_address(self,address):
        if not self.db.AddressForTransferRecord.find_one({"address":address}):
            self.db.AddressForTransferRecord.insert_one({"address":address,"has_query":0})



    def get_token_holding(self,address):
        record=self.db.Balance.find_one({"address":address},{"_id":0})
        if record:
            token_holding = record.get("tokenHolding")
        else:
            token_holding = []

        res = []
        for th in token_holding:
            tmp_dict = {}
            token = self.db.Token.find_one({"address":th})

            if token:
                tmp_dict["tokenAddress"] = token.get("address")
                tmp_dict["tokenDecimal"] = None if token.get("decimals") is None else str(token.get("decimals"))
                tmp_dict["tokenIcon"] = token.get("icon")
                tmp_dict["tokenName"] = token.get("name")
                tmp_dict["tokenSynbol"] = token.get("symbol")
                tmp_dict["tokenType"] = "ERC-20" if token.get("is_erc20") else "ERC-721"
                if tmp_dict["tokenSynbol"] is None:
                    continue
                res.append(tmp_dict)
        return res

    def get_token_holding_2(self,address):
        record=self.db.Balance.find_one({"address":address},{"_id":0})
        if record:
            token_holding = record.get("tokenHolding")
        else:
            token_holding = []

        return token_holding

    def get_transfer_records(self,address,asset,page,perPage=8):

        records=self.db.TransferRecord.find({"$or":[{"addressFrom":address},{"addressTo":address}],"asset":asset},
                                            {"_id":0}).sort([("blockTime",-1)]).skip((page-1)*perPage).limit(perPage)
        return records



    def get_token(self,symbol=None,contractAddress=None):
        if symbol:
            return self.db.Token.find({"symbol":symbol},{"_id":0})
        if contractAddress:
            return self.db.Token.find({"address":contractAddress},{"_id":0})


    def insert_address_nouce(self,address,nouce):
        self.db.Nouce.insert_one({"address":address,"nouce":nouce})

    def get_address_nouce(self,address):
        return self.db.Nouce.find_one({"address":address})

    def update_address_nouce(self,address,nouce):
        self.db.Nouce.update({"address":address},{"$set":{"nouce":nouce}})

    def get_tokens_of_owner(self,contract_name,owner,page):
        db_collection = eval("self.db.{}".format(contract_name), {"self": self})

        return db_collection.find({"owner":owner},{"_id":0}).sort([("birthTime",-1)]).skip((page-1)*8).limit(8)