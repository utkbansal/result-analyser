from scraper.models import *
import xlsxwriter


# def count(code):
# branch_code = '31'
#
#
# sub = Subject.objects.filter(code=code).first()
# all_marks = sub.marks_set.all()
#     branch_marks = [marks for marks in all_marks if marks.student.branch==
#                     Branch.objects.filter(code = branch_code).first()]
#     number_of_backs = len([marks for marks in branch_marks if marks.back])
#
#     print number_of_backs


def rd(college, branch):
    students = [student for student in
                Student.objects.filter(college=college, branch=branch)
                if student.status != 'INCOMP']
    return len(students)


def back(college, branch):
    students = Student.objects.filter(college=college, branch=branch)
    students = [student for student in students if student.status != 'INCOMP']
    back = 0
    for student in students:
        for marks in student.marks_set.all():
            if marks.back:
                # print student.roll_no
                back += 1
                break
    return back


def incomp(college, branch):
    students = [student for student in
                Student.objects.filter(college=college, branch=branch)
                if student.status == 'INCOMP']

    return len(students)


def college_compare():
    workbook = xlsxwriter.Workbook('data.xlsx')

    colleges = College.objects.all()
    for college in colleges:
        i = 4

        worksheet = workbook.add_worksheet(college.code)
        worksheet.write(0, 0, college.name)
        worksheet.write(3, 0, 'Branch')
        worksheet.write(3, 1, 'INCOMP')
        worksheet.write(3, 2, 'RD')
        worksheet.write(3, 3, 'PCP')
        worksheet.write(3, 4, 'Pass')
        worksheet.write(3, 5, 'Pass %')

        for branch in Branch.objects.all():
            if len(Student.objects.filter(college=college, branch=branch)) != 0:
                worksheet.write(i, 0, branch.codename)
                worksheet.write(i, 1, incomp(college, branch))
                print college, branch
                declared = rd(college, branch)
                worksheet.write(i, 2, declared)
                backs = back(college, branch)
                worksheet.write(i, 3, backs)
                clear = declared - backs
                worksheet.write(i, 4, clear)
                try:
                    clear_perc = (float(clear) / declared) * 100
                except ZeroDivisionError:
                    clear_perc = 0
                worksheet.write(i, 5, round(clear_perc, 2))
            i += 1

    workbook.close()


def college_back(code):
    students = [student for student in Student.objects.filter(college=code) if
                student.status != 'INCOMP']
    back = 0
    for s in students:
        for marks in s.marks_set.all():
            if marks.back:
                back += 1
                break

    print back


def pass_perc(code):
    students = [student for student in Student.objects.filter(college=code) if
                student.status != 'INCOMP']
    print len(students)
    back = college_back(code)
    print back


def max_of_subject_total(code):
    subject = Subject.objects.filter(code=code).first()
    # return subject.max_internal + subject.max_external
    n = max([
        marks.theory + marks.internal_theory
        for marks in subject.marks_set.all()])
    if n == 0:
        return 0
    elif n in range(26):
        return 25
    elif n in range(31):
        return 30
    elif n in range(51):
        return 50
    elif n in range(76):
        return 75
    elif n in range(101):
        return 100
    elif n in range(126):
        return 125
    elif n in range(151):
        return 150
    elif n in range(176):
        return 175
    elif n in range(201):
        return 200
    elif n in range(226):
        return 225
    elif n in range(251):
        return 250
    elif n in range(276):
        return 275
    elif n in range(301):
        return 300
    elif n in range(326):
        return 325
    elif n in range(351):
        return 350
    elif n in range(376):
        return 375
    elif n in range(401):
        return 400
    elif n in range(426):
        return 425
    elif n in range(451):
        return 450
    elif n in range(476):
        return 475
    else:
        return 500


def max_of_subject_external(code):
    """
    It finally went wrong for 4th year
    :param code:
    :return:
    """
    subject = Subject.objects.filter(code=code).first()
    # return subject.max_external
    n = max([
        marks.theory
        for marks in subject.marks_set.all()])
    if n == 0:
        return 0
    elif n in range(26):
        return 25
    elif n in range(31):
        return 30
    elif n in range(51):
        return 50
    elif n in range(76):
        return 75
    elif n in range(101):
        return 100
    elif n in range(126):
        return 125
    elif n in range(151):
        return 150
    elif n in range(176):
        return 175
    elif n in range(201):
        return 200
    elif n in range(226):
        return 225
    elif n in range(251):
        return 250
    elif n in range(276):
        return 275
    elif n in range(301):
        return 300
    elif n in range(326):
        return 325
    elif n in range(351):
        return 350
    elif n in range(376):
        return 375
    elif n in range(401):
        return 400
    elif n in range(426):
        return 425
    elif n in range(451):
        return 450
    elif n in range(476):
        return 475
    else:
        return 500


