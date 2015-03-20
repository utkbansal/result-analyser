from django.conf.urls import patterns,  url
from .views import (
    AnalyserFormView,
    LoginView,
    LogOutView,
    PasswordChangeView,
    AnalysisView
)

urlpatterns = patterns(
    '',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^analyze/$', AnalyserFormView.as_view(), name='analyze'),
    url(r'^analysis/$', AnalysisView.as_view(), name='analysis'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^reset/$', PasswordChangeView.as_view(), name='reset'),
)
