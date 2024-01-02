import datetime
import logging

from django.conf import settings
from django.utils import timezone

from accounts.models.activation import Activation

logger = logging.getLogger(__name__)


def activations_cleanup():
    """
    If the activation_code is older than a certain time and the account is still inactive (no domain,
    balance or payment belongs to the account as well), removes the inactive account and the expired activation code.

    If the activation_code is older than a certain time but the account is still active, then removes
    only the activation code.
    """

    activation_code_expiry_time = timezone.now() - datetime.timedelta(
        minutes=settings.ACTIVATION_CODE_EXPIRING_MINUTE
    )
    expired_activation_code_objects = Activation.objects.filter(
        created_at__lte=activation_code_expiry_time
    )

    for activation_code in expired_activation_code_objects:
        account = activation_code.account
        if not account.is_active:
            if account.balance == 0 and len(account.domains.all()) == 0 and len(account.payments.all()) == 0:
                activation_code.account.delete()  # This will remove activation code as well.
                logger.info("inactive account removed: %r", account.email)
                continue
        activation_code.delete()
        logger.info("activation code removed: %r", activation_code.code)
