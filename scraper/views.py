from .forms import AnalysisForm
from django.views import generic
from .excel import create_excel
from django.http import HttpResponseRedirect


class AnalysisFormView(generic.FormView):
    form_class = AnalysisForm
    template_name = 'analyze.html'
    success_url = ''

    def form_valid(self, form):
        college_code = form.cleaned_data['college_code']
        branch_code = form.cleaned_data['branch_code']
        sem = form.cleaned_data['semester']

        create_excel(college_code[0], branch_code[0], sem)

        return HttpResponseRedirect(self.get_success_url())