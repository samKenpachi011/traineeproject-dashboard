from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper
from edc_consent import ConsentModelWrapperMixin
from edc_base.utils import get_uuid

from .subject_consent_model_wrapper import SubjectConsentModelWrapper
from .screening_model_wrapper_mixin import ScreeningModelWrapperMixin

class SubjectScreeningModelWrapper(ScreeningModelWrapperMixin,ConsentModelWrapperMixin, ModelWrapper):


    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'traineeproject_subject.screeningeligibility'
    next_url_attrs = ['screening_identifier', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
 
    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def subject_identifier(self):
        if self.consent_model_obj:
            return self.consent_model_obj.subject_identifier
        return None

    @property
    def consent_model_obj(self):
        """Returns a consent model instance or None.
        """
        consent_model_cls = django_apps.get_model(self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(
            screening_identifier=self.screening_identifier,
            consent_identifier=get_uuid(),
            version=self.consent_version)
        return options

    @property
    def consent_options(self):
        """Returns a dictionary of options to get an existing
        consent model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            version=self.consent_version)
        return options

    @property
    def consent_version(self):
        return '1'
