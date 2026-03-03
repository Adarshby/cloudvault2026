from django.contrib import admin
from .models import File, AccessLog

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'uploaded_at', 'download_count')
    readonly_fields = ('uploaded_at',)

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('file', 'accessed_by', 'timestamp')