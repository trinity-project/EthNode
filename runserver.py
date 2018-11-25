from app import app
import os

ENVIRON=os.environ
if ENVIRON.get("CURRENT_ENVIRON") == "mainnet":
    debug=False
    host = "127.0.0.1"
else:
    debug=True
    host = "0.0.0.0"

if __name__ == '__main__':
    app.run(host=host, port=21332, debug=debug)
