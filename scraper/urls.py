from django.conf.urls import patterns,  url
from .views import AnalysisFormView, AnalysisView,LoginView

urlpatterns = patterns(
    '',
    url(r'^analyze/$', AnalysisFormView.as_view(), name='analyze'),
    url(r'^analysis/$', AnalysisView.as_view(), name='analysis'),
    url(r'^$', LoginView.as_view(), name='login'),
)
