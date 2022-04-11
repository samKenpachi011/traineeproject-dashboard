
from django.apps import apps as django_apps
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from traineeproject_subject.models import ScreeningEligibility, screening_eligibility
from edc_base.view_mixins import EdcBaseViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin
from edc_navbar import NavbarViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from traineeproject_subject.models.onschedule import OnSchedule
from ....model_wrappers import (SubjectConsentModelWrapper, 
                                ContactInformationModelWrapper,
                                AppointmentModelWrapper,
                                SubjectVisitModelWrapper,
                                SubjectOffStudyModelWrapper)
from edc_model_wrapper import ModelWrapper

class ActionItemModelWrapper(ModelWrapper):

    model = 'edc_action_item.actionitem'
    next_url_attrs = ['subject_identifier', 'ae_initial']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView):
    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'traineeproject_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    subject_locator_model = 'traineeproject_subject.personalcontactinfo'
    special_forms_include_value = 'traineeproject_dashboard/subject/dashboard/special_forms.html'
    subject_locator_model_wrapper_cls = ContactInformationModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper
    navbar_name = 'traineeproject_dashboard'
    navbar_selected_item = 'consented_subject'
    onschedule_model_cls = 'traineeproject_subject.onschedule'
    
    @property
    def appointments(self):
        if not self._appointments:
            self._appointments = self.appointment_model_cls.objects.filter(
                subject_identifier=self.subject_identifier).order_by(
                    'visit_code')
        return self._appointments
    
    # @property
    # def onschedule_model_obj(self):
    #     return django_apps.get_model(self.onschedule_model_cls)
    
    # def get_onschedule_model_obj(self, schedule):
    #     onschedule_model = self.onschedule_model_obj
    #     try:
    #         onschedule_model.objects.get(
    #             subject_identifier=self.subject_identifier,
    #             schedule_name=schedule.name)
    #     except ObjectDoesNotExist:
    #         return None 
    #     else:
    #         return onschedule_model   
    
    def get_onschedule_model_obj(self, schedule):
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule_name=schedule.name)
        except ObjectDoesNotExist:
            return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        locator_obj = self.get_locator_info()
        
        context.update(
            locator_obj=locator_obj,
            subject_consent=self.consent_wrapped,
            schedule_names=[model.schedule_name for model in self.onschedule_models]
            )
        return context

    def get_locator_info(self):

        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        return obj
                
    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
        
    #     locator_obj = self.get_locator_info()
    #     context.update(
    #         locator_obj = locator_obj,
    #         subject_consent = self.consent_wrapped,
    #         schedule_names = [model.schedule_name for model in self.onschedule_models])
        
    #     return context  
    
    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):
        if onschedule_model_obj:
            if is_onschedule:
                self.current_schedule = schedule
                self.current_visit_schedule = visit_schedule
                self.current_onschedule_model = onschedule_model_obj
                self.onschedule_models.append(onschedule_model_obj)
            self.visit_schedules.update(
                {visit_schedule.name: visit_schedule})        

 