from django.apps import AppConfig


class BaseFeatureAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_marketing_feature_app'
