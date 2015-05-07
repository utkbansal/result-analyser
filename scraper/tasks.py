from multiprocessing import Pool
import time
import sys

from bs4 import BeautifulSoup
from scraper.models import Student, College, Branch, Subject, Marks
import requests
from requests.exceptions import ConnectionError
from xlrd import open_workbook
from django.conf import settings


def get_in_session(session, url):
    i = 0
    while i < 5:
        try:
            response = session.get(url)
            return response
        except ConnectionError:
            print 'Connection Error'
            time.sleep(1)
            i += 1
    print 'Connection Error'
    sys.exit(0)


def post_in_session(session, url, post_data):
    i = 0
    while i < 5:
        try:
            response = session.post(url, data=post_data)
            return response
        except ConnectionError:
            print 'Connection Error'
            time.sleep(1)
            i += 1
    print 'Connection Error'
    sys.exit(0)


def roll_no_generator(college_code, year_code):
    branch_codes = [branch.code for branch in Branch.objects.all()]

    roll_nos = [int(year_code + college_code + branch_code + '001')
                for branch_code in branch_codes]

    return roll_nos


def get_result_data(roll_no, semester):
    year = (semester + 1) / 2
    with requests.Session() as s:
        url = getattr(settings, 'URLS')[year]
        response = get_in_session(s, url)

        # return response, s
        login_credentials = get_login_credentials(response, roll_no)
        response = post_in_session(s, url, post_data=login_credentials)
        return response


def get_login_credentials(response, roll_no):
    captcha = response.cookies['Captcha'].split('=')[1]
    soup = BeautifulSoup(response.text)
    data1 = str(soup.find(id='__VIEWSTATE')['value'])
    data2 = str(soup.find(id='__VIEWSTATEGENERATOR')['value'])
    data3 = str(soup.find(id='__EVENTVALIDATION')['value'])

    login_credentials = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': data1,
        '__VIEWSTATEGENERATOR': data2,
        '__EVENTVALIDATION': data3,
        'ctl00$ContentPlaceHolder1$txtRoll': str(roll_no),
        'ctl00$ContentPlaceHolder1$capt1$txtcaptcha': captcha,
        'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit'
    }
    return login_credentials


def save_result(arg):
    roll_no = arg[0]
    section = arg[1]
    semester = arg[2]
    print roll_no, section, semester

    response = get_result_data(roll_no, semester)
    soup = BeautifulSoup(response.text)
    try:
        name = soup.find(id='ctl00_ContentPlaceHolder1_lblName').text.strip()
        print 'getting name: ', name
    except AttributeError:
        print 'getting error', roll_no
        return False
    college_code = soup.find(id='ctl00_ContentPlaceHolder1_lblInstName') \
                       .text.split('(')[-1][:-1]

    roll_no = int(soup.find(
        id='ctl00_ContentPlaceHolder1_lblRollName'
    ).text)
    fathers_name = soup.find(
        id="ctl00_ContentPlaceHolder1_lblFname"
    ).text.strip()

    status = soup.find(
        id='ctl00_ContentPlaceHolder1_lblCarryOverStatus'
    ).text.strip()

    branch_data = soup.find(
        id='ctl00_ContentPlaceHolder1_lblCourse').text.strip()
    branch_name = branch_data.split('(')[0].split('.')[-1].strip()
    branch_code = branch_data.split(')')[0][-2:]

    carry_papers = soup.find(
        id='ctl00_ContentPlaceHolder1_lblCarryOver').text.split(',')

    carry_papers = [carry_code.rstrip() for carry_code in carry_papers]

    college = College.objects.filter(code=college_code).first()
    branch = Branch.objects.get_or_create(code=branch_code, name=branch_name)[0]

    student = Student.objects.update_or_create(
        roll_no=roll_no,
        name=name,
        fathers_name=fathers_name,
        college=college,
        defaults={
            'branch': branch,
            'section': section,
            'status': status
        })[0]

    student.save()

    for tr in soup.find_all('table')[3].find_all('tr')[1:]:
        if tr.find_all('span')[0].text.strip() != '':

            subject = Subject.objects.get_or_create(
                name=tr.find_all('span')[1].text.strip(),
                code=tr.find_all('span')[0].text.strip()
            )[0]
            try:
                theory = tr.find_all('span')[2].text.strip()

                theory = int(theory)
            except ValueError:
                theory = 0

            try:
                internal_theory = tr.find_all('span')[3].text.strip()

                internal_theory = int(internal_theory)

            except ValueError:
                internal_theory = 0
            marks = Marks(
                subject=subject,
                student=student,
                theory=int(theory),
                practical=0,
                internal_theory=int(internal_theory),
                internal_practical=0,
                semester=semester,
                credit=0,
                back=subject.code in carry_papers,
            )

            marks.save()


def current_status(arg):
    response = get_result_data(arg[0], arg[1])
    soup = BeautifulSoup(response.text)
    try:
        name = soup.find(id='ctl00_ContentPlaceHolder1_lblName').text.strip()
        print name
    except AttributeError:
        print '0'
        return 0  # error

    status = soup.find(
        id='ctl00_ContentPlaceHolder1_lblCarryOverStatus').text.strip()
    if status == 'INCOMP':
        print '1'
        return 1  # incomp
    else:
        print '2'
        return 2  # not incomp


def akg_result(semester):
    pool = Pool(8)
    book = open_workbook('master2.xls')
    sheet = book.sheet_by_index(0)

    roll_nos = [(int(roll_no.value), int(section.value), semester) for
                roll_no, section in zip(sheet.col_slice(0), sheet.col_slice(1))]
    pool.map(save_result, roll_nos)


def other_college_result():
    codes = [college.code for college in College.objects.all() if
             college.code != '027']
    for code in codes:
        roll_nos = roll_no_generator(code, year_code='13')
        for roll_no in roll_nos:
            error_count = 0
            while True:
                x = get_result_data(roll_no, 0)
                if x is False:
                    if error_count < 10:
                        roll_no += 1
                        error_count += 1
                    else:
                        break

                else:
                    roll_no += 1
                    error_count = 0
                    continue


def college_status(semester):
    pool = Pool(16)

    book = open_workbook('master2.xls')
    sheet = book.sheet_by_index(0)

    roll_nos = [(int(x.value), semester) for x in sheet.col_slice(0)]

    status_code = pool.map(current_status, roll_nos)

    print 'Error', status_code.count(0)
    print 'Complete', status_code.count(2)
    print 'Incomplete', status_code.count(1)