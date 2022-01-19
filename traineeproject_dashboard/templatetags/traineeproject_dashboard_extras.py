from django import template
from django.conf import settings

# TODO: create templates tags for the dashboard_button + screening

register =  template.Library()

@register.inclusion_tag('traineeproject_dashboard/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    # set the url and return a dict
    subject_dashboard_url  = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    return dict(
        subject_dashboard_url = subject_dashboard_url,
        subject_identifier = model_wrapper.subject_identifier
    )
