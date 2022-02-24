from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .screening_model_wrapper import SubjectScreeningModelWrapper

class SubjectScreeningModelWrapperMixin:
    
    screening_model_wrapper_cls = SubjectScreeningModelWrapper
    
    @property
    def screening_model_obj(self):
        try:
            return self.screening_cls.objects.get(
                **self.screening_options)
        except ObjectDoesNotExist:
            return None   
        
    @property
    def screening(self):
        model_obj = self.screening_model_obj or self.screening_cls(
            **self.create_screening_cls_options)
        return SubjectScreeningModelWrapper(model_obj=model_obj)
        
    @property
    def screening_cls(self):
        return django_apps.get_model(self.screening_model_wrapper_cls.model)
    
            
    @property
    def create_screening_cls_options(self):
        options =  dict(
            subject_identifier = self.subject_identifier)
        return options
        
    @property
    def screening_options(self):
        options =  dict(
            subject_identifier = self.subject_identifier)
        return options
    
    
        
    