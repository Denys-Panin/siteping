from django.contrib import admin
from .models import MonitoredSite, SiteCheckLog


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="admin").exists()


class SiteCheckLogInline(admin.TabularInline):
    model = SiteCheckLog
    extra = 0
    fields = ("checked_at", "status_code", "response_time", "is_online")
    readonly_fields = fields
    ordering = ("-checked_at",)
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(MonitoredSite)
class MonitoredSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "user", "check_interval", "created_at")
    search_fields = ("name", "url", "user__username")
    list_filter = ("check_interval", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    inlines = [SiteCheckLogInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_admin(request.user):
            return qs
        return qs.filter(user=request.user)


@admin.register(SiteCheckLog)
class SiteCheckLogAdmin(admin.ModelAdmin):
    list_display = ("site", "checked_at", "status_code", "response_time", "is_online")
    search_fields = ("site__name",)
    list_filter = ("is_online", "status_code", "checked_at")
    ordering = ("-checked_at",)
    readonly_fields = ("site", "checked_at", "status_code", "response_time", "is_online")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_admin(request.user):
            return qs
        return qs.filter(site__user=request.user)
