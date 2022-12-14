
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    print("[INFO]/ hello mydb")
    data = {"data": "Hello mydb"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
