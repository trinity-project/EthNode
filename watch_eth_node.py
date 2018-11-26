import time
from web3 import HTTPProvider, Web3

from project_log import setup_mylogger

INFURA_URL = "https://mainnet.infura.io/pZc5ZTRYM8wYfRPtoQal"
LOCAL_ETHNODE_URL = "http://127.0.0.1:8545"

logger = setup_mylogger(logfile="log/watch_eth_node.log")


def execute_shell_command(command):
    import os
    os.system(command)


def send_email(toAddr,local_block_number,infura_block_number):
    from email.header import Header
    from email.mime.text import MIMEText
    import smtplib

    msg = MIMEText(
        '''' 
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <div id='preview-contents' class='note-content'>
                      
        <h3 >title: restart eth node </h3>

        <p>local block number: {},infura block number:{}</p>

        </div>
        </body>
        </html>'''.format(local_block_number,infura_block_number), 'html', 'utf-8')

    msg['From'] = "no-reply@trinity.tech"
    msg['To'] = toAddr
    msg['Subject'] = Header('notification from WATCH ETH NODE.....')

    server = smtplib.SMTP_SSL("smtp.mxhichina.com", 465)  # SMTP协议默认端口是25
    server.login("no-reply@trinity.tech", "Trinity123456")
    server.sendmail("no-reply@trinity.tech", [toAddr], msg.as_string())
    server.quit()

def compare_block_number():
    infura_w3 = Web3(HTTPProvider(INFURA_URL, {"timeout": 30}))
    local_w3 = Web3(HTTPProvider(LOCAL_ETHNODE_URL, {"timeout": 30}))
    while True:
        try:
            infura_block_number = infura_w3.eth.blockNumber
            local_block_number = local_w3.eth.blockNumber
            logger.info("local_block_number:{},infura_block_number:{}".format(local_block_number, infura_block_number))
            if infura_block_number - local_block_number >= 20:
                execute_shell_command("supervisorctl stop geth")
                logger.warning("stop geth")
                time.sleep(10)
                execute_shell_command("supervisorctl start geth")
                logger.warning("start geth")
                send_email("m17379352738@163.com", local_block_number,infura_block_number)
                time.sleep(2*60*60)
        except:
            pass

        finally:
            time.sleep(120)


if __name__ == "__main__":
    compare_block_number()