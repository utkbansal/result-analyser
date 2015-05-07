from scraper.models import Student, College, Branch

import xlsxwriter

import StringIO


def work(student_tup):
    return ExcelGenerator.dict_generator(student_tup)


class ExcelGenerator():
    def __init__(self, college_codes, branch_codes, semester):

        # Get the list of all college objects
        # if no college is selected, then take all colleges,
        # whose results are present in db
        if len(college_codes) == 0:
            # Get all the colleges whose results we have in our db
            self.colleges = [College.objects.filter(code=college_code).first()
                             for college_code in [d.values()[0] for d in
                                                  Student.objects.values('college_id').distinct()]]
        else:
            self.colleges = [College.objects.filter(code=college_code).first()
                             for college_code in college_codes]

        # Get the list of all branch objects
        # if no branch is selected, then take all branches
        if len(branch_codes) == 0:
            self.branches = [branch for branch in Branch.objects.all()]
        else:
            self.branches = [Branch.objects.filter(code=branch_code).first() for branch_code in branch_codes]

        # Get the semester number
        # if no semester is selected, then take all semesters
        if semester == 0:
            self.semester = [i for i in range(1, 9)]
        else:
            self.semester = [semester]

    def excel_creator(self):
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # now write data of each combination in
        # a separate worksheet of the above workbook
        excel_list = [ExcelGenerator.writer(workbook, college, branch, semester)
                      for college in self.colleges for branch in self.branches
                      for semester in self.semester]
        print excel_list
        if not filter(None, excel_list):
            return "Combination doesn't exist"

        workbook.close()
        return output

    @staticmethod
    def writer(workbook, college, branch, semester):
        students = Student.objects.filter(college=college,
                                          branch=branch).all()

        students = [s for s in students if s.status !='INCOMP']
        subjects = set()
        filtered_students = set()

        for student in students:
            for mark in student.marks_set.all():
                if mark.semester == semester:
                    subjects.add(mark.subject)
                    filtered_students.add(student)

        subjects = list(subjects)
        worksheet = workbook.add_worksheet(college.code + '_' + branch.code + '_' + str(semester) + 'semester')
        worksheet.set_column(0, 0, 12)
        worksheet.set_column(1, 2, 25)

        # Adding styles

        # heading is the college name
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

        worksheet.merge_range(0, 0, 0, 10, college.name + ' ' +
                              branch.codename+' Semester '+str(semester),
                              table_headers)
        worksheet.write(1, 0, 'S.No.', table_headers)
        worksheet.write(1, 1, 'Roll. No.', table_headers)
        worksheet.write(1, 2, 'Name', table_headers)

        x = 0
        for subject in subjects:
            print subject.code
            worksheet.merge_range(1, x * 3 + 3, 1, (x + 1) * 3 + 2,
                                  subject.code, table_headers)
            worksheet.write(2, x * 3 + 3, 'Internal', table)
            worksheet.write(2, x * 3 + 4, 'External', table)
            worksheet.write(2, x * 3 + 5, 'Total', table)
            x += 1
        # adding heading for total of a student and back subjects
        worksheet.merge_range(1, x * 3 + 3, 1, (x + 1) * 3 + 1,
                              'Total', table_headers)
        worksheet.merge_range(1, (x + 1) * 3 + 2, 1, (x + 2) * 3,
                              'Carry Papers', table_headers)
        worksheet.write(2, x * 3 + 3, 'Obtained', table)
        worksheet.write(2, (x + 1) * 3 + 1, 'Max', table)
        worksheet.write(2, (x + 1) * 3 + 2, 'Carry Status', table)
        worksheet.write(2, (x + 2) * 3, 'Carry Subjects', table)
        i = 2
        n = 1
        for student in filtered_students:
            j = 3
            i += 1

            worksheet.write(i, 0, n, table)
            n += 1
            worksheet.write(i, 1, student.roll_no, table)
            worksheet.write(i, 2, student.name, table)
            for subject in subjects:
                mark = student.marks_set.filter(subject=subject).first()
                # print mark
                if mark:
                    worksheet.write(
                        i,
                        j,
                        mark.internal_theory,
                        table
                    )
                    worksheet.write(
                        i,
                        j+1,
                        mark.theory,
                        table
                    )
                    worksheet.write(
                        i,
                        j+2,
                        mark.theory + mark.internal_theory,
                        table
                    )
                    j += 3

                else:
                    worksheet.write(i, j, 'NA', table)
                    worksheet.write(i, j+1, 'NA', table)
                    worksheet.write(i, j+2, 'NA', table)
                    j += 3
            student_total = sum([s_mark.theory + s_mark.internal_theory +
                                 s_mark.practical + s_mark.internal_practical
                                 for s_mark in student.marks_set.all()])
            worksheet.write(i, j, student_total, table)
            worksheet.write(i, j + 1, 1000, table)
            worksheet.write(i, j + 2, student.status, table)
            back_marks = [s_mark.subject.code for s_mark in
                          student.marks_set.all() if s_mark.back]
            back_str = ', '.join(back_marks)
            if student.status != 'CP(0)':
                worksheet.write(i, j + 3, back_str, table)

        return True



























    # @staticmethod
    # def writer(workbook, college, branch, semester):
    #     """
    #     creates and saves an excel file containing
    #     marks of each student of given college, branch
    #     and semester if that branch exists in the
    #     college and returns False otherwise
    #
    #     """
    #     results = ExcelGenerator.result_dict(college, branch, semester)
    #     # If result cannot be generated for the give combination
    #     if not results:
    #         return False
    #     elif not results[0]:
    #         return False
    #
    #     # Add a new worksheet to the workbook with appropriate name
    #     worksheet = workbook.add_worksheet(college.code + '_' + branch.code + '_' + str(semester) + 'semester')
    #
    #     # Creating format properties
    #
    #     worksheet.set_column(0, 0, 12)
    #     worksheet.set_column(1, 2, 25)
    #
    #     # Adding styles
    #
    #     # heading is the college name
    #     heading = workbook.add_format()
    #     heading.set_bold()
    #     heading.set_font_size(15)
    #     heading.set_align('center')
    #
    #     table_headers = workbook.add_format()
    #     table_headers.set_bold()
    #     table_headers.set_align('center')
    #
    #     i = 2
    #     subject_codes = results[1]
    #     # Set Heading
    #     worksheet.merge_range(0, 0, 0, 10,
    #                           college.name + ' - ' + branch.name + ' - Semester: ' + str(semester),
    #                           heading)
    #
    #     # sub_codes is a list of subject codes with the subject code of open elective subjects
    #     # replaced with the string "Open Elective" so that
    #     # we can replace the code with the string in the excel heading
    #     sub_codes = []
    #
    #     for code in subject_codes:
    #         if code[1:4] == 'OE0':
    #             sub_codes.append('OE0')
    #         else:
    #             sub_codes.append(code)
    #
    #     for j in range(len(sub_codes)):
    #         worksheet.merge_range(1, j * 3 + 3, 1, (j + 1) * 3 + 2, sub_codes[j], table_headers)
    #
    #     worksheet.write(1, 0, 'Roll No', table_headers)
    #     worksheet.write(1, 1, 'Name', table_headers)
    #     worksheet.write(1, 2, 'Fathers Name', table_headers)
    #
    #     for c in range(3, 3 * len(subject_codes) + 3):
    #         if c % 3 == 0:
    #             worksheet.write(2, c, 'External', table_headers)
    #         elif c % 3 == 1:
    #             worksheet.write(2, c, 'Internal', table_headers)
    #         else:
    #             worksheet.write(2, c, 'Total', table_headers)
    #
    #     for result in results[0]:
    #
    #         keys = result['marks'].keys()
    #         if keys == subject_codes:
    #             for k in range(0, 3 * len(keys), 3):
    #                 worksheet.write(i + 1, k + 3, result['marks'][keys[k / 3]][1] + result['marks'][keys[k / 3]][2])
    #                 worksheet.write(i + 1, k + 4, result['marks'][keys[k / 3]][3] + result['marks'][keys[k / 3]][4])
    #                 worksheet.write(i + 1, k + 5, result['marks'][keys[k / 3]][1] + result['marks'][keys[k / 3]][2]
    #                                 + result['marks'][keys[k / 3]][3] + result['marks'][keys[k / 3]][4])
    #
    #             worksheet.write(i + 1, 0, result['roll_no'])
    #             worksheet.write(i + 1, 1, result['name'])
    #             worksheet.write(i + 1, 2, result['fathers_name'])
    #         else:
    #             i -= 1
    #         i += 1
    #     return True

    @staticmethod
    def result_dict(college, branch, semester):
        """
        makes a dictionary of result data of each student
        of given college_code and branch_code
        and appends it to a list and returns that list
        returns: a list of dictionaries containing
        data of each student
        """
        required_students = [(student, semester) for student in Student.objects.filter(
            college=college.code, branch=branch.code).all()]
        ls = []
        for student_tup in required_students:
            std_dict = work(student_tup)
            if std_dict:
                ls.append(std_dict)

        print 'Number of students in semester: ', len(ls)
        if len(ls) == 0:
            return False
        # TEST : making the list of possible correct subjects
        # bring in the subjects of first 5 students and compare them,
        # the list which has max identical lists is the correct list of subjects
        if len(ls) >= 5:
            subject_code_megalist = [ls[y]["marks"].keys() for y in range(5)]
        else:
            subject_code_megalist = [ls[y]["marks"].keys() for y in range(len(ls))]
        length_megalist = len(subject_code_megalist)
        check_list = [0 for k in range(length_megalist)]

        for m in range(length_megalist):
            count = 0
            current_list = subject_code_megalist[m]

            for n in range(length_megalist):
                if current_list == subject_code_megalist[n]:
                    count += 1
            check_list[m] = count

        subject_codes = subject_code_megalist[check_list.index(max(check_list))]

        return [ls, subject_codes]

    @staticmethod
    def dict_generator(student_tup):
        student = student_tup[0]
        semester = student_tup[1]
        student_dict = {}

        for mrks in student.marks_set.all():
            if mrks.semester == semester:
                if not student_dict:
                    student_dict["marks"] = {}
                if mrks.subject.code[1: 4] == 'OE0':
                    student_dict["marks"]['OE0'] = [mrks.subject.name, mrks.theory, mrks.practical,
                                                    mrks.internal_theory, mrks.internal_practical, mrks.subject.code
                                                    ]

                else:
                    student_dict["marks"][mrks.subject.code] = [mrks.subject.name, mrks.theory, mrks.practical,
                                                                mrks.internal_theory, mrks.internal_practical,
                                                                mrks.subject.code
                                                                ]

        # adding personal details to the dictionary
        if student_dict:
            student_dict["name"] = student.name
            student_dict["fathers_name"] = student.fathers_name
            student_dict["roll_no"] = student.roll_no

            # student_dict is the dictionary containing info about a student
            return student_dict

        else:
            return None


