from django.contrib import admin
from .models import  User,Portfolio
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.unregister(Group)

admin.site.site_header = "Inoa"
admin.site.site_title = "Administração"
admin.site.index_title = "Inoa"