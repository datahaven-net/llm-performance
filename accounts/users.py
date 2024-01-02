import logging

from accounts.models import Account, Profile

logger = logging.getLogger(__name__)


def list_all_users_by_date(year, month=None):
    if year and month:
        return Account.users.filter(date_joined__year=year, date_joined__month=month)
    else:
        return Account.users.filter(date_joined__year=year)


def create_profile(existing_account, **kwargs):
    """
    Creates new Profile for given Account.
    """
    prof = Profile.profiles.create(account=existing_account, **kwargs)
    logger.info('profile created: %r', prof)
    return prof
