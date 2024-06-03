from django.contrib import admin
from .models import Email
from .models import User
from .models import UserEmail

admin.site.register(Email)
admin.site.register(User)
admin.site.register(UserEmail)