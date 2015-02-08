__author__ = 'animesh'

from scraper.models import Student, Subject
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
        branch_dict = {'00': 'CE', '10': 'CSE', '13': 'IT','20': 'EE', '21': 'EN', '22': 'ICE', '30': 'ELE',
                       '31': 'ECE', '32': 'EIE', '35': 'AEI', '40': 'ME', '41': 'MT', '45': 'IPE', '51': 'CHE',
                       '54': 'BT'}
        if len(self.colleges) == 1 and len(self.branches) == 1 and len(self.semester) == 1:
            data = [['Subject Codes', 'Maximum Obtained', 'Average Marks', 'Minimum Obtained'], ]
            results = ExcelGenerator.result_dict(self.colleges[0], self.branches[0], self.semester[0])
            if not results:
                return data
            data_list = [[str(sub_code), 0, 0, 300] for sub_code in results[1]]
            num_students = 0
            maximum_marks = []
            for i in range(len(results[0])):
                sub_code_keys = results[0][i]["marks"].keys()
                if sub_code_keys == results[1]:
                    num_students += 1
                    if not maximum_marks:
                        for r in range(len(sub_code_keys)):
                            maximum_marks.append(GraphGenerator.max_of_subject(results[0][i]['marks'].values()[r][-1]))
                    for j in range(len(sub_code_keys)):
                        sub_marks = sum(results[0][i]['marks'][sub_code_keys[j]][1: -1])
                        data_list[j][2] += sub_marks
                        if data_list[j][1] < sub_marks:
                            data_list[j][1] = int(sub_marks)
                        if data_list[j][3] > sub_marks:
                            data_list[j][3] = int(sub_marks)

            for k in range(len(results[1])):
                data_list[k][2] = int(data_list[k][2] / float(num_students))
                data_list[k][1] = int(data_list[k][1] / float(maximum_marks[k]) * 100)
                data_list[k][2] = int(data_list[k][2] / float(maximum_marks[k]) * 100)
                data_list[k][3] = int(data_list[k][3] / float(maximum_marks[k]) * 100)
            # print data + data_list[:2]
            return data + data_list
        elif len(self.colleges) == 1 and len(self.branches) == 1 and len(self.semester) == 8:
            data = [['Semester', 'Maximum Marks', 'Average Marks', 'Minimum Marks']]
            for sem in self.semester:
                sem_max = 0
                sem_min = 300
                sem_avg = 0
                results = ExcelGenerator.result_dict(self.colleges[0], self.branches[0], sem)
                if not results:
                    return data
                total_marks = sum([GraphGenerator.max_of_subject(r[-1]) for r
                                   in results[0][0]['marks'].values()])
                for result in results[0]:
                    student_total = sum([sum(result['marks'][key][1: -1]) for
                                         key in result['marks']])
                    sem_avg += student_total
                    if sem_min > student_total:
                        sem_min = student_total
                    if sem_max < student_total:
                        sem_max = student_total
                sem_avg /= len(results[0])
                sem_avg_p = int((sem_avg / float(total_marks)) * 100)
                sem_min_p = int((sem_min / float(total_marks)) * 100)
                sem_max_p = int((sem_max / float(total_marks)) * 100)
                data.append([sem, sem_max_p, sem_avg_p, sem_min_p])
                # print sem, sem_max, sem_min, sem_avg, sem_all_max
            return data
        elif len(self.colleges) == 1 and len(self.branches) != 1 and len(self.semester) == 1:
            data = [['Branches', 'Maximum', 'Average', 'Minimum'], ]
            for branch in self.branches:
                results = ExcelGenerator.result_dict(self.colleges[0], branch, self.semester[0])
                if not results:
                    continue
                branch_marks = [branch_dict[branch.code], 0, 0, 3000]
                total_marks = sum([GraphGenerator.max_of_subject(r[-1]) for r in results[0][0]['marks'].values()])
                student_count = 0
                for result in results[0]:
                    if result['marks'].keys() == results[1]:
                        student_count += 1
                        student_total = sum([sum(result['marks'][key][1: -1]) for key in result['marks']])
                        branch_marks[2] += student_total
                        if branch_marks[1] < student_total:
                            branch_marks[1] = student_total
                        if branch_marks[3] > student_total:
                            branch_marks[3] = student_total
                branch_marks[2] = int(branch_marks[2] / float(student_count * total_marks) * 100)
                branch_marks[1] = int(branch_marks[1] / float(total_marks) * 100)
                branch_marks[3] = int(branch_marks[3] / float(total_marks) * 100)
                data.append(branch_marks)
            return data
        elif len(self.colleges) == 1 and len(self.branches) != 1 and len(self.semester) != 1:
            branch_list = [branch_dict[br.code] for br in self.branches]
            data = [['Semesters', ], ]
            existing_branches = []
            for sem in self.semester:
                sem_list = [str(sem), ]
                branch_iter = 0
                print sem_list
                for i in range(len(branch_list)):
                    results = ExcelGenerator.result_dict(self.colleges[0], self.branches[i], sem)
                    if not results and branch_list[i] in existing_branches:
                        sem_list.append(0)
                        branch_iter += 1
                        continue
                    elif not results:
                        continue
                    else:
                        if branch_list[i] not in existing_branches:
                            existing_branches.append(branch_list[i])
                        sem_list.append(0)
                        if branch_list[i] not in data[0]:
                            data[0].append(branch_list[i])
                    total_marks = sum([GraphGenerator.max_of_subject(r[-1]) for r in results[0][0]['marks'].values()])
                    student_count = 0
                    for result in results[0]:
                        if result['marks'].keys() == results[1]:
                            student_count += 1
                            student_total = sum([sum(result['marks'][key][1: -1]) for key in result['marks']])
                            sem_list[branch_iter + 1] += student_total
                    sem_list[branch_iter + 1] = int(sem_list[branch_iter + 1] / float(total_marks * student_count) * 100)
                    branch_iter += 1
                data.append(sem_list)
                print sem_list
            return data

    @staticmethod
    def max_of_subject(code):
        subject = Subject.objects.filter(code=code).first()
        n = max([marks.theory + marks.practical + marks.internal_practical + marks.internal_theory
                    for marks in subject.marks_set.all()])
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
