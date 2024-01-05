import logging

from django import shortcuts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from accounts.users import create_profile

from llm_performance.models import PerformanceSnapshot
from llm_performance.forms import ReportSendForm
from llm_performance import duration


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


class ReportSendView(FormView):
    template_name = 'report/send.html'
    form_class = ReportSendForm
    success_url = reverse_lazy('index')

    @validate_profile_exists
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['initial']['name'] = self.request.user.profile.person_name
        kwargs['initial']['email'] = self.request.user.email
        return kwargs

    def form_valid(self, form):
        ret = form.fields['message']._get_regex().match(form.data['message'])
        try:
            PerformanceSnapshot.objects.create(
                input=form.cleaned_data['message'],
                cpu=form.cleaned_data['cpu'],
                gpu=form.cleaned_data['gpu'],
                total_duration=duration.from_str(ret.group('total_duration')),
                load_duration=duration.from_str(ret.group('load_duration')),
                prompt_eval_count=ret.group('prompt_eval_count'),
                prompt_eval_duration=duration.from_str(ret.group('prompt_eval_duration')),
                prompt_eval_rate=ret.group('prompt_eval_rate'),
                eval_count=ret.group('eval_count'),
                eval_duration=duration.from_str(ret.group('eval_duration')),
                eval_rate=ret.group('eval_rate'),
            )
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'Because of technical error your report was not submitted')
            return super(ReportSendView, self).form_valid(form)
        messages.success(self.request, 'LLM performance report successfilly sent, we will review your submission and soon update gathered statistics. Thank you for cooperation.')
        return super(ReportSendView, self).form_valid(form)
