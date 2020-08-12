from django.contrib import admin
import common.models

# Register your models here.
admin.site.register(common.models.Song)
admin.site.register(common.models.Record)
admin.site.register(common.models.Author)
