from django.conf import settings
from edc_model_wrapper import ModelWrapper

class SubjectOffStudyModelWrapper(ModelWrapper):
    model = ''
    querystring_attrs = ''
    next_url_attrs = ''
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')