from django.contrib import admin
from .models import File, AccessLog


@admin.register(File)
class FileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "file",
        "download_count",
        "uploaded_at",
    )

    list_filter = (
        "uploaded_at",
        "user",
    )

    search_fields = (
        "file",
        "user__username",
    )

    ordering = ("-uploaded_at",)


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):

    list_display = (
        "file",
        "accessed_by",
        "timestamp",
    )

    list_filter = (
        "timestamp",
        "accessed_by",
    )

    search_fields = (
        "file__file",
        "accessed_by__username",
    )