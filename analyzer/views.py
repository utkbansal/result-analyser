from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from .excel import ExcelGenerator
from .analysis_graph import GraphGenerator
from .forms import AnalysisForm, LoginForm, PasswordResetForm

from braces import views


class AnalysisFormView(views.LoginRequiredMixin, generic.FormView):
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

        if 'download' in data:  # Checks if user has clicked on download or not

            # Downloading logic here
            obj = ExcelGenerator(college_code, branch_code, int(sem))
            output = obj.excel_creator()

            output.seek(0)
            response = HttpResponse(output.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="test.xlsx"'
            return response

        else:
            # Redirect to analysis
            obj = GraphGenerator(college_code, branch_code, int(sem))
            data = obj.graph_selector()
            return render(self.request, 'analysis.html', dictionary={'data': data})


class LoginView(views.AnonymousRequiredMixin, generic.FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = 'analyze/'

    authenticated_redirect_url = reverse_lazy('analyze')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(generic.RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)


class PasswordChangeView(views.LoginRequiredMixin, generic.FormView):
    login_url = reverse_lazy('login')
    form_class = PasswordResetForm
    template_name = 'password_reset.html'
    success_url = reverse_lazy('analyze')

    def form_valid(self, form):
        user = authenticate(username=self.request.user, password=form.cleaned_data['old_password'])
        if user is not None:
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return super(PasswordChangeView, self).form_valid(form)
        return self.form_invalid(form)