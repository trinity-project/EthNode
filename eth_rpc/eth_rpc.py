import binascii
import rlp
from ethereum import utils
from ethereum.utils import ecsign, normalize_key, int_to_big_endian, checksum_encode, privtoaddr
from solc import compile_files
from web3 import Web3, HTTPProvider
from ethereum.transactions import Transaction
from eth_abi import encode_abi

from config import setting, ERC20_ABI, ERC721_ABI


class Client(object):

    def __init__(self, eth_url):
        self.web3 = Web3(HTTPProvider(eth_url))

    def get_privtKey_from_keystore(self,filename, password):
        with open(filename) as keyfile:
            encrypted_key = keyfile.read()
            private_key = self.web3.eth.account.decrypt(encrypted_key, password)
            return binascii.hexlify(private_key).decode()

    def transfer_erc20(self,addressFrom,addressTo,value,assetId,privtKey):
        '''
        erc20转账
        '''
        contract_instance=self.get_contract_instance(assetId)
        tx = contract_instance.functions.transfer(
            checksum_encode(addressTo),
            int(value)
        ).buildTransaction({
            'gasPrice': self.web3.eth.gasPrice,
            'gas':97295,
            'nonce': self.web3.eth.getTransactionCount(checksum_encode(addressFrom)),
        })

        signed = self.web3.eth.account.signTransaction(tx, privtKey)
        tx_id=self.web3.eth.sendRawTransaction(signed.rawTransaction)

        return binascii.hexlify(tx_id).decode()

    def transfer_erc721(self,addressFrom,addressTo,tokenId,assetId,privtKey):
        '''
        erc721转账
        '''
        contract_instance=self.get_contract_instance(assetId)
        tx = contract_instance.functions.safeTransferFrom(
            checksum_encode(addressFrom),
            checksum_encode(addressTo),
            int(tokenId)
        ).buildTransaction({
            'gasPrice': self.web3.eth.gasPrice,
            'gas':197295,
            'nonce': self.web3.eth.getTransactionCount(checksum_encode(addressFrom)),
        })

        signed = self.web3.eth.account.signTransaction(tx, privtKey)
        tx_id=self.web3.eth.sendRawTransaction(signed.rawTransaction)

        return binascii.hexlify(tx_id).decode()

    def transfer_eth(self,addressFrom, addressTo, value, privtKey,nounce=None):
        '''
        eth转账
        '''
        dict_tx = {
            "from":addressFrom,
            "to":addressTo,
            "value":int(value),
            "data":b''
        }
        gas_limit = self.estimate_gas(dict_tx)
        nounce = nounce if nounce else self.web3.eth.getTransactionCount(addressFrom)
        tx = Transaction(
            nonce=nounce,
            gasprice=self.web3.eth.gasPrice,
            startgas=gas_limit,
            to=addressTo,
            value=int(value),
            data=b''
        )

        tx.sign(privtKey)
        raw_tx = self.web3.toHex(rlp.encode(tx))
        tx_id = self.web3.eth.sendRawTransaction(raw_tx)
        return binascii.hexlify(tx_id).decode()


    def construct_eth_tx(self, addressFrom, addressTo, value, gasPrice=None):
        '''
        构造eth未签名交易
        '''
        tx = Transaction(
            nonce=self.web3.eth.getTransactionCount(addressFrom),
            gasprice=self.web3.eth.gasPrice if not gasPrice else gasPrice,
            startgas=21000,
            to=addressTo,
            value=int(value),
            data=b''
        )
        UnsignedTransaction = Transaction.exclude(['v', 'r', 's'])
        unsigned_tx = rlp.encode(tx, UnsignedTransaction)
        before_hash = utils.sha3(unsigned_tx)
        return binascii.hexlify(unsigned_tx).decode()

    def construct_erc20_tx(self,addressFrom,addressTo,value,contractAddress,gasPrice=None):
        '''
        构造erc20未签名交易
        '''
        contract_instance=self.get_contract_instance(contractAddress)
        if not contract_instance:
            return None

        tx_dict = contract_instance.functions.transfer(
            checksum_encode(addressTo),
            int(value)
        ).buildTransaction({
            'from': addressFrom,
            'nonce': self.web3.eth.getTransactionCount(addressFrom),
        })

        tx = Transaction(
            nonce=tx_dict.get("nonce"),
            gasprice=tx_dict.get("gasPrice") if not gasPrice else gasPrice,
            startgas=tx_dict.get("gas"),
            to=tx_dict.get("to"),
            value=tx_dict.get("value"),
            data=binascii.unhexlify(tx_dict.get("data")[2:]))

        UnsignedTransaction = Transaction.exclude(['v', 'r', 's'])
        unsigned_tx = rlp.encode(tx, UnsignedTransaction)
        before_hash = utils.sha3(unsigned_tx)
        return binascii.hexlify(unsigned_tx).decode()


    def sign(self, unsigned_tx, privtKey):
        '''
        对交易签名
        '''
        before_hash = utils.sha3(binascii.unhexlify(unsigned_tx.encode()))
        v,r,s=ecsign(before_hash,normalize_key(privtKey))
        signature = binascii.hexlify(int_to_big_endian(r) + int_to_big_endian(s) +
                                     bytes(chr(v).encode())).decode()
        return signature




    def broadcast(self, unsigned_tx,signature):
        '''
        将未签名的交易和签名组装在一起广播出去
        '''
        signature=binascii.unhexlify(signature.encode())
        unsigned_tx=binascii.unhexlify(unsigned_tx.encode())
        r = signature[0:32]
        s = signature[32:64]
        v = bytes(chr(signature[64]).encode())

        unsigned_items = rlp.decode(unsigned_tx)
        unsigned_items.extend([v, r, s])
        signed_items = unsigned_items

        signed_tx_data = rlp.encode(signed_items)
        tx_id = self.web3.eth.sendRawTransaction(signed_tx_data)
        return "0x"+binascii.hexlify(tx_id).decode()

    def sendTransaction(self,addressFrom, addressTo, value,startgas,data,privtKey):
        tx = Transaction(
            nonce=self.web3.eth.getTransactionCount(addressFrom),
            gasprice=self.web3.eth.gasPrice,
            startgas=startgas,
            to=addressTo,
            value=value,
            data=data
        )

        tx.sign(privtKey)
        raw_tx = self.web3.toHex(rlp.encode(tx))
        tx_id = self.web3.eth.sendRawTransaction(raw_tx)

        return tx_id.hex()


    def deploy_contract(self,contract_file_name, contract_name,addressFrom, privtKey,contract_args=None,import_remappings=[]):
        '''
        部署合约
        '''
        # compiled_sol = compile_source(solidity_code)
        compiled_sol = compile_files([contract_file_name],import_remappings=import_remappings)
        contract_interface = compiled_sol.get("{}:{}".format(contract_file_name, contract_name))
        bytecode = contract_interface['bin']
        abi = contract_interface['abi']
        if contract_args:
            args_abi = self.constructor_abi(contract_args[0],contract_args[1])
            if args_abi:
                bytecode += args_abi
        data = binascii.unhexlify(bytecode.encode())
        gas_limit = self.web3.eth.estimateGas({"from": addressFrom, "value": "0x0", "data": bytecode})
        tx_id = self.sendTransaction(
                                addressFrom=addressFrom,
                                addressTo="",
                                value=0,
                                startgas=gas_limit,
                                data=data,
                                privtKey=privtKey
        )

        # tx_receipt = w3.eth.waitForTransactionReceipt(reszult)
        # contract_address = tx_receipt['contractAddress']

        return tx_id,bytecode,abi

    def compiler_contract(self,contract_file_name, contract_name,contract_args=None,import_remappings=[]):
        '''
        编译合约
        '''
        compiled_sol = compile_files([contract_file_name],import_remappings=import_remappings)
        contract_interface = compiled_sol.get("{}:{}".format(contract_file_name, contract_name))
        bytecode = contract_interface['bin']
        if contract_args:
            args_abi = self.constructor_abi(contract_args[0],contract_args[1])
            if args_abi:
                bytecode += args_abi
        return bytecode

    def get_contract_instance(self, contract_address,abi):
        '''
        获取合约实例
        '''
        contract_address = checksum_encode(contract_address)
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        return contract

    def get_contract_instance_erc721(self, contract_address):
        '''
        获取合约实例
        '''
        contract_address = checksum_encode(contract_address)
        contract = self.web3.eth.contract(address=contract_address, abi=ERC721_ABI)
        return contract

    def write_contract(self, invoker, contractAddress, method, args,value,gas_limit=200000,gasPrice=None,abi=ERC20_ABI):
        '''
        调用合约里实现的方法
        '''
        invoker = checksum_encode(invoker)
        contractAddress = checksum_encode(contractAddress)
        contract_instance = self.get_contract_instance(contractAddress,abi)
        if not contract_instance:
            return None
        nounce = self.web3.eth.getTransactionCount(invoker)
        tx_dict = contract_instance.functions[method](*args).buildTransaction({
            'gasPrice': self.web3.eth.gasPrice if not gasPrice else gasPrice,
            'from':invoker,
            'nonce': nounce,
            "gas":gas_limit,
            "value":value
        })
        tx = Transaction(
            nonce=tx_dict.get("nonce"),
            gasprice=tx_dict.get("gasPrice"),
            startgas=tx_dict.get("gas"),
            to=tx_dict.get("to"),
            value=tx_dict.get("value"),
            data=binascii.unhexlify(tx_dict.get("data")[2:]))

        UnsignedTransaction = Transaction.exclude(['v', 'r', 's'])
        unsigned_tx = rlp.encode(tx, UnsignedTransaction)

        return binascii.hexlify(unsigned_tx).decode()

    def read_contract(self, contractAddress, method, args):
        '''
        读取合约状态
        '''
        contractAddress = checksum_encode(contractAddress)
        contract_instance = self.get_contract_instance(contractAddress)
        if not contract_instance:
            return None

        result = contract_instance.functions[method](*args).call()

        return result

    def read_contract_erc721(self, contractAddress, method, args):
        '''
        读取合约状态
        '''
        contractAddress = checksum_encode(contractAddress)
        contract_instance = self.get_contract_instance_erc721(contractAddress)
        if not contract_instance:
            return None

        result = contract_instance.functions[method](*args).call()

        return result

    def sign_args(self,typeList, valueList, privtKey):
        '''

        :param typeList: ['bytes32', 'bytes32', 'uint256', 'uint256']
        :param valueList: ["0x3ae88fe370c39384fc16da2c9e768cf5d2495b48", "0x9da26fc2e1d6ad9fdd46138906b0104ae68a65d8", 1, 1]
        :param privtKey: "095e53c9c20e23fd01eaad953c01da9e9d3ed9bebcfed8e5b2c2fce94037d963"
        :return:
        '''
        data_hash = Web3.soliditySha3(typeList, valueList)
        v, r, s = ecsign(data_hash, normalize_key(privtKey))
        signature = binascii.hexlify(int_to_big_endian(r) + int_to_big_endian(s)
                                     + bytes(chr(v - 27).encode()))
        return signature

    def get_balance_of_eth(self,address):
        address = checksum_encode(address)
        return self.web3.eth.getBalance(address)

    def get_balance_of_erc20(self,address,contractAddress):
        address = checksum_encode(address)
        contractAddress = checksum_encode(contractAddress)
        contract_instance = self.get_contract_instance(contractAddress)
        return contract_instance.functions.balanceOf(address).call()



    def get_transaction_receipt_by_hash(self,txId):
        res=self.web3.eth.getTransactionReceipt(txId)
        return res


    def get_gas_price(self):
        gas_price=self.web3.eth.gasPrice
        return gas_price

    def estimate_gas(self,dict_transaction):
        return self.web3.eth.estimateGas(dict_transaction)

    def constructor_abi(self,typeList,valueList):
        '''

        :param typeList: ['string', 'string', 'uint8', 'uint256']
        :param valueList: ['testtoken', 'test', 8, 10000000000]
        :return:
        '''
        try:
            encoded_abi = encode_abi(typeList,valueList).hex()
        except:
            encoded_abi = None
        return encoded_abi


    def faucet(self,addressFrom, addressTo, value_eth,value_tnc, privtKey):
        '''

        测试网水龙头
        '''
        dict_tx = {
            "from":addressFrom,
            "to":addressTo,
            "value":int(value_eth*(10**18)),
            "data":b''
        }
        gas_limit = self.estimate_gas(dict_tx)
        nonce = self.web3.eth.getTransactionCount(addressFrom)

        tx_eth = Transaction(
            nonce=nonce,
            gasprice=self.web3.eth.gasPrice,
            startgas=gas_limit,
            to=addressTo,
            value=int(value_eth*(10**18)),
            data=b''
        )

        tx_eth.sign(privtKey)
        raw_tx_eth = self.web3.toHex(rlp.encode(tx_eth))
        tx_id_eth = self.web3.eth.sendRawTransaction(raw_tx_eth)

        contract_instance=self.get_contract_instance(setting.CONTRACT_ADDRESS)
        tx_tnc = contract_instance.functions.transfer(
            checksum_encode(addressTo),
            int(value_tnc*(10**8))
        ).buildTransaction({
            'gasPrice': self.web3.eth.gasPrice,
            'gas':97295,
            'nonce': nonce+1,
        })

        signed = self.web3.eth.account.signTransaction(tx_tnc, privtKey)
        tx_id_tnc=self.web3.eth.sendRawTransaction(signed.rawTransaction)


        return binascii.hexlify(tx_id_eth).decode(),binascii.hexlify(tx_id_tnc).decode()




    def token_swap(self,nouce, addressTo, value,privtKey):
        addressTo = checksum_encode(addressTo)
        contractAddress = checksum_encode(setting.CONTRACT_ADDRESS)
        contract_instance = self.web3.eth.contract(address=contractAddress,abi=ERC20_ABI)

        tx = contract_instance.functions.transfer(
            checksum_encode(addressTo),
            int(value)
        ).buildTransaction({
            'gasPrice': self.web3.eth.gasPrice,
            'gas':97295,
            'nonce': nouce,
        })


        signed = self.web3.eth.account.signTransaction(tx, privtKey)
        tx_id=self.web3.eth.sendRawTransaction(signed.rawTransaction)

        return binascii.hexlify(tx_id).decode()





