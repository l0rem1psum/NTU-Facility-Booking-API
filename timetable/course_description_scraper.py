import requests
from robobrowser import RoboBrowser
from lxml import etree
import pandas as pd

COURSE_DESCRIPTION_URL = "https://wish.wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main"
br = RoboBrowser(parser='lxml')

with requests.Session() as s:
    r = s.get(COURSE_DESCRIPTION_URL)
    br._update_state(r)

    form = br.get_form()

    form['r_subj_code'] = "AB1401"
    form['boption'] = 'Search'

    br.submit_form(form)
    tables = pd.read_html(str(br.parsed))
    print(tables)
    # print(br.parsed)
    
 