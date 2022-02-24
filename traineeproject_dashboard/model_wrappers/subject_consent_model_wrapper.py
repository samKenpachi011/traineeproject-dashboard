from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .contact_information_mixin import ContactInformationModelWrapperMixin
class SubjectConsentModelWrapper(ContactInformationModelWrapperMixin, ModelWrapper):

    model = 'traineeproject_subject.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier','gender', 'first_name', 'initials', 'modified']