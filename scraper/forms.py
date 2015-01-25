from django import forms
from .models import College, Branch, Student
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class AnalysisForm(forms.Form):

    colleges = []
    college_codes = [college_dict['college_id'] for college_dict in Student.objects.values('college_id').distinct()]
    for college_code in college_codes:
        db_college = College.objects.filter(code=college_code).first()
        if db_college:
            colleges.append(db_college)
    college_options = tuple([(college.code, college.name) for college in colleges])
    branch_options = tuple([(branch.code, branch.name,) for branch in Branch.objects.all()])
    semester_options = tuple([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (0, '')])

    college_code = forms.MultipleChoiceField(label='Colleges',
                                             widget=forms.SelectMultiple,
                                             choices=college_options,
                                             required=False)

    branch_code = forms.MultipleChoiceField(label='Branches',
                                            widget=forms.SelectMultiple,
                                            choices=branch_options,
                                            required=False)

    semester = forms.ChoiceField(choices=semester_options,
                                 label='Semester',
                                 required=False,
                                 initial=0)

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs = {'onsubmit': 'return ValidateForm()', 'name': 'form'}
        self.helper.layout = Layout(
            'college_code',
            'branch_code',
            'semester',
            ButtonHolder(
                Submit('download', 'Download', css_class='btn-block ')
            ),
            ButtonHolder(
                Submit('analyze', 'Analyze', css_class='btn-block ')
            )
        )