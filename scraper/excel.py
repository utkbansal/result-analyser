from .models import Student, College, Branch
import xlsxwriter


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
        workbook = xlsxwriter.Workbook('test.xlsx')
        # now write data of each combination in
        # a separate worksheet of the above workbook
        [ExcelGenerator.writer(self, workbook, college, branch, semester)
         for college in self.colleges for branch in self.branches
         for semester in self.semester]

        workbook.close()

    def writer(self, workbook, college, branch, semester):
        """
        creates and saves an excel file containing
        marks of each student of given college, branch
        and semester if that branch exists in the
        college and returns False otherwise

        """
        results = ExcelGenerator.result_dict(self, college, branch, semester)
        # If result cannot be generated for the give combination
        if not results:
            return False

        # Add a new worksheet to the workbook with appropriate name
        worksheet = workbook.add_worksheet(college.code + '_' + branch.code + '_' + str(semester) + 'semester')

        # Creating format properties

        worksheet.set_column(0, 0, 12)
        worksheet.set_column(1, 2, 25)

        i = 2

        # TEST : making the list of possible correct subjects
        # bring in the subjects of first 5 students and compare them,
        # the list which has max identical lists is the correct list of subjects

        subject_code_megalist = [results[y]['marks'].keys() for y in range(5)]

        for k in range(len(subject_code_megalist)):
            for j in range(len(subject_code_megalist[k])):
                if subject_code_megalist[k][j][1:4] == 'OE0':
                    subject_code_megalist[k][j] = 'Open Elective'

        check_list = [0 for k in range(5)]

        for m in range(3):
            count = 0
            current_list = subject_code_megalist[m]

            for n in range(3):
                if current_list == subject_code_megalist[n]:
                    count += 1
            check_list[m] = count

        subject_codes = subject_code_megalist[check_list.index(max(check_list))]

        # Set Heading
        worksheet.merge_range(0, 0, 0, 10, college.name+' '+branch.name+' '+' '+str(semester)+' '+'semester')

        for j in range(len(subject_codes)):
            worksheet.merge_range(1, j * 3 + 3, 1, (j + 1) * 3 + 2, subject_codes[j])

        worksheet.write(1, 0, 'Roll No')
        worksheet.write(1, 1, 'Name')
        worksheet.write(1, 2, 'Fathers Name')

        for c in range(3, 3 * len(subject_codes) + 3):
            if c % 3 == 0:
                worksheet.write(2, c, 'External')
            elif c % 3 == 1:
                worksheet.write(2, c, 'Internal')
            else:
                worksheet.write(2, c, 'Total')

        for result in results:

            keys = result['marks'].keys()
            if keys == subject_codes:
                for k in range(0, 3 * len(keys), 3):
                    worksheet.write(i+1, k + 3, result['marks'][keys[k / 3]][1] + result['marks'][keys[k / 3]][2])
                    worksheet.write(i+1, k + 4, result['marks'][keys[k / 3]][3] + result['marks'][keys[k / 3]][4])
                    worksheet.write(i+1, k + 5, result['marks'][keys[k / 3]][1] + result['marks'][keys[k / 3]][2]
                                    + result['marks'][keys[k / 3]][3] + result['marks'][keys[k / 3]][4])

                worksheet.write(i+1, 0, result['roll_no'])
                worksheet.write(i+1, 1, result['name'])
                worksheet.write(i+1, 2, result['fathers_name'])
            else:
                i -= 1
            i += 1

    def result_dict(self, college, branch, semester):
        """
        makes a dictionary of result data of each student
        of given college_code and branch_code
        and appends it to a list and returns that list
        returns: a list of dictionaries containing
        data of each student
        """

        # list of dictionaries
        ls = []
        required_students = Student.objects.filter(college=college.code, branch=branch.code).all()

        for student in required_students:
            student_dict = {}
            for mrks in student.marks_set.all():
                if mrks.semester == semester:
                    if not student_dict:
                        student_dict['marks'] = {}
                    student_dict['marks'][mrks.subject.code] = [mrks.subject.name, mrks.theory, mrks.practical,
                                                                mrks.internal_theory, mrks.internal_practical]
            if student_dict:
                student_dict['name'] = student.name
                student_dict['fathers_name'] = student.fathers_name
                student_dict['roll_no'] = student.roll_no
                ls.append(student_dict)
        return ls
