from django.conf.urls import patterns,  url
from .views import AnalysisFormView

urlpatterns = patterns(
    '',
    url(r'^analyze/$', AnalysisFormView.as_view(), name='analyze'),
)
