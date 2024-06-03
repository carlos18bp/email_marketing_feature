from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from email_marketing_feature_app.views import email, user, user_email

urlpatterns = [
    # Email related endpoints
    path('emails/', email.email_list_create, name='email_list_create'),
    path('emails/update/<int:id>/', email.email_update, name='email_update'),
    path('emails/delete/<int:id>/', email.email_delete, name='email_delete'),
    path('send_email_to_users/', email.send_email_to_users, name='send_email_to_users'),
    path('schedule_email/', email.schedule_email, name='schedule_email'),
    
    # User related endpoints
    path('users/', user.user_list, name='user_list'),
    
    # UserEmail related endpoints
    path('users_emails/', user_email.users_emails_list, name='users_emails_list'),
    path('delete_scheduled_email/<int:id>/', user_email.delete_scheduled_email, name='delete_scheduled_email'),
]

# Serve static and media files in development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
