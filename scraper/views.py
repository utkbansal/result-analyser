import os

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render

from .excel import create_excel
from .forms import AnalysisForm
from result_analyzer.settings import BASE_DIR


class AnalysisView(generic.TemplateView):
    template_name = 'analysis.html'


class AnalysisFormView(generic.FormView):
    form_class = AnalysisForm
    template_name = 'analyze.html'
    success_url = reverse_lazy('analysis')

    def form_valid(self, form):
        college_code = form.cleaned_data['college_code']
        branch_code = form.cleaned_data['branch_code']
        sem = form.cleaned_data['semester']

        # get_form_kwargs() returns all the data from the form which includes
        # which button was pressed (analyze/download)

        data = self.get_form_kwargs()['data'].keys()

        if 'download' in data:

            # Downloading logic here

            create_excel(college_code[0], branch_code[0], int(sem))
            excel = open(os.path.join(BASE_DIR, 'test.xlsx'), 'rb')
            data = excel.read()

            response = HttpResponse(data,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="test.xls"'
            return response

        else:
            # Redirect to analysis

            return render(self.request, 'analysis.html')

    def create_analysis_data(self):
        pass