def avg(college_code):
    students = Student.objects.filter(college=college_code)
    students = [student for student in students if student.status != 'INCOMP']
    total_marks = 0


    ############### For 4th Year ################
    maximum = 500
    #############################################


    # maximum = 600
    # maximum = 0
    # print students[0].roll_no
    # for mark in students[0].marks_set.all():
    #     print mark.subject
    #     print max_of_subject_external(mark.subject.code)
    #     maximum = maximum + max_of_subject_total(mark.subject.code)
    # print maximum
    for student in students:
        marks = student.marks_set.all()
        for mark in marks:
            if mark.subject.code != 'AUC001':
                total_marks += mark.theory
    avg_marks = float(total_marks) / len(students)

    return avg_marks, (avg_marks / maximum) * 100


def external_avg():
    workbook = xlsxwriter.Workbook('external_avg.xlsx')
    sheet = workbook.add_worksheet()
    j = 1
    for college in College.objects.all():
        i = 0
        sheet.write(0, 0, 'College')
        sheet.write(1, 0, 'Average Marks')
        sheet.write(2, 0, 'Percentage')
        sheet.write(i, j, college.name)
        total, average = avg(college.code)
        sheet.write(i + 1, j, round(total, 2))
        sheet.write(i + 2, j, round(average, 2))

        j += 1
    workbook.close()


def pass_fail(sub_code, col_code):
    students = [student for student in Student.objects.filter(college=col_code)
                if student.status != 'INCOMP']
    total = 0
    clear = 0
    fail = 0

    for student in students:
        marks = student.marks_set.all()
        sub = Subject.objects.filter(code=sub_code).first()
        for mark in marks:
            if mark.subject == sub:
                if mark.back == True:
                    fail += 1
                    total = total + 1
                    break

                else:
                    clear += 1
                    total = total + 1
                    break

    return total, clear, fail


