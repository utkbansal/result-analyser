from datetime import datetime
from multiprocessing import Pool

from bs4 import BeautifulSoup

from scraper.models import Student, College, Branch, Subject, Marks
import requests


def save_colleges():
    # TODO: remove this function and create a bash script to populate the db from the sql script
    # URL of wikipedia page where list of the institutions of UPTU and their code is given
    url = 'http://en.wikipedia.org/wiki/List_of_colleges_affiliated_to_Uttar_Pradesh_Technical_University'
    response = requests.get(url)
    college_soup = BeautifulSoup(response.text)
    # Slicing the head row
    rows = college_soup.table.find_all('tr')[1:]
    # Adding the colleges and their codes to database
    print 'Adding colleges... '
    for row in rows:
        cols = row.find_all('td')
        college_code = cols[0].text.strip()
        college_name = cols[1].text.strip()
    # Checking if college already present in database
        if college_code not in [college.code for college in College.objects.all()]:
            new_college = College(
                code=college_code,
                name=college_name
            )
            # Saving new college to database
            new_college.save()
    print '...', len(College.objects.all()), ' colleges added'


def roll_no_generator(college_code, year):
    """
    This function generates a list of the first roll number of each branch for the given year
    and college
    :param year: year of which the result is required
    :param college_code: college code of college of which the result is required
    :return: roll_no
    """
    current_year = datetime.now().year % 100
    # TODO: create another sql script to populate the branch table and then get branch codes form the database
    branch_codes = [
    '80', '89', '35', '81', '65', '50', '74', '52', '54', '64','88', '53',
    '55', '51', '00', '15', '12', '11', '10', '21', '20', '33','31', '32',
    '30', '34', '82', '45', '16', '13', '22', '23', '86', '62','41', '14',
    '70', '72', '43', '40', '42', '07', '84', '85', '87', '46','44', '83',
    '60', '63', '61']
    branch_codes = ['00', '10', '21', '31', '32', '13', '40']
    if datetime.now().month >= 7:
        year_code = str(current_year - year)
    else:
        year_code = str(current_year - year - 1)
    roll_nos = [year_code + college_code + branch_code + '001' for branch_code in branch_codes]
    return roll_nos


def get_result_data(roll_no, year):
    with requests.Session() as s:
        # TODO: move the following url to config file
        urls = {
            1: 'http://uptu.ac.in/results/gbturesult_11_12/Even14/frmBTech2MTU_mtu_fhgerifcllpl.aspx',
            2: 'http://uptu.ac.in/results/gbturesult_11_12/Even14/frmBTech4MTU_mtu_jhgrrpifdsdgcwslidp.aspx',
            3: 'http://uptu.ac.in/results/gbturesult_11_12/Even14/frmBTecha6semester_uptuhgnbt65r.aspx',
            4: 'http://uptu.ac.in/results/gbturesult_11_12/even14/frmBtech8semester_uptrkshfplrsncjflvm.aspx'
        }

        url = urls[year]
        response = s.get(url)
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
        response = s.post(url, data=login_credentials)
    soup = BeautifulSoup(response.text)
    try:
        name = soup.find(id='ctl00_ContentPlaceHolder1_lblName').text.strip()
        print 'getting name: ', name
    except AttributeError:
        print 'getting error'
        return False
    college_code = soup.find(id='ctl00_ContentPlaceHolder1_lblInstName')\
        .text.split('(')[-1][:-1]

    if year <= 2:
        roll_no = int(soup.find(
            id='ctl00_ContentPlaceHolder1_lblRollName'
            ).text)
        fathers_name = soup.find(id="ctl00_ContentPlaceHolder1_lblFname").text.strip()
    else:
        roll_no = int(soup.find(
            id='ctl00_ContentPlaceHolder1_lblROLLNO'
            ).text)
        fathers_name = soup.find(id="ctl00_ContentPlaceHolder1_lblF_NAME").text.strip()

    branch_data = soup.find(id='ctl00_ContentPlaceHolder1_lblCourse').text
    branch_name = branch_data.split('(')[0].split('.')[-1].strip()
    branch_code = branch_data.split(')')[0][-2:]
    carry_papers = soup.find(id='ctl00_ContentPlaceHolder1_lblCarryOver').text.split(',')

    data_dict = {
        'student_details': {
            'name': name,
            'fathers_name': fathers_name,
            'college_code': college_code,
            'roll_no': roll_no,
            'branch_name': branch_name,
            'branch_code': branch_code
        },
        'result_odd': {},
        'result_even': {},
        'carry_papers': carry_papers
    }
    tables = soup.find_all('table')
    if year >= 3:
        rows_all = {
            'result_odd': tables[3].find_all('tr')[1:],
            'result_even': tables[5].find_all('tr')[1:]
        }
    else:
        rows_all = {
            'result_odd': tables[2].find_all('tr')[3:],
            'result_even': tables[3].find_all('tr')[3:]
        }

    # This for loop stores different marks of result, it uses try except clause to catch errors
    # which occur due to empty fields such as no practical marks in mathematics.
    for rows in rows_all:
        for row in rows_all[rows]:
            cols = row.find_all('td')
            subject_code = cols[0].text.strip()
            subject_name = cols[1].text.strip()
            if subject_code != '':
                try:
                    marks_te = int(cols[2].text)
                except ValueError:
                    marks_te = 0
                if year <= 2:
                    try:
                        marks_pe = int(cols[3].text)
                    except ValueError:
                        marks_pe = 0
                    try:
                        marks_ts = int(cols[4].text)
                    except ValueError:
                        marks_ts = 0
                    try:
                        marks_ps = int(cols[5].text)
                    except ValueError:
                        marks_ps = 0
                    try:
                        if year == 1:
                            credit = int(cols[7].text)
                        else:
                            credit = int(cols[6].text)
                    except ValueError:
                        credit = 0
                else:
                    marks_pe = 0
                    marks_ps = 0
                    try:
                        marks_ts = int(cols[3].text)
                    except (ValueError, IndexError):
                        marks_ts = 0
                    try:
                        credit = int(cols[5].text)
                    except (ValueError, IndexError):
                        credit = 0
                data_dict[rows][subject_code] = [
                    subject_name, marks_te, marks_pe, marks_ts, marks_ps, credit
                ]
    return data_dict


