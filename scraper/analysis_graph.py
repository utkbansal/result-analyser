__author__ = 'animesh'

from scraper.models import Subject, AverageMarks
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
        """
        Selects which graph to plot on the basis of fields selected and returns data in
        the form such that google charts can plot graph
        :return: a list containing data which is to be passed to google charts
        """
        # this dictionary maps branch codes to their abbreviations
        branch_dict = {'00': 'CE', '10': 'CSE', '13': 'IT', '20': 'EE', '21': 'EN', '22': 'ICE', '30': 'ELE',
                       '31': 'ECE', '32': 'EIE', '35': 'AEI', '40': 'ME', '41': 'MT', '45': 'IPE', '51': 'CHE',
                       '54': 'BT'}
        # this dictionary maps college codes to their abbreviations
        college_dict = {'027': 'AKGEC', '029': 'KIET', '032': 'ABES', '033': 'RKGIT', '054': 'BBDNITM',
                        '063': 'GLAITM', '068': 'MIET', '077': 'KNMIET', '091': 'JSSATE', '097': 'GALGOTIAS',
                        '110': 'IERT', '122': 'RAMSWAROOP', '128': 'BHARAT', '143': 'IMS', '161': 'KEC',
                        '164': 'PSIT', '193': 'UNITED', '520': 'INDRAPRASTHA'}
        # this if plots marks for subjects of one college, one branch and one semester
        if len(self.colleges) == 1 and len(self.branches) == 1 and len(self.semester) == 1:
            # the nested list to be returned
            data = [['Subject Codes', 'Maximum Obtained', 'Average Marks', 'Minimum Obtained'], ]
            # getting results in list of dictionary form by calling result_dict method
            results = ExcelGenerator.result_dict(self.colleges[0], self.branches[0], self.semester[0])
            if not results:
                return data
            data_list = [[str(sub_code), 0, 0, 300] for sub_code in results[1]]
            num_students = 0
            maximum_marks = []  # stores maximum marks of each subject
            for i in range(len(results[0])):
                sub_code_keys = results[0][i]["marks"].keys()
                if sub_code_keys == results[1]:  # checking if student is normal or not
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
            return data + data_list

        # this if plots average, max and min marks of each semester for selected college and branch
        elif len(self.colleges) == 1 and len(self.branches) == 1 and len(self.semester) != 1:
            # nested list to be returned
            message = "Analysis of " + self.colleges[0].name + " - " + self.branches[0].name
            data = [['Semesters', 'Maximum Marks', 'Average Marks', 'Minimum Marks']]
            for sem in self.semester:
                # querying marks of each semester
                sem_marks = AverageMarks.objects.filter(college=self.colleges[0],
                                                        branch=self.branches[0], semester=sem).first()
                if sem_marks:
                    data.append([str(sem), int(sem_marks.maximum), int(sem_marks.average), int(sem_marks.minimum)])
                else:
                    data.append([str(sem), 0, 0, 0])
            return data

        # this if plots average, max, min marks of each branch of selected college and semester
        elif len(self.colleges) == 1 and len(self.branches) != 1 and len(self.semester) == 1:
            # nested list to be returned
            data = [['Branches', 'Maximum', 'Average', 'Minimum'], ]
            for branch in self.branches:
                # querying marks of each branch
                br_marks = AverageMarks.objects.filter(college=self.colleges[0], branch=branch,
                                                       semester=self.semester[0]).first()
                if br_marks:
                    data.append([branch_dict[branch.code], int(br_marks.maximum),
                                 int(br_marks.average), int(br_marks.minimum)])
            return data

        # plots average marks of each branch for each semester of the selected college
        elif len(self.colleges) == 1 and len(self.branches) != 1 and len(self.semester) != 1:
            # nested list to be returned
            data = [['Semesters', ], ]
            # lists contains branches which exist for selected college
            existing_branches = []
            # the next two loops for adding existing branches to the list
            for sem in self.semester:
                for branch in self.branches:
                    sem_marks = AverageMarks.objects.filter(college=self.colleges[0],
                                                            branch=branch, semester=sem).first()
                    if sem_marks:
                        if branch not in existing_branches:
                            existing_branches.append(branch)
                            data[0].append(branch_dict[branch.code])
            for sem in self.semester:
                sem_list = [str(sem), ]  # individual list to be appended to the nested list
                for branch in existing_branches:
                    sem_marks = AverageMarks.objects.filter(college=self.colleges[0],
                                                            branch=branch, semester=sem).first()
                    if sem_marks:
                        sem_list.append(int(sem_marks.average))
                    else:
                        sem_list.append(0)  # adding zero if marks doesn't exit for that semester
                data.append(sem_list)
            return data

        # plots marks of selected colleges for given branch and semester
        elif len(self.colleges) != 1 and len(self.branches) == 1 and len(self.semester) == 1:
            # nested list to be returned
            data = [['Colleges', 'Maximum', 'Average', 'Minimum'], ]
            for college in self.colleges:
                college_marks = AverageMarks.objects.filter(college=college, branch=self.branches[0],
                                                            semester=self.semester[0]).first()
                if college_marks:
                    data.append([college_dict[college.code], int(college_marks.maximum), int(college_marks.average),
                                 int(college_marks.minimum)])
            return data

        elif len(self.colleges) != 1 and len(self.branches) == 1 and len(self.semester) != 1:
            data = [['Semesters', ], ]
            existing_colleges = []
            for sem in self.semester:
                for college in self.colleges:
                    college_marks = AverageMarks.objects.filter(college=college, branch=self.branches[0],
                                                                semester=sem).first()
                    if college_marks:
                        if college not in existing_colleges:
                            existing_colleges.append(college)
                            data[0].append(college_dict[college.code])
            for sem in self.semester:
                sem_list = [str(sem), ]
                for i in range(len(existing_colleges)):
                    college_marks = AverageMarks.objects.filter(college=existing_colleges[i], branch=self.branches[0],
                                                                semester=sem).first()
                    if college_marks:
                        sem_list.append(int(college_marks.average))
                    else:
                        sem_list.append(0)
                data.append(sem_list)
            return data

        elif len(self.colleges) != 1 and len(self.branches) != 1 and len(self.semester) == 1:
            data = [['Branches', ], ]
            common_branches = []
            for branch in self.branches:
                flag = 1
                for college in self.colleges:
                    college_marks = AverageMarks.objects.filter(college=college, branch=branch,
                                                                semester=self.semester[0]).first()
                    if not college_marks:
                        flag = 0
                if flag == 1:
                    common_branches.append(branch)
            if common_branches:
                for branch in common_branches:
                    branch_list = [branch_dict[branch.code], ]
                    for college in self.colleges:
                        college_marks = AverageMarks.objects.filter(college=college, branch=branch,
                                                                    semester=self.semester[0]).first()
                        if college_marks:
                            if college_dict[college.code] not in data[0]:
                                data[0].append(college_dict[college.code])
                            branch_list.append(int(college_marks.average))
                    data.append(branch_list)
                return data
            common_colleges = []
            for college in self.colleges:
                flag = 1
                for branch in self.branches:
                    branch_marks = AverageMarks.objects.filter(college=college, branch=branch,
                                                               semester=self.semester[0])
                    if not branch_marks:
                        flag = 0
                if flag == 1:
                    common_colleges.append(college)
            if common_colleges:
                for branch in self.branches:
                    branch_list = [branch_dict[branch.code], ]
                    for college in common_colleges:
                        college_marks = AverageMarks.objects.filter(college=college, branch=branch,
                                                                    semester=self.semester[0]).first()
                        if college_marks:
                            if college_dict[college.code] not in data[0]:
                                data[0].append(college_dict[college.code])
                            branch_list.append(int(college_marks.average))
                    data.append(branch_list)
                return data
            return [[], ]

        elif len(self.colleges) != 0 and len(self.branches) != 1 and len(self.semester) != 1:
            data = [['Semesters', ]]
            for sem in self.semester:
                sem_list = [str(sem), ]
                common_branches = []
                for branch in self.branches:
                    flag = 1
                    for college in self.colleges:
                        college_marks = AverageMarks.objects.filter(college=college, branch=branch,
                                                                    semester=sem).first()
                        if not college_marks:
                            flag = 0
                    if flag == 1:
                        common_branches.append(branch)
                if common_branches:
                    common_colleges = self.colleges
                else:
                    common_branches = self.branches
                    common_colleges = []
                    for college in self.colleges:
                        flag = 1
                        for branch in common_branches:
                            branch_marks = AverageMarks(college=college, branch=branch,
                                                        semster=sem).first()
                            if not branch_marks:
                                flag = 0
                        if flag == 1:
                            common_colleges.append(college)
                for college in common_colleges:
                    if college_dict[college.code] not in data[0]:
                        data[0].append(college_dict[college.code])
                    college_marks = 0
                    for branch in common_branches:
                        branch_marks = AverageMarks.objects.filter(college=college, branch=branch,
                                                                   semester=sem).first()
                        college_marks += branch_marks.average
                    college_marks = int(college_marks / float(len(common_branches)))
                    sem_list.append(college_marks)
                data.append(sem_list)
            if len(data[0]) != 1:
                for data_list in data:
                    print data_list
                return data
            else:
                return [[], ]

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

    @staticmethod
    def find_total_max(student_list):
        if len(student_list) >= 5:
            student_list = student_list[: 5]
        totals = [sum([GraphGenerator.max_of_subject(student['marks'][key][-1]) for
                       key in student['marks']]) for student in student_list]
        total_freq = [0 for i in range(len(student_list))]
        for i in range(len(totals)):
            curr = totals[i]
            for j in range(len(totals)):
                if curr >= totals[j]:
                    total_freq[i] += 1
        return totals[total_freq.index(max(total_freq))]