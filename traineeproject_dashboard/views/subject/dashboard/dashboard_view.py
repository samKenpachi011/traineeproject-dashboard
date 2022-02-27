
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
                                SubjectOffStudyModelWrapper)
class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView):
    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'traineeproject_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    subject_locator_model = 'traineeproject_subject.subjectpersonalcontactinfo'
    subject_locator_model_wrapper_cls = ContactInformationModelWrapper
    navbar_name = 'traineeproject_dashboard'
    navbar_selected_item = 'consented_subject'
    
    @property
    def subject_offstudy_wrapper(self):
        # create an instance of the subject offstudy if the offstudy is filled
        
        subject_offstudy_cls = django_apps.get_models('traineeproject_prn.subjectoffstudy')
        try:
            subject_offstudy_obj = subject_offstudy_cls.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            subject_offstudy_wrapper = SubjectOffStudyModelWrapper(model_obj=subject_offstudy_obj)
        return subject_offstudy_wrapper
    
    @property
    def appointment(self):
        # returns a queryset of all appointments for this subject
        if not self._appointments:
            self._appointments =  self.appointment_model_cls.filter(
                subject_identifier=self.subject_identifier).order_by('visit_code')
        return self._appointments
    
    
    def get_onschedule_model_obj(self, schedule):
        # returns an onschedule instance
        try:
            return schedule.onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                schedule=schedule.name)
        except ObjectDoesNotExist:
            return None    
    
    def get_locator_info(self):
        # return an instance of the subjects contact info
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = self.subject_locator_model_cls.objects.get(
                subject_identifier = subject_identifier)
        except ObjectDoesNotExist:
            return None   
        return obj
    
    def set_current_schedule(self, onschedule_model_obj=None,
                             schedule=None, visit_schedule=None,
                             is_onschedule=True):
        
        if onschedule_model_obj:
            if is_onschedule:
                self.current_schedule = schedule
                self.current_visit_schedule = visit_schedule
                self.current_onschedule_model = onschedule_model_obj
                self.onschedule_models.append(onschedule_model_obj)
                self.visit_schedules.update({visit_schedule.name: visit_schedule})
    
    def main_schedule_enrollment(self):
        # checks the screening eligibility if the subject_identifier is eligible 
        # after check is sent data to the put_on_schedule funtion
        cohort = 'traineeproject_main'
        onschedule_model = 'traineeproject_subject.onschedule'
        try:
            screening_eligibility = ScreeningEligibility.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            if screening_eligibility.is_eligible:
                # put onschedule
                self.put_on_schedule(f'{cohort}_enrol_schedule',
                                     onschedule_model=onschedule_model,
                                     onschedule_datatime=screening_eligibility.created.replace(microsecond=0))
                self.put_on_schedule(f'{cohort}_fu_schedule',
                                     onschedule_model=onschedule_model,
                                     onschedule_datatime=screening_eligibility.created.replace(microsecond=0))
                
    
    def sub_cohort_enrollment(self):
        # check if the subcohort is full then put the subject onschedule
        cohort = 'traineeproject_sub'
        if not self.is_subcohort_full():
            onschedule_model = 'traineeproject_subject.onschedule'
            try:
                screening_eligibility = ScreeningEligibility.objects.get(
                    subject_identifier = self.subject_identifier)
            except ObjectDoesNotExist:
                pass
            else:    
                if screening_eligibility.is_eligible:
                    self.put_on_schedule(f'{cohort}_enrol_schedule',
                                     onschedule_model=onschedule_model,
                                     onschedule_datatime=screening_eligibility.created.replace(microsecond=0))
                    self.put_on_schedule(f'{cohort}_fu_schedule',
                                     onschedule_model=onschedule_model,
                                     onschedule_datatime=screening_eligibility.created.replace(microsecond=0))
                    
    
    def put_on_schedule(self, schedule_name, onschedule_model, onschedule_datatime=None):
        # uses site_visit_schedules to get the on schedule model schedule name
        # takes the schedule name,onschedule_model,onschedule_datetime
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name
        )
        schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datatime,
            schedule_name=schedule_name)
        
    
    def is_subcohort_full(self):
        onschedule_subcohort = OnSchedule.objects.filter(
            schedule_name='traineeproject_sub_enrol_schedule'
        )
        
        return onschedule_subcohort.count() == 3000
    
    def get(self,request, *args, **kwargs):
        # redirect base on the enrollment request.path
        context = self.get_context_data(self, **kwargs)
        if 'main_schedule_enrollment' in self.request.path:
            url = self.request.path.split('main_schedule_enrollment')[0]
            return redirect(url)
        elif 'sub_cohort_enrollment' in self.request.path:
            url = self.request.path.split('sub_cohort_enrollment')[0]
            return redirect(url)
        else:
            return self.render_to_response(context)
           
        
         
    def has_schedules(self):
        # return the count for onschedule objects for the subject identifier
        onschedule = OnSchedule.objects.filter(
            subject_identifier = self.subject_identifier
        )   
        return onschedule.count() > 0
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        locator_obj = self.get_locator_info()
        # check for enrollment
        if 'main_schedule_enrollment' in self.request.path:
            self.main_schedule_enrollment()

        if 'sub_cohort_enrollment' in self.request.path:
            self.sub_cohort_enrollment()
             
        context.update(
            locator_obj = locator_obj,
            subject_consent = self.consent_wrapped,
            schedule_names = [model.schedule_name for model in self.onschedule_models],
            is_subcort_full = self.is_subcohort_full(),
            has_schedules = self.has_schedules(),
            subject_offstudy = self.subject_offstudy_wrapper)
        return context