import time
from collections import deque

import binascii
import gevent
import requests
from decimal import Decimal

from ethereum.utils import checksum_encode, sha3
from etherscan.accounts import Account

from app import app_logger
from app.utils import fix_address, is_address, get_tokens_from_open_sea, get_tokens_from_ethscan
from config import setting
from .ethClient import Client
from .model import MongodbEth


mongo_client=MongodbEth()

eth_client=Client(eth_url=setting.ETH_URL)

record = mongo_client.get_address_nouce(setting.FUNDING_ADDRESS)
if not record:
    funding_address_nouce = eth_client.web3.eth.getTransactionCount(checksum_encode(setting.FUNDING_ADDRESS))
    mongo_client.insert_address_nouce(setting.FUNDING_ADDRESS,funding_address_nouce)



def construct_tx(addressFrom,addressTo,value,assetId,gasPrice):
    if assetId == "0x":
        unsigned_tx_data=eth_client.construct_eth_tx(addressFrom,addressTo,value,gasPrice)

    else:
        unsigned_tx_data= eth_client.construct_erc20_tx(addressFrom, addressTo, value,assetId, gasPrice)

    before_hash = sha3(binascii.unhexlify(unsigned_tx_data))
    before_hash = binascii.hexlify(before_hash).decode()
    return dict(txData=unsigned_tx_data,txHash=before_hash)



def sign(unsignedTxData,privtKey):
    signature=eth_client.sign(unsignedTxData,privtKey)
    return signature




def broadcast(unsignedTxData,signature):
    res=eth_client.broadcast(unsignedTxData,signature)
    return res


def get_balance(address,assetId):

    if assetId=="0x":
        eth_balance=eth_client.get_balance_of_eth(address)
        return eth_balance
    else:
        erc20_balance = eth_client.get_balance_of_erc20(address,assetId)
        return erc20_balance

def _get_balance(address,assetId):

    if assetId=="0x":
        eth_balance=eth_client.get_balance_of_eth(address)
        return {assetId:eth_balance}
    else:
        erc20_balance = eth_client.get_balance_of_erc20(address,assetId)
        return {assetId:erc20_balance}

def get_many_balance(address,assetIdList):
    task_list = []
    res = []
    for asset in assetIdList:
        task_list.append(gevent.spawn(get_balance,address,asset))

    task_result = gevent.joinall(task_list)

    for task in task_result:
        res.append(task.value)
    return res


def get_token_holding(address):
    asset_list = mongo_client.get_token_holding(address)
    task_list = []
    res = deque([])
    for asset_info in asset_list:
        task_list.append(gevent.spawn(_get_balance,address,asset_info.get("tokenAddress")))


    task_result = gevent.joinall(task_list)
    task_result_0x = gevent.joinall([gevent.spawn(get_balance,address,"0x")])
    asset_dict = {}
    for task in task_result:
        asset_dict.update(task.value)

    for asset_info in asset_list:
        asset_info["balance"] = asset_dict.get(asset_info["tokenAddress"])
        if asset_info.get("tokenIcon"):
            res.appendleft(asset_info)
        else:
            res.append(asset_info)

    res.appendleft({
        "balance":task_result_0x[0].value,
        "tokenAddress": "0x0000000000000000000000000000000000000000",
        "tokenDecimal": "18",
        "tokenIcon": "",
        "tokenName": "Ethereum",
        "tokenSynbol": "ETH",
        "tokenType": "ETH"
        })

    return list(res)




def get_transaction_by_address(address,asset,page):
    address = address.lower()
    try:
        mongo_client.insert_address(address)
    except Exception as e:
        app_logger.error(e)

    txs=[tx for tx in  mongo_client.get_transfer_records(address,asset,page)]
    new_txs = []
    for tx in txs:
        if tx["txReceiptStatus"] == "0":
            tx["txReceiptStatus"] = "-1"
        new_txs.append(tx)

    if page != 1:
        return new_txs
    else:
        if new_txs:
            return new_txs
    my_account = Account(address=address,
                         api_key=setting.API_KEY)
    my_account.PREFIX = setting.ETHSCAN_API_PREFIX

    try:
        res = my_account.get_transaction_page(sort="desc")
    except:
        res = None
    if res:
        tmp_list_0x = []
        tmp_list_contract = []
        for r in res:
            tmp_dict = {}
            input_data = r.get("input")
            if r.get("to") == asset and input_data[:10] == "0xa9059cbb":


                tmp_dict["addressFrom"] = r.get("from")
                tmp_dict["addressTo"] = input_data[34:74]
                tmp_dict["value"] = str(int(input_data[74:],16))
                tmp_dict["txId"] = r.get("hash")
                tmp_dict["gasUsed"] = r.get("gasUsed")
                tmp_dict["gasPrice"] = r.get("gasPrice")
                tmp_dict["gas"] = r.get("gas")
                tmp_dict["blockNumber"] = r.get("blockNumber")
                tmp_dict["blockTime"] = r.get("timeStamp")
                tmp_dict["asset"] = r.get("to")
                tmp_dict["txReceiptStatus"] = r.get("txreceipt_status") if r.get("txreceipt_status")!="0" else "-1"
                tmp_list_contract.append(tmp_dict)

            if input_data == "0x" and asset == "0x00000000000000000000000000000000000000":
                tmp_dict["addressFrom"] = r.get("from")
                tmp_dict["addressTo"] = r.get("to")
                tmp_dict["value"] = r.get("value")
                tmp_dict["txId"] = r.get("hash")
                tmp_dict["gasUsed"] = r.get("gasUsed")
                tmp_dict["gasPrice"] = r.get("gasPrice")
                tmp_dict["gas"] = r.get("gas")
                tmp_dict["blockNumber"] = r.get("blockNumber")
                tmp_dict["blockTime"] = r.get("timeStamp")
                tmp_dict["asset"] = "0x00000000000000000000000000000000000000"
                tmp_dict["txReceiptStatus"] = r.get("txreceipt_status") if r.get("txreceipt_status")!="0" else "-1"
                tmp_list_0x.append(tmp_dict)

        if asset == "0x00000000000000000000000000000000000000":
            tmp_list = tmp_list_0x
        else:
            tmp_list = tmp_list_contract

        if len(tmp_list) > 8:
            return tmp_list[:8]

        return tmp_list

    return []


