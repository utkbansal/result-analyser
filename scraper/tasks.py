from datetime import datetime
from multiprocessing import Pool
import time
import sys

from bs4 import BeautifulSoup
from scraper.models import Student, College, Branch, Subject, Marks
import requests
from requests.exceptions import ConnectionError
from xlrd import open_workbook


"""
    For now you have to manually add colleges
"""


def get(url, i=0):
    # this function tries to get a url and fails gracefully in case of a
    # connection error it will try 5 times to get the response after which
    # it will exit the script
    if i in range(5):
        try:
            response = requests.get(url)
            return response

        except ConnectionError:
            print "sleeping..."
            time.sleep(2)
            i += 1
            get(url, i)
    else:
        print 'Connection Error'
        sys.exit(0)


def roll_no_generator(college_code):
    """
    This function generates a list of the first roll number of each branch for
     the given year and college
    :param college_code: college code of college of which the result is required
    :return: roll_no
    """

    # TODO: create another sql script to populate the branch table and then get
    # branch codes form the database
    branch_codes = [
        # '80', '89', '35', '81', '65', '50', '74', '52', '54', '64', '88', '53',
        # '55', '51', '00', '15', '12', '11', '10', '21', '20', '33', '31', '32',
        # '30', '34', '82', '45', '16', '13', '22', '23', '86', '62', '41', '14',
        # '70', '72', '43', '40', '42', '07', '84', '85', '87', '46', '44', '83',
        # '60', '63', '61'
        '00', '10', '21', '31', '32', '13', '40']
    # if datetime.now().month >= 7:
    #     year_code = str(current_year - year + 1)
    # else:
    #     year_code = str(current_year - year)
    year_code = str(12)
    roll_nos = [int(year_code + college_code + branch_code + '001')
                for branch_code in branch_codes]
    return roll_nos


def get_result_data(roll_no, section, year=3):

    with requests.Session() as s:
        # TODO: move the following url to config file
        urls = {
            # New url
            1: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frmBte'
               'ch1uplko2015dghdjhg.aspx',
            # 1: 'http://uptu.ac.in/results/gbturesult_11_12/Even14/frmBTech2MTU
            # _mtu_fhgerifcllpl.aspx',
            2: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frm'
               'Btech3uplko2015fhfdhfdhy.aspx',
            3: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frm'
               'Btech5uplko2015lkjdfg.aspx',
            4: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frm'
               'Btech7uplko2015yykkll.aspx'
        }

        url = urls[year]

        def get_in_session(url, i=0):
            # this function tries to get a url and fails gracefully in case of
            # a connection error it will try 5 times to get the response after
            #  which it will exit the script
            if i in range(5):
                try:
                    response = s.get(url)
                    return response

                except ConnectionError:
                    print "sleeping..."
                    time.sleep(2)
                    i += 1
                    get_in_session(url, i)
            else:
                print 'Connection Error'
                sys.exit(0)

        response = get_in_session(url)

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

    branch_data = soup.find(id='ctl00_ContentPlaceHolder1_lblCourse').text.strip()
    branch_name = branch_data.split('(')[0].split('.')[-1].strip()
    branch_code = branch_data.split(')')[0][-2:]

    carry_papers = soup.find(
        id='ctl00_ContentPlaceHolder1_lblCarryOver').text.split(',')
    ################################################################
    carry_papers = [carry_code.rstrip() for carry_code in carry_papers]

    college = College.objects.filter(code=college_code).first()
    branch = Branch.objects.get_or_create(code=branch_code, name=branch_name)[0]

    student = Student.objects.get_or_create(
        roll_no=roll_no,
        name=name,
        fathers_name=fathers_name,
        college=college,
        branch=branch,
        section=section,
        status=status,
    )[0]
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
                semester=3,
                credit=0,
                back=subject.code in carry_papers,
            )

            marks.save()


def go():
    codes = ['029', '032', '091']
    for code in codes:
        roll_nos = roll_no_generator(code)
        for roll_no in roll_nos:
            error_count = 0
            while True:
                x = get_result_data(roll_no, 0)
                if x is False:
                    if error_count < 10:
                        roll_no+=1
                        error_count += 1
                    else:
                        break

                else:
                    roll_no+=1
                    error_count=0
                    continue



def go2():
    book = open_workbook('master.xls')
    sheet = book.sheet_by_index(7)

    roll_nos = [int(x.value) for x in sheet.col_slice(0)]
    sections = [x.value for x in sheet.col_slice(1)]

    i=0
    for x in roll_nos:
        get_result_data(x, sections[i])
        i+=1


def current_status(roll_no):
    year = 3
    with requests.Session() as s:
        # TODO: move the following url to config file
        urls = {
            # New url
            1: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frmBte'
               'ch1uplko2015dghdjhg.aspx',
            # 1: 'http://uptu.ac.in/results/gbturesult_11_12/Even14/frmBTech2MTU
            # _mtu_fhgerifcllpl.aspx',
            2: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frmBtech3uplko2015fhfdhfdhy.aspx',
            3: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frmBtech5uplko2015lkjdfg.aspx',
            4: 'http://uptu.ac.in/results/gbturesult_11_12/Odd2015Result/frmBtech7uplko2015yykkll.aspx'
        }

        url = urls[year]

        # def get_in_session(url, i=0):
        #     # this function tries to get a url and fails gracefully in case of
        #     # a connection error it will try 5 times to get the response after
        #     # which it will exit the script
        #     if i in range(5):
        #         try:
        #             response = s.get(url)
        #             return response
        #
        #         except ConnectionError:
        #             #print "sleeping..."
        #             time.sleep(2)
        #             i += 1
        #             get_in_session(url, i)
        #     else:
        #         #print 'Connection Error'
        #         sys.exit(0)

        try:
            response = requests.get(url)
        except:
            print 'some error'
            response = requests.get(url)

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
        try:
            response = s.post(url, data=login_credentials)
        except:
            print 'error posting'
            response = s.post(url, data=login_credentials)
    soup = BeautifulSoup(response.text)
    try:
        name = soup.find(id='ctl00_ContentPlaceHolder1_lblName').text.strip()
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
        return 2 # not incomp


def college_status(year):
    """
    Check the result (incomplete/complete) for AKGEC
    :param year:
    :return:
    """

    pool = Pool(16)

    book = open_workbook('master.xls')
    sheet = book.sheet_by_index(7)

    roll_nos = [int(x.value) for x in sheet.col_slice(0)]
    error = 0
    incomplete=0
    complete=0

    status_code = pool.map(current_status, roll_nos)


    print 'Error', status_code.count(0)
    print 'Complete', status_code.count(2)
    print 'Incomplete', status_code.count(1)

if __name__ == '__main__':
    go()