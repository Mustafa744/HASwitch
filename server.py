from flask import Flask, jsonify, request

app = Flask(__name__)

# Define a dictionary to store the state of the switch
switch_state = {
    "is_on": False
}

# define connect endpoint
@app.route("/connect", methods=["GET"])
def connect():
    return jsonify({"message": "Connected to the server!"})

# define disconnect endpoint
@app.route("/disconnect", methods=["GET"])
def disconnect():
    return jsonify({"message": "Disconnected from the server!"})

# define get_devices endpoint
@app.route("/get_devices", methods=["GET"])
def get_devices():
    return jsonify({"name": "My Device", "ip":"192.168.1.6","port": "8080"})

@app.route("/<data>", methods=["GET"])
def get_data(data):
    if data == "on":
        switch_state["is_on"] = True
        return jsonify(switch_state)
    
    elif data == "off":
        switch_state["is_on"] = False
        return jsonify(switch_state)


@app.route("/is_on", methods=["GET"])
def is_on():
    return jsonify(switch_state)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")