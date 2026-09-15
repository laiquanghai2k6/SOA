from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

@app.route('/test/<int:idx>',methods=["GET"])
def getItem(idx):
    return{"idx":idx}

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
    