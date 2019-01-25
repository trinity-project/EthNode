
import os

ENVIRON = os.environ


class SettingHolder(object):



    def setup_mainnet(self):
        # self.ETH_URL = "https://mainnet.infura.io/pZc5ZTRYM8wYfRPtoQal"
        self.ETH_URL = "http://127.0.0.1:8545"
        # self.ETH_URL = "http://47.91.249.76:8545"
        self.ETHSCAN_API_PREFIX = "https://api.etherscan.io/api?"


        self.API_KEY = "FQBNNPZ4H5ZEWDYPPGGS5QR4J9DG5FNHCM"

        self.CONTRACT_ADDRESS = "0x67fba6d5eed1f20f8454ab93aed3a010f36f549d"
        self.FUNDING_ADDRESS = "0x0d7c7d0e76e25290abb5bfec7d1adff36befb09f"
        self.PRIVTKEY = ENVIRON.get("PRIVTKEY")
        self.PASSWORD_HASH = "$2b$10$F7GVmj.eahbHMIUjOxooYuLBMqZaIGcJZ7KxufGfbxwGTErKCzNQm"
        self.REMOTE_ADDR = ENVIRON.get("REMOTE_ADDRESS")

        self.REDIS_HOST = "appserver.trinity.ink"
        self.REDIS_PORT = 6379
        self.REDIS_PASSWORD = ENVIRON.get("REDIS_PASSWORD")

        self.MONGO_URI = ENVIRON.get("MONGO_URI")

        self.TOPICS_OF_ERC_TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
    def setup_testnet(self):
        self.ETH_URL = "https://ropsten.infura.io/pZc5ZTRYM8wYfRPtoQal"
        self.ETHSCAN_API_PREFIX = "https://ropsten.etherscan.io/api?"

        self.API_KEY = "FQBNNPZ4H5ZEWDYPPGGS5QR4J9DG5FNHCM"
        self.CONTRACT_ADDRESS = "0x65096f2b7a8dc1592479f1911cd2b98dae4d2218"

        self.FUNDING_ADDRESS = "0xcA9f427df31A1F5862968fad1fE98c0a9eE068c4"
        self.PRIVTKEY = ENVIRON.get("PRIVTKEY")
        self.PASSWORD_HASH = "$2b$10$F7GVmj.eahbHMIUjOxooYuLBMqZaIGcJZ7KxufGfbxwGTErKCzNQm"
        self.REMOTE_ADDR = ENVIRON.get("REMOTE_ADDRESS")

        self.REDIS_HOST = "47.104.81.20"
        self.REDIS_PORT = 9001

        self.MONGO_HOST = "127.0.0.1"
        self.MONGO_PORT = 27017

    def setup_privtnet(self):
        self.ETH_URL = "https://ropsten.infura.io/pZc5ZTRYM8wYfRPtoQal"




