from .models import Student
import xlsxwriter


def result_dict(college_code, branch_code, sem):
    """
    makes a dictionary of result data of given
    each student of given college_code and branch_code
    and appends it to a list and returns that list
    returns: a list of dictionaries containing
    data of each student
    """
    ls = []
    required_students = Student.objects.filter(college=college_code, branch=branch_code).all()
    len(required_students)
    for student in required_students:
        st_dict = {}
        for mrks in student.marks_set.all():
            if mrks.semester == sem:
                if not st_dict:
                    st_dict['marks'] = {}
                st_dict['marks'][mrks.subject.code] = [mrks.subject.name, mrks.theory, mrks.practical,
                                                       mrks.internal_theory, mrks.internal_practical]
        if st_dict:
            st_dict['name'] = student.name
            st_dict['fathers_name'] = student.fathers_name
            st_dict['roll_no'] = student.roll_no
            ls.append(st_dict)
    return ls


def create_excel(college_code, branch_code, sem):
    results = result_dict(college_code, branch_code, int(sem))
    #print results

    workbook = xlsxwriter.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()

    # Creating format properties

    worksheet.set_column(0, 0, 12)
    worksheet.set_column(1, 2, 25)

    i = 2

    subject_codes = results[0]['marks'].keys()
    for num in range(len(subject_codes)):
        if subject_codes[num][1:4] == 'OE0':
            subject_codes[num] = 'Open Elective'
    # Print subject codes in first row
    for j in range(len(results[0]['marks'].keys())):
        worksheet.merge_range(0, j*3 + 3, 0, (j + 1)*3 + 2, subject_codes[j])

    worksheet.write(0, 0, 'Roll No')
    worksheet.write(0, 1, 'Name')
    worksheet.write(0, 2, 'Fathers Name')

    for c in range(3, 3 * len(subject_codes) + 3):
        if c % 3 == 0:
            worksheet.write(1, c, 'External')
        elif c % 3 == 1:
            worksheet.write(1, c, 'Internal')
        else:
            worksheet.write(1, c, 'Total')

    for result in results:

        keys = result['marks'].keys()
        # printing marks
        for k in range(0, 3*len(keys), 3):
            worksheet.write(i, k+3, result['marks'][keys[k/3]][1]+result['marks'][keys[k/3]][2])
            worksheet.write(i, k+4, result['marks'][keys[k/3]][3]+result['marks'][keys[k/3]][4])
            worksheet.write(i, k+5, result['marks'][keys[k/3]][1]+result['marks'][keys[k/3]][2]
                            + result['marks'][keys[k/3]][3]+result['marks'][keys[k/3]][4])

        worksheet.write(i, 0, result['roll_no'])
        worksheet.write(i, 1, result['name'])
        worksheet.write(i, 2, result['fathers_name'])

        i += 1

    workbook.close()