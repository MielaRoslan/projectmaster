from django.contrib import admin
from .models import SearchLog, APIKeys, Twitter
# Register your models here.

admin.site.register(SearchLog)
admin.site.register(APIKeys)
admin.site.register(Twitter)