from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from nested_admin import NestedModelAdmin  # @UnresolvedImport

from accounts.models.account import Account
from accounts.models.activation import Activation
from accounts.models.notification import Notification
from accounts.models.profile import Profile


class AccountAdmin(NestedModelAdmin):

    list_display = ('email', 'profile_link', 'is_active', 'is_staff', 'notes', )
    search_fields = ('email', )
    readonly_fields = ('email', )

    def profile_link(self, account_instance):
        return mark_safe('<a href="{}?q={}">{}</a>'.format(
            reverse("admin:accounts_profile_changelist"), account_instance.email, account_instance.profile))
    profile_link.short_description = 'Profile'


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
