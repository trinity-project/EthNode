from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_cors import CORS




app = Flask(__name__)
cors = CORS(app, support_credentials=True)

jsonrpc = JSONRPC(app,'/')


from project_log.my_log import setup_mylogger

app_logger = setup_mylogger(logfile="log/runserver.log")

from .controller import *

