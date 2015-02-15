__author__ = 'animesh'
from scraper.models import Student,  College, Branch, AverageMarks


class AverageGenerator(object):
    """
    Takes college, branch and semester as parameters and
    has methods for calculating average, lowest and highest marks
    of particular college, branch and semester
    """
    def __init__(self, college, branch, semester):
        """
        saves average, maximum and minimum marks in database of
        given college branch and semester
        :param college: college object of college of which marks are to be saved
        :param branch: branch object of the branch of which marks are to be saved
        :param semester: an integer of which marks are to be saved
        :return: None
        """
        self.college = college
        self.branch = branch
        self.semester = semester

    def feed_marks(self):
        """
        feeds the marks of college, branch and semester of the AverageGenerator object
        :return: True if successfully saves the marks of given college, branch and semester,
        False otherwise
        """
        # getting all students of given college and branch
        students = Student.objects.filter(college=self.college.code, branch=self.branch.code).all()
        average_marks = 0
        maximum_marks = 0
        minimum_marks = 5000
        required_students = []
        # This loop filters students of required semester by comparing semester of marks of amy one subject
        for student in students:
            student_marks = student.marks_set.all()
            for subject_marks in student_marks:
                if subject_marks.semester == self.semester:
                    required_students.append(student)
                    break
        if required_students:
            if len(required_students) >= 5:
                students_for_marks = required_students[: 5]  # list of students to get general subject codes
            else:
                students_for_marks = required_students
            subject_codes_list = []
            # for creating general list of subject codes with open electives replaced with 'OE0'
            for student in students_for_marks:
                subject_codes = [sub_marks.subject.code for sub_marks in student.marks_set.all() if
                                 sub_marks.semester == self.semester]
                for i in range(len(subject_codes)):
                    if subject_codes[i][1: 4] == 'OE0':
                        subject_codes[i] = 'OE0'
                subject_codes_list.append(subject_codes)
            pos = [0 for i in range(len(students_for_marks))]
            for i in range(len(subject_codes_list)):
                for j in range(len(subject_codes_list)):
                    if subject_codes_list[i] == subject_codes_list[j]:
                        pos[i] += 1
            real_subject_codes = subject_codes_list[pos.index(max(pos))]  # stores correct subject codes(most probably)
            total = 1000.0
            student_count = 0 # counts number of students of which we will be taking average
            for student in required_students:
                subjects_marks = [sub_marks for sub_marks in student.marks_set.all() if
                                  sub_marks.semester == self.semester]
                sub_codes = [sub.subject.code for sub in subjects_marks]
                for i in range(len(sub_codes)):
                    if sub_codes[i][1: 4] == 'OE0':
                        sub_codes[i] = 'OE0'
                if sub_codes == real_subject_codes:  # checking if subject codes of the particular student matches with
                    student_count += 1               # correct subject codes, if yes then incrementing student_count
                    student_total = 0  # stores total marks of a student
                    for subject_marks in subjects_marks:
                        subject_total = AverageGenerator.total_marks(subject_marks)
                        student_total += subject_total  # adding marks of each subject
                    average_marks += student_total
                    if maximum_marks < student_total:
                        maximum_marks = student_total
                    if minimum_marks > student_total:
                        minimum_marks = student_total
            average_marks /= float(student_count)
            average_marks = int((average_marks / total) * 100)
            maximum_marks = int((maximum_marks / total) * 100)
            minimum_marks = int((minimum_marks / total) * 100)
            new_marks = AverageMarks(college=self.college, branch=self.branch, semester=self.semester,
                                     average=average_marks, maximum=maximum_marks, minimum=minimum_marks)
            new_marks.save()
            return True
        return False

    @staticmethod
    def total_marks(subject_marks):
        """
        :subject_marks: marks object
        :return: total marks corresponding to the marks object
        """
        return subject_marks.theory + subject_marks.practical + subject_marks.internal_theory + \
            subject_marks.internal_practical


def update():
    """
    updates AverageMarks table with average marks of each college branch and semester
    :return: None
    """
    # list of college codes of collegs of which the data is available
    college_codes = [clg['college'] for clg in Student.objects.values('college').distinct().all()]
    all_colleges = []  # list of existing college objects
    for college_code in college_codes:
        college = College.objects.filter(code=college_code).first()
        all_colleges.append(college)
    all_branches = Branch.objects.all()
    # updates marks of each semester of each branch of each college
    for college in all_colleges:
        for branch in all_branches:
            for sem in range(1, 9):
                ob = AverageGenerator(college, branch, sem)
                ob.feed_marks()