__author__ = 'animesh'

from scraper.models import Student, Subject, College, Branch, Marks
from excel import ExcelGenerator


class GraphGenerator(ExcelGenerator):
    """
    Objects of this class are initialized with data of the form submitted
    by the user for analysis and this class implements some methods to
    plot graphs of that data using Google Application Programming Interface
    """
    def __init__(self, college_codes, branch_codes, semester):
        """



        :type branch_codes: list containing branch codes
         of branches selected by user
        :type college_codes: list containing college codes
        of colleges selected by user
        :type semester: integer lies between 0 and 8
        """
        ExcelGenerator.__init__(self, college_codes, branch_codes, semester)

    def graph_selector(self):
        if len(self.colleges) == 1 and len(self.branches) == 1 and len(self.semester) == 1:
            students = Student.objects.filter(college = self.colleges[0], branch = self.branches).all()
            results = self.result_dict(self.colleges[0], self.branches[0], self.semester[0])
            data = [['Subject Codes', 'Maximum Obtained', 'Average Marks', 'Minimum Obtained'], ]
            data_list = [[str(sub_code), 0, 0, 300] for sub_code in results[1]]
            num_students = 0
            max_marks = []
            for i in range(len(results[0])):
                sub_code_keys = results[0][i]["marks"].keys()
                #print 'Subject code keys: ', sub_code_keys
                #print 'Results subjects: ', [results[1][j] for j in range(len(sub_code_keys))]
                if sub_code_keys == [results[1][j] for j in range(len(sub_code_keys))]:
                    num_students += 1
                    if not max_marks:
                        for sub_code in sub_code_keys:
                            max_marks.append(self.max_of_subject(sub_code))
                        print("Maximum Marks: {0}".format(max_marks))
                    for j in range(len(sub_code_keys)):
                        sub_marks = sum(results[0][i]['marks'][sub_code_keys[j]][1:])
                        data_list[j][2] += sub_marks
                        if data_list[j][1] < sub_marks:
                            data_list[j][1] = int(sub_marks)
                        if data_list[j][3] > sub_marks:
                            data_list[j][3] = int(sub_marks)

            for k in range(len(results[1])):
                data_list[k][2] = int(data_list[k][2] / float(num_students))
                data_list[k][1] = int(data_list[k][1] / float(max_marks[k]) * 100)
                data_list[k][2] = int(data_list[k][2] / float(max_marks[k]) * 100)
                data_list[k][3] = int(data_list[k][3] / float(max_marks[k]) * 100)
            #print data + data_list[:2]
            return data + data_list


    def max_of_subject(self, code):
        subject = Subject.objects.filter(code = code).first()
        return max([marks.theory + marks.practical + marks.internal_practical + marks.internal_theory
        for marks in subject.marks_set.all()])


    def max_marks(self, n):
        n = int(n)
        if n in range(51):
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
        else:
            return 300