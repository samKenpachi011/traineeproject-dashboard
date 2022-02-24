from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .contact_information_model_wrapper import ContactInformationModelWrapper


class ContactInformationModelWrapperMixin:
    
    contact_information_model_wrapper_cls = ContactInformationModelWrapper
    
    @property
    def contact_information_cls(self):
        return django_apps.get_model(self.contact_information_model_wrapper_cls.model)
    
    @property
    def contact_information(self):
        # return the wrapped saved or unsaved personal contact information
        model_obj = self.contact_information_model_obj or self.contact_information_cls(
            **self.contact_information_options)
        return self.contact_information_model_wrapper_cls(model_obj=model_obj)
    
    @property
    def contact_information_model_obj(self):
        # return a model instance or none
        try:
            return self.contact_information_cls.objects.get(
                **self.contact_information_options)
        except ObjectDoesNotExist:
            return None   

    @property
    def create_contact_information_options(self):
        # returning a dictionary of options to create a new unpersisted personal contact information model instance
        options =  dict(subejct_identifier = self.subject_identifier)

        return options
    
    @property
    def contact_information_options(self):
        # returning a dictionary of options to get an existing instance
        options =  dict(subejct_identifier = self.subject_identifier)

        return options
    
    