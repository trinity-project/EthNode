from functools import wraps
from enum import Enum
import requests
from flask import jsonify
from etherscan.contracts import Contract

from config import setting


def response_wrap(func):
    @wraps(func)
    def wrapper():
        response=func()
        return jsonify(response)
    return wrapper


class ASSET_TYPE(Enum):
    TNC=2443
    NEO=1376
    GAS=1785
    ETH=1027

def get_price_from_coincapmarket(asset_type):
    coincapmarket_api="https://api.coinmarketcap.com/v2/ticker/{0}/?convert=CNY".format(asset_type)
    res=requests.get(coincapmarket_api).json()
    return res.get("data").get("quotes").get("CNY").get("price")

def verify_password(password, hashed):
    import bcrypt
    if isinstance(password, str):
        password = password.encode("utf-8")
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    try:
        result = bcrypt.checkpw(password, hashed)
    except Exception:
        result = False
    return result


def lower_address(address):
    return address.lower()

def is_address(address):
    if len(address)==42 :
        return True
    return False

def fix_address(address):

    if len(address)==40:
        return "0x"+address
    else:
        return address

def get_contract_abi(contract_address):

    my_contract = Contract(address=contract_address,api_key=setting.API_KEY)
    my_contract.PREFIX =setting.ETHSCAN_API_PREFIX
    try:
        res = my_contract.get_abi()
    except:
        res = None

    return res

def get_tokens_from_open_sea(contract,owner,page):
    limit = 8
    offset = (page-1)*limit
    open_sea_api = "https://api.opensea.io/api/v1/assets?owner={}&order_by=token_id&order_direction=asc&asset_contract_address={}&offset={}&limit={}".format(owner,contract,offset,limit)
    try:
        res=requests.get(open_sea_api).json()
        return res.get("assets")
    except Exception as e:
        return []

