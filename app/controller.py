from flask import request

from config import setting
from . import jsonrpc, app_logger
from . import service

from .utils import response_wrap, verify_password, lower_address


@response_wrap
@jsonrpc.method("constructTx")
def construct_tx(addressFrom,addressTo,value,assetId,gasPrice=None):
    return service.construct_tx(addressFrom,addressTo,value,assetId,gasPrice)



@response_wrap
@jsonrpc.method("sign")
def sign(txData,privtKey):
    return service.sign(txData,privtKey)

@response_wrap
@jsonrpc.method("broadcast")
def broadcast(rawTx,signature):
    return service.broadcast(rawTx,signature)



@response_wrap
@jsonrpc.method("getBalance")
def get_balance(address,assetId):
    return service.get_balance(address,assetId)

@response_wrap
@jsonrpc.method("getManyBalance")
def get_many_balance(address,assetIdList):
    return service.get_many_balance(address,assetIdList)


@jsonrpc.method("getTokenHolding")
def get_token_holding(address):
    address = address.lower()
    return service.get_token_holding(address)

@jsonrpc.method("getTokenHolding_2")
def get_token_holding_2(address):
    address = address.lower()
    return service.get_token_holding_2(address)

@jsonrpc.method("getTransactionByAddress")
def get_transaction_by_address(address,asset,page=1):
    address=lower_address(address)
    asset = lower_address(asset)
    if asset == "0x":
        asset = "0x00000000000000000000000000000000000000"
    return service.get_transaction_by_address(address,asset,page)


@jsonrpc.method("getTokenInfo")
def get_token_info(queryWord):

    return service.get_token_info(queryWord)


@response_wrap
@jsonrpc.method("writeContract")
def write_contract(invoker,contractAddress,method,args):
    return service.write_contract(invoker,contractAddress,method,args)

@response_wrap
@jsonrpc.method("readContract")
def read_contract(contractAddress,method,args):
    return service.read_contract(contractAddress,method,args)


# for token swap
@jsonrpc.method("autoTransferTNC")
def token_swap(addressTo,value):
    passwd=request.headers.get("Password")
    remote_ip=request.headers.get("X-Real-IP")
    passwd_hash=setting.PASSWORD_HASH
    res = verify_password(passwd, passwd_hash)
    app_logger.info(setting.REMOTE_ADDR)
    app_logger.info(remote_ip)
    if remote_ip== setting.REMOTE_ADDR and res:
        return service.token_swap(addressTo,value)
    return {}

@jsonrpc.method("getGasPrice")
def get_gas_price():
    return service.get_gas_price()


@jsonrpc.method("faucet")
def faucet(addressTo):

    return service.faucet(addressTo)

@jsonrpc.method("transfer")
def transfer(addressFrom,addressTo,value,assetId,privtKey):
    return service.transfer(addressFrom,addressTo,value,assetId,privtKey)

@jsonrpc.method("transferErc721")
def transfer_erc721(addressFrom,addressTo,tokenId,assetId,privtKey):
    return service.transfer_erc721(addressFrom,addressTo,tokenId,assetId,privtKey)


@jsonrpc.method("tokensOfOwner")
def get_tokens_of_owner(contract,owner,page=1):
    page = int(page)
    return service.get_tokens_of_owner(contract,owner,page)

