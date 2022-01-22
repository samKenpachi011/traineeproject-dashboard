from django.conf import settings
from django.urls.conf import path, include
from edc_dashboard import UrlConfig
from edc_appointment.admin_site import edc_appointment_admin

from .patterns import screening_identifier, subject_identifier
from .views import SubjectListboardView, SubjectDashboardView
from .views import SubjectScreeningListboardView

# To update urls
app_name = 'traineeproject_dashboard'

subject_listboard_url_config = UrlConfig(
    url_name='subject_listboard_url',
    view_class=SubjectListboardView,
    label='subject_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

screening_listboard_url_config = UrlConfig(
    url_name='screening_listboard_url',
    view_class=SubjectScreeningListboardView,
    label='screening_listboard',
    identifier_label='screening_identifier',
    identifier_pattern=screening_identifier)

subject_dashboard_url_config = UrlConfig(
    url_name='subject_dashboard_url',
    view_class=SubjectDashboardView,
    label='subject_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

urlpatterns = []
urlpatterns += subject_listboard_url_config.listboard_urls
urlpatterns += screening_listboard_url_config.listboard_urls
urlpatterns += subject_dashboard_url_config.dashboard_urls

if settings.APP_NAME == 'traineeproject_dashboard':

    from django.views.generic.base import RedirectView

    urlpatterns += [
        path('edc_device/', include('edc_device.urls')),
        path('edc_protocol/', include('edc_protocol.urls')),
        path('admin/', edc_appointment_admin.urls),
        path('admininistration/', RedirectView.as_view(url='admin/'),
             name='administration_url'),
        path('accounts/', include('edc_base.auth.urls')),
        path('admin/', include('edc_base.auth.urls')),
        path('edc_lab/', include('edc_lab.urls')),
        path('edc_lab_dashboard/', include('edc_lab_dashboard.urls')),
        path(r'', RedirectView.as_view(url='admin/'), name='home_url')] 
urlpatterns = [

]
