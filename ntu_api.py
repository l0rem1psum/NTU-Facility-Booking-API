from booker.booking import Booker
from booker.facilities import FACILITIES
from timetable.timetable import get_courses_registered
from flask import Flask, jsonify, request
import json
app = Flask(__name__)

booker = Booker("Username", "Password")
booker.login()


@app.route("/")
def hello():
    return "Hi"


# @app.route("/login", methods=['POST'])
# def login():
#     data = request.get_json()
#     global booker
#     booker = Booker(data['username'], data['password'])
#     return jsonify(booker.login())


@app.route("/booking/library/facilities", methods=['GET'])
def get_facilities():
    return jsonify(FACILITIES)


@app.route("/booking/library/<resource_id>", methods=['GET'])
def check_facil_avaliability(resource_id):
    return jsonify(booker.get_facil_avaliability(resource_id))


@app.route("/booking/library/<resource_id>/book", methods=['POST'])
def book_facil(resource_id):
    data = request.get_json()
    return jsonify(
        booker.book_facility(resource_id, data['starttime'], data['endtime'],
                             data['date']))


@app.route("/scheduling/<course_code>", methods=['GET'])
def get_course_info(course_code):
    with open("timetable/Y1819S2.json", "r") as j:
        course_info = json.load(j)
    return jsonify(course_info[course_code])


@app.route("/scheduling/<course_code>/exam", methods=['GET'])
def get_exam_info(course_code):
    with open("timetable/Y1819S2_exam.json", "r") as j:
        exam_info = json.load(j)
        if course_code in exam_info:
            return jsonify(exam_info[course_code])
        else:
            return jsonify({
                "code": course_code,
                "description": "No Data",
                "success": False
            })


@app.route("/scheduling/registeredcourses", methods=['GET'])
def get_registered_courses():
    return_dict = {}
    with open("timetable/Y1819S2.json", "r") as j:
        course_info = json.load(j)
        for course in get_courses_registered():
            for i in course_info[course[0]]['index']:
                if i['index_number'] == course[6]:
                    return_dict[course[0]] = i
    return jsonify(return_dict)


if __name__ == "__main__":
    app.run(debug=True, host="172.20.112.96", port=90)
