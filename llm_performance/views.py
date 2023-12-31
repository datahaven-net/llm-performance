import logging

from django.views.generic import TemplateView

from django import shortcuts
from django.contrib import messages

from accounts.users import create_profile


def validate_profile_exists(dispatch_func):
    def dispatch_wrapper(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                create_profile(request.user, contact_email=request.user.email)
            if not request.user.profile.is_complete():
                messages.info(request, 'Please provide your username to start')
                return shortcuts.redirect('accounts_profile')
        return dispatch_func(self, request, *args, **kwargs)
    return dispatch_wrapper


logger = logging.getLogger(__name__)


class IndexPageView(TemplateView):
    template_name = 'base/index.html'

    @validate_profile_exists
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            pass
        return context