ERC20_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "burn",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "burnFrom",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newAdmin",
                        "type": "address"
            }
        ],
        "name": "changeAdmin",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                        "type": "address"
            }
        ],
        "name": "changeAll",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_subtractedValue",
                        "type": "uint256"
            }
        ],
        "name": "decreaseApproval",
        "outputs": [
            {
                "name": "success",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "token",
                        "type": "address"
            },
            {
                "name": "amount",
                        "type": "uint256"
            }
        ],
        "name": "emergencyERC20Drain",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_addedValue",
                        "type": "uint256"
            }
        ],
        "name": "increaseApproval",
        "outputs": [
            {
                "name": "success",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newPausedPublic",
                        "type": "bool"
            },
            {
                "name": "newPausedOwnerAdmin",
                        "type": "bool"
            }
        ],
        "name": "pause",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "_burner",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "Burn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "name": "newState",
                "type": "bool"
            }
        ],
        "name": "PauseOwnerAdmin",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "name": "newState",
                "type": "bool"
            }
        ],
        "name": "PausePublic",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousAdmin",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newAdmin",
                "type": "address"
            }
        ],
        "name": "AdminTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                        "type": "address"
            },
            {
                "name": "_to",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                        "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "admin",
                "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                        "type": "address"
            },
            {
                "name": "_spender",
                        "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                        "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                        "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                        "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
                "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
                "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
                "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pausedOwnerAdmin",
                "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pausedPublic",
                "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
                "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
                "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

#适配大写的 NAME,DECIMALS,SYMBOL
ERC20_ABI_EXCEPTION_1 = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "burn",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "burnFrom",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newAdmin",
                        "type": "address"
            }
        ],
        "name": "changeAdmin",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                        "type": "address"
            }
        ],
        "name": "changeAll",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_subtractedValue",
                        "type": "uint256"
            }
        ],
        "name": "decreaseApproval",
        "outputs": [
            {
                "name": "success",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "token",
                        "type": "address"
            },
            {
                "name": "amount",
                        "type": "uint256"
            }
        ],
        "name": "emergencyERC20Drain",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_addedValue",
                        "type": "uint256"
            }
        ],
        "name": "increaseApproval",
        "outputs": [
            {
                "name": "success",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newPausedPublic",
                        "type": "bool"
            },
            {
                "name": "newPausedOwnerAdmin",
                        "type": "bool"
            }
        ],
        "name": "pause",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "_burner",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "Burn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "name": "newState",
                "type": "bool"
            }
        ],
        "name": "PauseOwnerAdmin",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "name": "newState",
                "type": "bool"
            }
        ],
        "name": "PausePublic",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousAdmin",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newAdmin",
                "type": "address"
            }
        ],
        "name": "AdminTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                        "type": "address"
            },
            {
                "name": "_to",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                        "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "admin",
                "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                        "type": "address"
            },
            {
                "name": "_spender",
                        "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                        "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                        "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                        "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "DECIMALS",
                "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "NAME",
                "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
                "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pausedOwnerAdmin",
                "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pausedPublic",
                "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "SYMBOL",
                "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
                "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

#适配name symbol 返回值是bytes32的
ERC20_ABI_EXCEPTION_2 = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "burn",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "burnFrom",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newAdmin",
                        "type": "address"
            }
        ],
        "name": "changeAdmin",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                        "type": "address"
            }
        ],
        "name": "changeAll",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_subtractedValue",
                        "type": "uint256"
            }
        ],
        "name": "decreaseApproval",
        "outputs": [
            {
                "name": "success",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "token",
                        "type": "address"
            },
            {
                "name": "amount",
                        "type": "uint256"
            }
        ],
        "name": "emergencyERC20Drain",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                        "type": "address"
            },
            {
                "name": "_addedValue",
                        "type": "uint256"
            }
        ],
        "name": "increaseApproval",
        "outputs": [
            {
                "name": "success",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newPausedPublic",
                        "type": "bool"
            },
            {
                "name": "newPausedOwnerAdmin",
                        "type": "bool"
            }
        ],
        "name": "pause",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "_burner",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "Burn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "name": "newState",
                "type": "bool"
            }
        ],
        "name": "PauseOwnerAdmin",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "name": "newState",
                "type": "bool"
            }
        ],
        "name": "PausePublic",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousAdmin",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newAdmin",
                "type": "address"
            }
        ],
        "name": "AdminTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                        "type": "address"
            },
            {
                "name": "_to",
                        "type": "address"
            },
            {
                "name": "_value",
                        "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                        "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                        "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
    },
    {
        "inputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "admin",
                "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                        "type": "address"
            },
            {
                "name": "_spender",
                        "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                        "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                        "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                        "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
                "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
                "outputs": [
            {
                "name": "",
                "type": "bytes32"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
                "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pausedOwnerAdmin",
                "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "pausedPublic",
                "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
                "outputs": [
            {
                "name": "",
                "type": "bytes32"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
                "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]


ERC721_ABI = [
	{
		"constant": True,
		"inputs": [
			{
				"name": "_interfaceId",
				"type": "bytes4"
			}
		],
		"name": "supportsInterface",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_tokenIdList",
				"type": "uint256[]"
			},
			{
				"name": "_tokenOwner",
				"type": "address"
			}
		],
		"name": "createToken",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "getApproved",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_to",
				"type": "address"
			},
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "getNFTbyTokenId",
		"outputs": [
			{
				"name": "attribute",
				"type": "string"
			},
			{
				"name": "birthTime",
				"type": "uint256"
			},
			{
				"name": "status",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			},
			{
				"name": "_uri",
				"type": "string"
			}
		],
		"name": "setTokenURI",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "InterfaceId_ERC165",
		"outputs": [
			{
				"name": "",
				"type": "bytes4"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_from",
				"type": "address"
			},
			{
				"name": "_to",
				"type": "address"
			},
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_owner",
				"type": "address"
			},
			{
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "tokenOfOwnerByIndex",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_from",
				"type": "address"
			},
			{
				"name": "_to",
				"type": "address"
			},
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "exists",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "tokenByIndex",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "ownerOf",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_owner",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_owner",
				"type": "address"
			}
		],
		"name": "tokensOfOwner",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_to",
				"type": "address"
			},
			{
				"name": "_approved",
				"type": "bool"
			}
		],
		"name": "setApprovalForAll",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_from",
				"type": "address"
			},
			{
				"name": "_to",
				"type": "address"
			},
			{
				"name": "_tokenId",
				"type": "uint256"
			},
			{
				"name": "_data",
				"type": "bytes"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "tokenURI",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_owner",
				"type": "address"
			}
		],
		"name": "myTokens",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_tokenId",
				"type": "uint256"
			},
			{
				"name": "attribute",
				"type": "string"
			},
			{
				"name": "status",
				"type": "bool"
			}
		],
		"name": "setNFTbyTokenId",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "_owner",
				"type": "address"
			},
			{
				"name": "_operator",
				"type": "address"
			}
		],
		"name": "isApprovedForAll",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "_newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "buyer",
				"type": "address"
			},
			{
				"indexed": False,
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "BoughtToken",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"name": "tokenId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"name": "result",
				"type": "bool"
			}
		],
		"name": "SetNFTbyTokenId",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "previousOwner",
				"type": "address"
			}
		],
		"name": "OwnershipRenounced",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": True,
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "_from",
				"type": "address"
			},
			{
				"indexed": True,
				"name": "_to",
				"type": "address"
			},
			{
				"indexed": True,
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "_owner",
				"type": "address"
			},
			{
				"indexed": True,
				"name": "_approved",
				"type": "address"
			},
			{
				"indexed": True,
				"name": "_tokenId",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"name": "_owner",
				"type": "address"
			},
			{
				"indexed": True,
				"name": "_operator",
				"type": "address"
			},
			{
				"indexed": False,
				"name": "_approved",
				"type": "bool"
			}
		],
		"name": "ApprovalForAll",
		"type": "event"
	}
]

setting = SettingHolder()

if ENVIRON.get("CURRENT_ENVIRON") == "testnet":
    setting.setup_testnet()
elif ENVIRON.get("CURRENT_ENVIRON") == "mainnet":
    setting.setup_mainnet()
elif ENVIRON.get("CURRENT_ENVIRON") == "privtnet":
    setting.setup_privtnet()
else:
    setting.setup_testnet()
