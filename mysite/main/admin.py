from django.contrib import admin
from .models import table_a

# Register your models here.
class table_aAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date",{"fields":['title','date']}),
        ("content",{"fields":['message']})
    ]
admin.site.register(table_a,table_aAdmin)
