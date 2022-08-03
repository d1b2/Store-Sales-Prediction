from flask import Flask
from store.logger import logging

app=Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    logging.info("Testing logging module")
    return "CI/CD pipeline established"


if __name__=="__main__":
    app.run(debug=True)