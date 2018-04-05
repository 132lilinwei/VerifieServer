from django.contrib import admin
from realapp.models import MyUser
# Register your models here.
admin.site.register(MyUser)

class PostCodesAdmin(admin.ModelAdmin):
    exclude = ('pcname',)