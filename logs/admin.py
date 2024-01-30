from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy

from logs.models import RequestLog, VisitorIP


class HasExceptionListFilter(admin.SimpleListFilter):

    title = gettext_lazy('have exception')
    parameter_name = 'has_exception'

    def lookups(self, request, model_admin):
        return (
            ('yes', gettext_lazy('Has exception')),
            ('no', gettext_lazy("Doesn't have exception")),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(exception__isnull=False)
        if self.value() == 'no':
            return queryset.filter(exception__isnull=True)


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip_address', 'user', 'method', 'path', 'status_code', 'duration', 'no_exception')
    list_filter = ('timestamp', 'ip_address', 'user', 'method', 'path', 'status_code', HasExceptionListFilter)
    search_fields = ('timestamp', 'ip_address', 'user', 'method', 'path', 'status_code', 'duration', 'exception')
    readonly_fields = ('timestamp', 'ip_address', 'user', 'method', 'path', 'status_code', 'duration', 'get_request', 'exception')
    exclude = ('request', )
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request, **kwargs):
        return False

    def no_exception(self, obj):
        return not bool(obj.exception)
    no_exception.boolean = True

    def get_request(self, instance):
        return format_html('<pre>{request}</pre>', request=instance.request)
    get_request.short_description = 'Request'


class IsVisitorIPBlockedFilter(admin.SimpleListFilter):

    title = gettext_lazy('is blocked')
    parameter_name = 'is_blocked'

    def lookups(self, request, model_admin):
        return (
            ('no', gettext_lazy("was not blocked")),
            ('yes', gettext_lazy('is blocked')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(blocked=True)
        if self.value() == 'no':
            return queryset.filter(blocked=False)


class VisitorIPAdmin(admin.ModelAdmin):
    list_display = ('first_seen', 'ip_address', 'counter', 'was_not_blocked', )
    list_filter = ('first_seen', IsVisitorIPBlockedFilter, )
    search_fields = ('first_seen', 'ip_address', )
    readonly_fields = ('first_seen', 'ip_address', 'counter', 'blocked', )
    date_hierarchy = 'first_seen'

    def has_add_permission(self, request, **kwargs):
        return False

    def was_not_blocked(self, obj):
        return not bool(obj.blocked)
    was_not_blocked.boolean = True


admin.site.register(RequestLog, RequestLogAdmin)
admin.site.register(VisitorIP, VisitorIPAdmin)
