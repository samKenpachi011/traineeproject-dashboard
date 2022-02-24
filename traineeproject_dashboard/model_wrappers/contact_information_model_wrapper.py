from pyexpat import model
from django.conf import settings
from edc_model_wrapper import ModelWrapper


class ContactInformationModelWrapper(ModelWrapper):
   
   model = 'traineeproject_personalcontactinfo'
   querystring_attrs = ['subject_identifier'] 
   next_url_attrs = ['subject_identifier']
   next_url_name = settings.DASHBOARD_URL('subject_dashboard_url')
    