import logging

from django import shortcuts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
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


class IndexPageView(ListView):
    template_name = 'report/list.html'
    paginate_by = 25

    @validate_profile_exists
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return PerformanceSnapshot.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated:
    #         pass
    #     return context


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
        try:
            if not form.data['message'].count('--verbose'):
                form.add_error('message', 'to get detailed performance info you need to run ollama with "--verbose" flag')
                return super(ReportSendView, self).form_invalid(form)

            m = form.fields['message']._get_regex().match(form.data['message'])
            d = form.cleaned_data

            known_cpu_brand = None
            for cpu_brand in (
                'intel',
                'amd',
                'qualcomm',
                'arm',
                'mips',
            ):
                known_cpu_brand = cpu_brand if cpu_brand in d['cpu'].lower() else known_cpu_brand
            if not known_cpu_brand and d['cpu']:
                form.add_error('cpu', 'CPU company brand was not detected, your input is not valid')
                return super(ReportSendView, self).form_invalid(form)

            known_gpu_brand = None
            for gpu_brand in (
                'intel',
                'geforce',
                'nvidia',
                'gigabyte',
                'asus',
                'msi',
                'xfx',
                'sapphire',
                'amd',
                'powercolor',
                'evga',
                'kfa',
                'zotac',
                'hp ',
                'palit',
                'pny ',
                'dell',
                'asrock',
                'gainward',
                'inno',
            ):
                known_gpu_brand = gpu_brand if gpu_brand in d['gpu'].lower() else known_gpu_brand
            if not known_gpu_brand and d['gpu']:
                form.add_error('gpu', 'GPU company brand was not detected, your input is not valid')
                return super(ReportSendView, self).form_invalid(form)

            if d['name'] != self.request.user.profile.person_name or d['email'] != self.request.user.email:
                form.add_error(None, 'Not authorised')
                return super(ReportSendView, self).form_invalid(form)

            PerformanceSnapshot.objects.create(
                input=form.cleaned_data['message'],
                cpu=form.cleaned_data['cpu'],
                cpu_brand=known_cpu_brand.upper(),
                ram=form.cleaned_data['ram'],
                gpu=form.cleaned_data['gpu'],
                gpu_brand=known_gpu_brand.upper(),
                vram=form.cleaned_data['vram'],
                total_duration=duration.from_str(m.group('total_duration')),
                load_duration=duration.from_str(m.group('load_duration')),
                prompt_eval_count=m.group('prompt_eval_count'),
                prompt_eval_duration=duration.from_str(m.group('prompt_eval_duration')),
                prompt_eval_rate=m.group('prompt_eval_rate'),
                eval_count=m.group('eval_count'),
                eval_duration=duration.from_str(m.group('eval_duration')),
                eval_rate=m.group('eval_rate'),
                llm_model=m.group('llm_model'),
                reporter=self.request.user,
            )
        except Exception as err:
            logger.exception(err)
            form.add_error(None, 'Because of technical error your report was not submitted')
            return super(ReportSendView, self).form_invalid(form)

        messages.success(self.request, 'LLM performance report successfilly sent, we will review your submission and soon update gathered statistics. Thank you for cooperation.')
        return super(ReportSendView, self).form_valid(form)
