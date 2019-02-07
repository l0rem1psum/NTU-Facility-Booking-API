from robobrowser import RoboBrowser
import pandas as pd
import re


def get_courses_registered(username="B170007", password="3a1415926535B!!!"):
    TIMETABLE_URL = "https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_check.check_subject_web2&extra=&pg="

    rb = RoboBrowser(parser="lxml")
    rb.open(TIMETABLE_URL)

    form = rb.get_form()
    form['UserName'] = "B170007"
    rb.submit_form(form)

    form = rb.get_form()
    form['PIN'] = '3a1415926535B!!!'
    rb.submit_form(form)

    matric_number = re.search('p1=(.*)&p2', str(rb.parsed))
    matric_number = matric_number.group(1)

    rb.open(
        "https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_check.check_subject_web2?p1="
        + matric_number + "&p2=")

    r = rb.session.post(
        "https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_check.check_subject_web2",
        data={
            "p1": matric_number,
            "p2": '',
            "acad": 2018,
            "semester": 2
        },
        headers={
            "Referer":
            "https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_check.check_subject_web2?p1="
            + matric_number + "&p2="
        })

    rb._update_state(r)

    table = pd.read_html(str(rb.parsed), keep_default_na=False)[0]

    courses_registered_raw = table.iloc[:, [0, 6]].to_dict('records')
    courses_registered = []
    for i in range(1, len(courses_registered_raw)):
        if courses_registered_raw[i][0] != '' and courses_registered_raw[i][
                6] != '':
            courses_registered.append(courses_registered_raw[i])

    return courses_registered