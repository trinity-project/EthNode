# ETH  增强节点
> 通过josn rpc的方式对外提供与链交互的一些rpc接口

## 服务运行步骤
- 安装python3.5, mongodb数据库
- 安装requirements.txt 所依赖的python库

    `pip install requirements_whl/*.whl`
    
- 在根目录下创建log文件夹
- 设置环境变量 CURRENT_ENVIRON  ,  PRIVTKEY , REMOTE_ADDRESS
- 运行个脚本：
   + store_tx_from_etherscan.py
   通过etherscan提供的获取交易记录的接口将交易记录存到本地Mongodb
   + store_tx.py
    通过块高为参数获取每个块里面的所有交易，只将数据库里面保存的地址的交易记录存进Mongodb
    
   + runserver.py
   启动  rpc 服务

   + extract_token_from_rpc
   解析 token ,数据入库

      + extract_token_holding
   解析 地址持有 token 的种类 ,数据入库
