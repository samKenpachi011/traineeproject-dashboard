from django.conf import settings
from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper

class SubjectVisitModelWrapper():
    
    model = 'traineeproject_subject.subjecvisit'
    next_url_name = settings.DASHBOARD_URL_NAME.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier','appointment']
    