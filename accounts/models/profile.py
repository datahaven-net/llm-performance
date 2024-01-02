from django.core.validators import validate_email
from django.db import models

from accounts.models.account import Account


class Profile(models.Model):

    profiles = models.Manager()

    class Meta:
        app_label = 'accounts'
        base_manager_name = 'profiles'
        default_manager_name = 'profiles'

    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')

    person_name = models.CharField(max_length=255, verbose_name='user name')

    contact_email = models.CharField(validators=[validate_email], max_length=255, verbose_name='e-mail')

    email_notifications_enabled = models.BooleanField(
        verbose_name='e-mail notifications',
        help_text='enable e-mail notifications',
        default=True,
    )

    def __str__(self):
        return 'profile({}:{})'.format(self.person_name, self.contact_email)

    def __repr__(self):
        return 'profile({}:{})'.format(self.person_name, self.contact_email)

    def is_complete(self):
        # TODO: extra regex validators to be added later
        if not self.person_name:
            return False
        if not self.contact_email:
            return False
        return True