def get_token_info(queryWord):
    length_of_query_word=len(queryWord)

    if length_of_query_word==42 or length_of_query_word==40:
        queryWord=queryWord if length_of_query_word ==42 else "0x"+queryWord
        queryWord = queryWord.lower()
        query_res = mongo_client.get_token(contractAddress=queryWord)
    else:
        queryWord = queryWord.upper()
        query_res = mongo_client.get_token(symbol=queryWord)

    return [
        {
            "tokenAddress":q.get("address"),
            "tokenDecimal":"0" if q.get("decimals") is None else str(q.get("decimals")),
            "tokenIcon":q.get("icon"),
            "tokenName":q.get("name"),
            "tokenSynbol":q.get("symbol"),
            "tokenType":"ERC-20" if q.get("is_erc20") else "ERC-721"
        }
            for q in query_res]

def write_contract(invoker,contractAddress,method,args):
    args=[fix_address(arg) for arg in args]
    args = [checksum_encode(arg) if is_address(arg) else arg for arg in args]
    res=eth_client.write_contract(invoker, contractAddress, method, args)
    return res

def read_contract(contractAddress,method,args):
    args=[fix_address(arg) for arg in args]
    args = [checksum_encode(arg) if is_address(arg) else arg for arg in args]
    res=eth_client.read_contract(contractAddress, method, args)
    return res

def token_swap(addressTo,value):
    value=Decimal(str(value))*(10**8)
    privt_key=setting.PRIVTKEY
    record_instance = mongo_client.get_address_nouce(setting.FUNDING_ADDRESS)
    nouce = int(record_instance.get("nouce"))
    tx_id= eth_client.token_swap(nouce, addressTo, value,privt_key)
    if tx_id:
        nouce += 1
        mongo_client.update_address_nouce(setting.FUNDING_ADDRESS,nouce)
        return {
            "txId":"0x"+tx_id
        }
    return None

def get_gas_price():
    gas_price=eth_client.get_gas_price()
    return {
        "gasOftransferEth":21000,
        "gasOftransferErc20Tnc":37295,
        "min":gas_price,
        "max":gas_price*30
    }


def faucet(addressTo):
    value_tnc=10
    value_eth=0.1
    address_from="0xcA9f427df31A1F5862968fad1fE98c0a9eE068c4"
    privt_key="9e35c48588711469e13c9a594f9f6d81491ce44ff1e8c5d968fcbd17168088a4"
    tx_id = eth_client.faucet(address_from,addressTo,value_eth,value_tnc,privt_key)[1]
    return {
        "txId":"0x"+tx_id
    }

def transfer(addressFrom, addressTo,value,assetId,privtKey):
    if assetId == "0x":
        tx_id = eth_client.transfer_eth(addressFrom, addressTo, value, privtKey)
    else:
        tx_id= eth_client.transfer_erc20(addressFrom, addressTo,value,assetId, privtKey)

    return "0x"+tx_id


def transfer_erc721(addressFrom,addressTo,tokenId,assetId,privtKey):
    tx_id = eth_client.transfer_erc721(addressFrom,addressTo,tokenId,assetId,privtKey)
    return "0x"+tx_id


def get_tokens_of_owner(contract,owner,page):
    owner = checksum_encode(owner)
    if contract.lower() == "0x06012c8cf97bead5deae237070f9587f8e7a266d":
        tokens = get_tokens_from_open_sea(contract,owner,page)
        tokens = [{
            "tokenId":token.get("token_id"),
            "icon":"https://img.cryptokitties.co/0x06012c8cf97bead5deae237070f9587f8e7a266d/{}.png".format(token.get("token_id")),
            "data":{
                "cooldownIndex":token.get("traits")[0].get("value"),
                "generation":token.get("traits")[1].get("value"),
            }
        } for token in tokens]

    else:
        tokens = get_tokens_from_ethscan(contract,owner,page)
        app_logger.info(contract,owner,page)
        app_logger.info(tokens)
        tokens = [{
            "tokenId":str(token),
            "data":{}
        } for token in tokens]


    return tokens