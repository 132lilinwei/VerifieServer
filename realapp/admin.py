from django.contrib import admin
from realapp.models import MyUser
# Register your models here.


class MyAdmin(admin.ModelAdmin):
    exclude = ('password',)

admin.site.register(MyUser,MyAdmin)