def save_result_data(college_code, year):
    """
    This function calls get_result_data to get the html page data and stores that data
    to database. It implements a while loop which checks that when roll nos
    have ended and breaks the loop when no data comes for 5 consecutive roll nos
    :param college_code: code of the college of which the result is to be saved
    :param year:
    :return: None
    """

    roll_nos = roll_no_generator(college_code, year)
    # Query which stores existing students in a list roll_no_indb to check for
    # duplicate entries in database if script crashes or interrupted.
    for roll_no in roll_nos:
        not_found = 0
        while not_found < 5:
            print roll_no
            print type(get_result_data(roll_no, year))
            while get_result_data(roll_no, year):
                not_found = 0
                data = get_result_data(roll_no, year)
                if data['student_details']['branch_code'] not in [branch.code for branch in Branch.objects.all()]:
                    new_branch = Branch(
                        name=data['student_details']['branch_name'],
                        code=data['student_details']['branch_code']
                    )
                    new_branch.save()
                    print 'New Branch Added', new_branch.name

                if int(data['student_details']['roll_no']) not in [student.roll_no for student in
                                                                   Student.objects.all()]:
                    new_student = Student(
                        roll_no=roll_no,
                        name=data['student_details']['name'],
                        fathers_name=data['student_details']['fathers_name'],
                        college=College.objects.filter(code=data['student_details']['college_code']).first(),
                        branch=Branch.objects.filter(code=data['student_details']['branch_code']).first()
                    )
                    new_student.save()
                    print 'Roll number added ', new_student.roll_no

                    for key in ['result_odd', 'result_even']:
                        for subject_code in data[key]:
                            if subject_code not in [subject.code for subject in Subject.objects.all()]:
                                new_subject = Subject(
                                    name=data[key][subject_code][0],
                                    code=subject_code
                                )
                                new_subject.save()
                                print 'Subject added ', new_subject.name
                        if key == 'result_odd':
                            sem = 2 * year - 1
                        else:
                            sem = 2 * year

                        for subject_code in data[key]:
                            new_marks = Marks(
                                theory=data[key][subject_code][1],
                                practical=data[key][subject_code][2],
                                internal_theory=data[key][subject_code][3],
                                internal_practical=data[key][subject_code][4],
                                subject=Subject.objects.filter(code=subject_code).first(),
                                student=Student.objects.filter(roll_no=roll_no).first(),
                                credit=data[key][subject_code][5],
                                semester=sem,
                                back=subject_code in data['carry_papers']
                            )
                            new_marks.save()
                    print 'Marks added for ', new_marks.student.name
                # incrementing roll no by one for next iteration
                roll_no = int(roll_no)+1
            not_found = not_found + 1
            roll_no = int(roll_no)+1


def get_college_result(college_code):
    """
    updates subjects, branches and saves data of all the years of college
    of given college_code
    """
    for year in range(1, 5):
        save_result_data(college_code, year)


def start():
    codes = [college.code for college in College.objects.all()]

    pool = Pool(8)
    pool.map(get_college_result, codes)

    print 'Getting results'

if __name__ == '__main__':
    start()