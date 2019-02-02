from booking import Booker
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    global booker
    booker = Booker(data['username'], data['password'])
    return jsonify(booker.login())

@app.route("/booking/library/<resource_id>", methods = ['GET'])
def check_facil_avaliability(resource_id):
    return jsonify(booker.get_facil_avaliability(resource_id))

@app.route("/booking/library/<resource_id>/book", methods = ['POST'])
def book_facil(resource_id):
    data = request.get_json()
    return jsonify(booker.book_facility(resource_id, data['starttime'], data['endtime']))

if __name__ == "__main__":
    app.run(debug=True)
