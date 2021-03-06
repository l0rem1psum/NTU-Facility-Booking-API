### TODO:
### During the request for facility availability, the endDataTime and startDataTime parameters should be changed.
### Try successful booking

import requests
import json
from robobrowser import RoboBrowser
from datetime import datetime, time
from pprint import pprint


class Booker():
    LOGIN_URL = "https://ntupcb.ntu.edu.sg/fbscbs/Account/SignIn?ReturnUrl=%2ffbscbs"
    FACILITY_AVALIABILITY_URL = "https://ntupcb.ntu.edu.sg/fbscbs/Booking/CalendarData"
    FACILITY_BOOKING_URL = "https://ntupcb.ntu.edu.sg/fbscbs/Booking/Create?resourceId="

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = RoboBrowser(parser="lxml")
        self.browser.open(Booker.LOGIN_URL)

    def login(self):
        login_form = self.browser.get_form()
        login_form["Username"] = self.username
        login_form["Password"] = self.password
        self.browser.submit_form(login_form)
        if b'Incorrect domain, user name or password' in self.browser.response.content:
            return {"success": "False"}
        else:
            return {"success": "True"}

    def get_facil_avaliability(self, resource_id):
        r = self.browser.session.post(
            Booker.FACILITY_AVALIABILITY_URL,
            data={
                "endDateTime": "2019-02-03T16:00:00.000Z",
                "isOnBehalf": False,
                "resourceId": resource_id,
                "startDateTime": "2019-01-27T16:00:00.000Z",
            },
            headers={
                "Access-Control-Allow-Origin":
                "http://webdavserver.com",
                "Access-Control-Allow-Credentials":
                "true",
                "Access-Control-Allow-Methods":
                "ACL, CANCELUPLOAD, CHECKIN, CHECKOUT, COPY, DELETE, GET, HEAD, LOCK, MKCALENDAR, MKCOL, MOVE, OPTIONS, POST, PROPFIND, PROPPATCH, PUT, REPORT, SEARCH, UNCHECKOUT, UNLOCK, UPDATE, VERSION-CONTROL",
                "Access-Control-Allow-Headers":
                "Overwrite, Destination, Content-Type, Depth, User-Agent, Translate, Range, Content-Range, Timeout, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control, Location, Lock-Token, If",
                "Access-Control-Expose-Headers":
                "DAV, content-length, Allow",
                "X-Requested-With":
                "XMLHttpRequest",
                "Referer":
                "https://ntupcb.ntu.edu.sg/fbscbs/Booking/Create?resourceId=" +
                str(resource_id)
            })
        self.browser._update_state(r)
        parsed_dict = self.format_avaliability_json(json.loads(r.content))
        return parsed_dict

    def format_avaliability_json(self, d):
        for booking in d['Bookings']:
            start_ts = int(booking['StartDateTime'][6:-5])
            end_ts = int(booking['EndDateTime'][6:-5])
            s = datetime.utcfromtimestamp(start_ts)
            e = datetime.utcfromtimestamp(end_ts)
            booking['TimeCoordinate'] = {
                "Weekday": s.weekday() + 1,
                "StartTimeCoordinate": s.hour,
                "EndTimeCoordinate" : e.hour
            }
        return d

    def book_facility(self,
                      resource_id,
                      start_time,
                      end_time,
                      date=datetime.today().strftime('%d/%m/%Y'),
                      number_of_people=1,
                      course_code=str(),
                      purpose_of_use=str()):
        '''
        Date format: dd/mm/yyyy
        Time format: hh:mm:ss
        '''
        r = self.browser.session.get(Booker.FACILITY_BOOKING_URL +
                                     str(resource_id))
        self.browser._update_state(r)
        try:
            booking_form = self.browser.get_form()
            booking_form['StartDateTime.Date'] = date
            booking_form['EndDateTime.Date'] = date
            booking_form['StartDateTime.TimeOfDay'] = start_time
            booking_form['EndDateTime.TimeOfDay'] = end_time
            booking_form['NoOfPeopleExpected'] = number_of_people
            booking_form['CourseCode'] = course_code
            booking_form['PurposeOfUse'] = purpose_of_use
        except ValueError:
            return json.loads('{"success": "False"}')
        else:
            self.browser.submit_form(booking_form)
            return json.loads(self.browser.response.content)