def subject_wise():
    subjects = Subject.objects.all()
    colleges = College.objects.all()
    workbook = xlsxwriter.Workbook('yyy.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(3, 0, 'Subject Code')
    worksheet.write(3, 1, 'Subject Name')
    i = 4
    for subject in subjects:
        worksheet.write(i, 1, subject.name)
        worksheet.write(i, 0, subject.code)
        j = 2
        for college in colleges:
            worksheet.write(2, j, college.name)
            total, clear, fail = pass_fail(subject.code, college.code)
            print 'aaya'
            worksheet.write(i, j, total)
            try:
                worksheet.write(i, j + 1,
                                round((float(clear) / total) * 100, 2))
            except ZeroDivisionError:
                worksheet.write(i, j + 1, '0')
            #print round((float(clear)/total)*100,2)
            try:
                worksheet.write(i, j + 2, round((float(fail) / total) * 100, 2))
            except ZeroDivisionError:
                worksheet.write(i, j + 2, '0')
            print 'blah'
            j = j + 3
        i = i + 1
    workbook.close()


# def back_students(col_code):
#     subjects = [s for s in Subject.objects.all() if s.code != 'NAS154']
#     # NAS154 was alag wala professional communicstion in jss of 1 student
#
#     workbook = xlsxwriter.Workbook('data.xlsx')
#     bold = workbook.add_format()
#     bold.set_bold()
#     bold.set_align('center')
#
#     for subject in subjects:
#         i = 3
#
#         worksheet = workbook.add_worksheet(subject.code)
#         worksheet.write(0, 0, subject.name + subject.code, bold)
#         worksheet.write(2, 0, 'S.No.', bold)
#         worksheet.write(2, 1, 'Roll No.', bold)
#         worksheet.write(2, 2, 'Name', bold)
#         worksheet.write(2, 3, "Father's Name", bold)
#         worksheet.write(2, 4, "Branch", bold)
#         worksheet.write(2, 5, 'Section', bold)
#         worksheet.write(2, 6, 'Internal', bold)
#         worksheet.write(2, 7, 'External', bold)
#         worksheet.write(2, 8, 'Total', bold)
#         worksheet.write(2, 9, 'Status', bold)
#
#         students = [student for student in
#                     Student.objects.filter(college=col_code)
#                     if student.status != 'INCOMP']
#
#         print len(students)
#         clear = 0
#
#         for student in students:
#             marks = student.marks_set.all()
#             sub = Subject.objects.filter(code=subject.code).first()
#
#             for mark in marks:
#                 if mark.subject == sub:
#                     if mark.back is True:
#                         worksheet.write(i, 0, i - 2)
#                         worksheet.write(i, 1, student.roll_no)
#                         worksheet.write(i, 2, student.name)
#                         worksheet.write(i, 3, student.fathers_name)
#                         worksheet.write(i, 4, student.branch.code)
#                         worksheet.write(i, 5, student.section)
#                         worksheet.write(i, 6, Marks.objects.filter(student = student, subject = sub).first().internal_theory)
#                         worksheet.write(i, 7, Marks.objects.filter(student = student, subject = sub).first().theory)
#                         worksheet.write(i, 8, Marks.objects.filter(student = student, subject = sub).first().theory+
#                                         Marks.objects.filter(student=student,
#                                                              subject=sub).first().internal_theory)
#                         worksheet.write(i, 9, student.status)
#                         i += 1
#                         break
#
#     workbook.close()


def faculty_performance():
    branches = Branch.objects.all()
    workbook = xlsxwriter.Workbook('fac.xlsx')
    for branch in branches:
        print branch
        worksheet = workbook.add_worksheet(branch.code)
        worksheet.write(0, 0, branch.name)
        students1 = Student.objects.filter(branch=branch, college='027')
        sec = []
        for student in students1:
            sec.append(student.section)
        sec = set(sec)
        ############################################################

        worksheet.write(1, 0, 'Subject')
        worksheet.write(1, 1, 'Code')
        worksheet.write(1, 2, 'Total Students')
        worksheet.write(1, 3, 'External Avg %')
        worksheet.write(1, 4, 'Total Avg %')
        worksheet.write(1, 5, 'Pass %')
        worksheet.write(1, 6, 'Fail %')

        i = 3
        subjects_len = 0
        for s in sec:

            worksheet.write(i, 0, 'Section' + s)
            i += 1
            students = [student for student in students1 if
                        student.section == s and student.status != 'INCOMP']

            subjects = []
            for student in students:
                for mark in student.marks_set.all():
                    subjects.append(mark.subject)

            subjects = set(subjects)
            # subjects.remove('GP101')
            subjects_len = len(subjects)

            for sub in subjects:
                worksheet.write(i, 0, sub.name)
                worksheet.write(i, 1, sub.code)

                back = 0
                clear = 0
                external = 0
                total = 0
                for student in students:
                    marks = student.marks_set.all()
                    for mark in marks:
                        if mark.subject == sub:
                            external = external + mark.theory
                            total = total + mark.theory + mark.internal_theory
                            if mark.back is True:
                                back += 1
                                print student.roll_no
                            else:

                                clear += 1
                worksheet.write(i, 2, back + clear)
                total_students = back + clear
                avg = float(external) / total_students
                try:
                    perc = (avg / max_of_subject_external(sub.code)) * 100
                except ZeroDivisionError:
                    perc = 0
                total = (float(total) / total_students)
                total_avg = (total / max_of_subject_total(sub.code)) * 100
                worksheet.write(i, 3, round(perc, 2))
                worksheet.write(i, 4, round(total_avg, 2))
                try:
                    worksheet.write(i, 5,
                                    round((float(clear) / total_students) * 100,
                                          2))
                except ZeroDivisionError:
                    worksheet.write(i, 5, '0')
                try:
                    worksheet.write(i, 6,
                                    round((float(back) / total_students) * 100,
                                          2))
                except ZeroDivisionError:
                    worksheet.write(i, 6, '0')
                i += 1
        i = i + subjects_len
    workbook.close()


def complete_student_status(col_code):
    subjects = [s for s in Subject.objects.all() if s.code != 'NAS154']
    # NAS154 was alag wala professional communicstion in jss of 1 student

    workbook = xlsxwriter.Workbook('status.xlsx')
    bold = workbook.add_format()
    bold.set_bold()
    bold.set_align('center')

    for subject in subjects:
        i = 3

        worksheet = workbook.add_worksheet(subject.code)
        worksheet.write(0, 0, subject.name + ' ' + subject.code, bold)
        worksheet.write(2, 0, 'S.No.', bold)
        worksheet.write(2, 1, 'Roll No.', bold)
        worksheet.write(2, 2, 'Name', bold)
        worksheet.write(2, 3, "Father's Name", bold)
        worksheet.write(2, 4, "Branch", bold)
        worksheet.write(2, 5, 'Section', bold)
        worksheet.write(2, 6, 'Internal', bold)
        worksheet.write(2, 7, 'External', bold)
        worksheet.write(2, 8, 'Total', bold)
        worksheet.write(2, 9, 'Status', bold)

        students = [student for student in
                    Student.objects.filter(college=col_code)]

        print len(students)
        clear = 0

        for student in students:
            marks = student.marks_set.all()
            sub = Subject.objects.filter(code=subject.code).first()

            for mark in marks:
                if mark.subject == sub:
                    worksheet.write(i, 0, i - 2)
                    worksheet.write(i, 1, student.roll_no)
                    worksheet.write(i, 2, student.name)
                    worksheet.write(i, 3, student.fathers_name)
                    worksheet.write(i, 4, student.branch.codename)
                    worksheet.write(i, 5, student.section)
                    worksheet.write(i, 6,
                                    Marks.objects.filter(student=student,
                                                         subject=sub).first().internal_theory)
                    worksheet.write(i, 7,
                                    Marks.objects.filter(student=student,
                                                         subject=sub).first().theory)
                    worksheet.write(i, 8,
                                    Marks.objects.filter(student=student,
                                                         subject=sub).first().theory +
                                    Marks.objects.filter(student=student,
                                                         subject=sub).first().internal_theory)
                    worksheet.write(i, 9, student.status)
                    i += 1
                    break

    workbook.close()


def back_students():
    branches = Branch.objects.all()
    workbook = xlsxwriter.Workbook('back.xlsx')
    bold = workbook.add_format()
    bold.set_bold()
    bold.set_align('center')

    for branch in branches:
        print branch
        worksheet = workbook.add_worksheet(branch.codename)
        worksheet.write(0, 0, branch.name)
        students = Student.objects.filter(college='027', branch=branch)
        students = [student for student in students if
                    student.status != 'INCOMP' and student.status != 'CP(0)']

        subjects = []
        for student in students:
            for mark in student.marks_set.all():
                subjects.append(mark.subject)
        subjects = set(subjects)

        k = 2
        for subject in subjects:
            worksheet.write(1, k, subject.code)
            k = k + 1
            worksheet.write(1, k, 'No. of Back')

        i = 2
        for student in students:
            worksheet.write(i, 0, student.name)
            worksheet.write(i, 1, student.roll_no)
            j = 2
            for subject in subjects:
                marks = student.marks_set.filter(subject=subject)
                if len(marks) == 0:
                    worksheet.write(i, j, 'N.A.')
                elif marks[0].back is True:
                    worksheet.write(i, j, 'F')
                else:
                    worksheet.write(i, j, '-')
                j = j + 1
            worksheet.write(i, j, student.status.split('(')[1].split(')')[0])

            i = i + 1
    workbook.close()


def faculty_new():
    college_code = '027'

    students = Student.objects.filter(
        college=College.objects.filter(code=college_code).first())
    branches_section_pair = set(
        [(student.branch, student.section) for student in students])

    subjects = set()
    for student in students:
        for mark in student.marks_set.all():
            subjects.add(mark.subject)

    workbook = xlsxwriter.Workbook('faculty_performance_new.xlsx')

    heading = workbook.add_format()
    heading.set_bold()
    heading.set_font_size(15)
    heading.set_align('center')
    heading.set_border(2)

    table_headers = workbook.add_format()
    table_headers.set_bold()
    table_headers.set_align('center')
    table_headers.set_border(2)

    table = workbook.add_format()
    table.set_align('center')
    table.set_border(2)

    print subjects
    worksheet = workbook.add_worksheet()
    i = 3
    worksheet.write(i - 1, 0, 'Subject', table_headers)
    worksheet.write(i - 1, 1, 'Pass %', table_headers)
    worksheet.write(i - 1, 2, 'Average %', table_headers)
    worksheet.write(i - 1, 3, 'External Average %', table_headers)
    worksheet.write(i - 1, 4, 'Section', table_headers)
    for subject in subjects:
        branch_count = 0
        worksheet.write(i, 0, subject.name, table_headers)
        i += 1
        for x in branches_section_pair:

            count = 0
            external = 0
            internal = 0
            clear = 0
            students = [student for student in
                        Student.objects.filter(college='027', branch=x[0],
                                               section=x[1]) if
                        student.status != 'INCOMP']

            for student in students:

                mark = student.marks_set.filter(subject=subject).first()

                if not mark:
                    pass
                else:
                    count += 1
                    external += mark.theory
                    internal += mark.internal_theory
                    if not mark.back:
                        clear += 1

            if count != 0:
                branch_count += 1
                print subject.code
                worksheet.write(i, 0, subject.code, table)
                worksheet.write(i, 1, round((float(clear) / count) * 100, 2),
                                table)
                try:
                    avg = round(((float(
                        internal + external) / count) / max_of_subject_total(
                        subject.code)) * 100, 2)
                except ZeroDivisionError:
                    avg = 0

                worksheet.write(i, 2, avg, table)
                try:
                    external_avg = round(((float(
                        external) / count) / max_of_subject_external(
                        subject.code)) * 100, 2)
                except ZeroDivisionError:
                    external_avg = 0
                worksheet.write(i, 3, external_avg, table)
                worksheet.write(i, 4, x[0].codename + '-' + str(x[1]), table)
                i += 1
        worksheet.merge_range(i - branch_count, 0, i - 1, 0, subject.code,
                              table)