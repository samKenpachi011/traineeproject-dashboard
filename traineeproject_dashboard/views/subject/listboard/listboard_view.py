import re
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView as BaseListBoardView
from traineeproject_dashboard.model_wrappers import SubjectConsentModelWrapper

from .filters import ListboardViewFilters
class ListboardView(NavbarViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
                    SearchFormViewMixin, BaseListBoardView):

    listboard_template = 'subject_listboard_template'
    listboard_url = 'subject_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "far fa-user-circle"
    model = 'traineeproject_subject.subjectconsent'
    model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'traineeproject_dashboard'
    navbar_selected_item = 'consented_subject'
    search_form_url = 'subject_listboard_url'
    listboard_view_filters = ListboardViewFilters()

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q