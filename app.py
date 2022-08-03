from flask import Flask
from store.logger import logging
from store.exception import StoreException

app=Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("Testing custom exception")
    except Exception as e:
        store = StoreException(e,sys)
        logging.info(store.error_message)
        logging.info("Testing logging module")
    return "CI CD pipeline has been established."

if __name__=="__main__":
    app.run(debug=True)




