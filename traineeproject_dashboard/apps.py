from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'traineeproject_dashboard'
    admin_site_name = 'traineeproject_subject_admin'