from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

from nested_admin import NestedModelAdmin  # @UnresolvedImport

from accounts.models.account import Account
from accounts.models.activation import Activation
from accounts.models.notification import Notification
from accounts.models.profile import Profile


def trust_account(modeladmin, request, queryset):
    for inst in queryset:
        inst.trusted = True
        inst.save()
trust_account.short_description = 'Trust'


def discredit_account(modeladmin, request, queryset):
    for inst in queryset:
        inst.trusted = False
        inst.save()
discredit_account.short_description = 'Discredit'


class AccountAdmin(NestedModelAdmin):

    class Media:
        css = {
            'all': ('css/styles.css', )
        }

    list_display = ('email', 'profile_link', 'is_active', 'is_staff', 'notes', 'get_trust_discredit_links', )
    search_fields = ('email', )
    readonly_fields = ('email', )

    actions = [trust_account, discredit_account, ]

    def profile_link(self, account_instance):
        return mark_safe('<a href="{}?q={}">{}</a>'.format(
            reverse("admin:accounts_profile_changelist"), account_instance.email, account_instance.profile))
    profile_link.short_description = 'Profile'

    def get_model_info(self):
        return (self.model._meta.app_label, self.model._meta.model_name)

    def process_account_trusted(self, request, account_id, *args, **kwargs):
        inst = self.get_object(request, account_id)
        inst.trusted = True
        inst.save()
        url = reverse("admin:%s_%s_changelist" % self.get_model_info(), current_app=self.admin_site.name)
        return HttpResponseRedirect(url)

    def process_account_discredited(self, request, account_id, *args, **kwargs):
        inst = self.get_object(request, account_id)
        inst.trusted = False
        inst.save()
        url = reverse("admin:%s_%s_changelist" % self.get_model_info(), current_app=self.admin_site.name)
        return HttpResponseRedirect(url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:account_id>/trust/',
                self.admin_site.admin_view(self.process_account_trusted),
                name='account-trust',
            ),
            path(
                '<int:account_id>/discredit/',
                self.admin_site.admin_view(self.process_account_discredited),
                name='account-discredit',
            ),
        ]
        return custom_urls + urls

    def get_trust_discredit_links(self, instance):
        t = '<a href="{}" class="grp-button {}" style="opacity: {};">{}</a>'
        l = reverse('admin:account-discredit' if instance.trusted else 'admin:account-trust', args=[instance.pk])
        if instance.trusted:
            return format_html(t.format(l, 'grp-default', '.6', '&nbsp;&nbsp;&nbsp;trusted&nbsp;&nbsp;&nbsp;&nbsp;'))
        else:
            return format_html(t.format(l, 'grp-delete-link', '.9', 'discredited'))
    get_trust_discredit_links.short_description = 'trust'
    get_trust_discredit_links.allow_tags = True


class ActivationAdmin(NestedModelAdmin):
    list_display = ('account', 'code', 'created_at', )
    search_fields = ('account__email', )


class NotificationAdmin(NestedModelAdmin):
    list_display = ('account', 'recipient', 'subject', 'type', 'status', 'created_at',  )
    search_fields = ('account__email', 'recipient', )


class ProfileAdmin(NestedModelAdmin):
    list_display = ('account', 'person_name', 'contact_email', )
    search_fields = ('account__email', 'person_name', 'contact_email', )


admin.site.register(Account, AccountAdmin)
admin.site.register(Activation, ActivationAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Profile, ProfileAdmin)
