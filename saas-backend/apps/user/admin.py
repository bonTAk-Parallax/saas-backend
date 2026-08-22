from django.contrib import admin
from apps.user.models.custom_user import User
from apps.user.models.user_profile import UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
