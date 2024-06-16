from django.contrib import admin
from .models import User, Invite, Team

admin.site.register(User)
admin.site.register(Invite)
admin.site.register(Team)
