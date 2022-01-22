
from django.apps import apps as django_apps
from django.conf import settings
from edc_base.view_mixins import EdcBaseViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin
from edc_navbar import NavbarViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView

class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView):
    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    consent_model = 'traineeproject_subject.subjectconsent'
    navbar_name = 'traineeproject_dashboard'