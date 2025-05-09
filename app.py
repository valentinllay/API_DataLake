from flask import Flask, jsonify
from hello_world.greet import say_hello_world

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
 message = say_hello_world()
 return jsonify({"message": message})

if __name__ == "__main__":
 app.run(host="0.0.0.0", port=5000)
