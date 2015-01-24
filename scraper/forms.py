from django import forms
from .models import College, Branch
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class AnalysisForm(forms.Form):

    college_options = tuple([(college.code, college.name) for college in College.objects.all()])
    branch_options = tuple([(branch.code, branch.name,) for branch in Branch.objects.all()])

    college_code = forms.MultipleChoiceField(label='Colleges',
                                             widget=forms.SelectMultiple,
                                             choices=college_options)

    branch_code = forms.MultipleChoiceField(label='Branches',
                                            widget=forms.SelectMultiple,
                                            choices=branch_options)

    semester = forms.ChoiceField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)],
                                 label='Semester')

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
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