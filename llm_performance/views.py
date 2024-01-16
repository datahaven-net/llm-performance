import logging

from django import shortcuts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

import django_tables2

from accounts.users import create_profile

from llm_performance.models import PerformanceSnapshot
from llm_performance.forms import ReportSendForm
from llm_performance import duration


logger = logging.getLogger(__name__)


def validate_profile_exists(dispatch_func):
    def dispatch_wrapper(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                create_profile(request.user, contact_email=request.user.email)
            if not request.user.profile.is_complete():
                messages.info(request, 'Please provide your user name to start.')
                return shortcuts.redirect('accounts_profile')
        return dispatch_func(self, request, *args, **kwargs)
    return dispatch_wrapper


class PerformanceSnapshotTable(django_tables2.Table):

    cpu = django_tables2.Column(verbose_name='CPU')
    cpu_cores = django_tables2.Column(verbose_name='cores')
    gpu = django_tables2.Column(verbose_name='GPU')
    ram = django_tables2.Column(verbose_name='RAM')
    vram = django_tables2.Column(verbose_name='VRAM')
    operating_system = django_tables2.Column(verbose_name='operating system')
    prompt_eval_rate = django_tables2.Column(verbose_name='prompt eval rate')
    eval_rate = django_tables2.Column(verbose_name='eval rate')
    llm_model = django_tables2.Column(verbose_name='model name')
    reporter = django_tables2.Column(verbose_name='reporter')

    class Meta:
        model = PerformanceSnapshot
        template_name = "table/bootstrap4-responsive.html"
        sequence = ('cpu', 'cpu_cores', 'gpu', 'ram', 'vram', 'operating_system',
                    'prompt_eval_rate', 'eval_rate', 'llm_model', 'reporter', )
        exclude = ('timestamp', 'input', 'cpu_brand', 'gpu_brand', 'purchase_year', 'purchase_price',
                   'total_duration', 'load_duration',
                   'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration',
                   'approved', 'id', )

    def render_ram(self, record):
        return record.ram_formatted

    def render_vram(self, record):
        return record.vram_formatted

    def render_reporter(self, record):
        return record.reporter_formatted


class IndexPageView(django_tables2.SingleTableView):
    template_name = 'report/list.html'
    table_class = PerformanceSnapshotTable

    @validate_profile_exists
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return PerformanceSnapshot.objects.filter(approved=True)


class ReportSendView(FormView):
    template_name = 'report/send.html'
    form_class = ReportSendForm
    success_url = reverse_lazy('index')

    @validate_profile_exists
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_report = PerformanceSnapshot.objects.filter(
            reporter=self.request.user,
            approved=True,
        ).last()
        if last_report:
            context['cpu_initial_value'] = last_report.cpu
            context['gpu_initial_value'] = last_report.gpu
        return context

    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['initial']['name'] = self.request.user.profile.person_name
        kwargs['initial']['email'] = self.request.user.email
        last_report = PerformanceSnapshot.objects.filter(
            reporter=self.request.user,
            approved=True,
        ).last()
        if last_report:
            kwargs['initial']['cpu_cores'] = last_report.cpu_cores
            kwargs['initial']['ram'] = last_report.ram
            kwargs['initial']['vram'] = last_report.vram
            kwargs['initial']['purchase_year'] = last_report.purchase_year
            kwargs['initial']['purchase_price'] = last_report.purchase_price
            kwargs['initial']['operating_system'] = last_report.operating_system
        return kwargs

    def form_valid(self, form):
        try:
            if not form.data['message'].count('--verbose'):
                form.add_error('message', 'To get detailed performance info you need to run ollama with "--verbose" flag.')
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
                form.add_error('cpu', 'CPU company brand was not detected, your input is not valid.')
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
                form.add_error('gpu', 'GPU company brand was not detected, your input is not valid.')
                return super(ReportSendView, self).form_invalid(form)

            if d['name'] != self.request.user.profile.person_name or d['email'] != self.request.user.email:
                form.add_error(None, 'You are not authorised!')
                return super(ReportSendView, self).form_invalid(form)

            PerformanceSnapshot.objects.create(
                input=form.cleaned_data['message'],
                cpu=form.cleaned_data['cpu'],
                cpu_brand=known_cpu_brand.upper(),
                cpu_cores=form.cleaned_data['cpu_cores'],
                ram=form.cleaned_data['ram'],
                gpu=form.cleaned_data['gpu'],
                gpu_brand=known_gpu_brand.upper(),
                vram=form.cleaned_data['vram'],
                purchase_year=form.cleaned_data['purchase_year'],
                purchase_price=form.cleaned_data['purchase_price'],
                operating_system=form.cleaned_data['operating_system'],
                total_duration=duration.from_str(m.group('total_duration')),
                load_duration=duration.from_str(m.group('load_duration')),
                prompt_eval_count=m.group('prompt_eval_count'),
                prompt_eval_duration=duration.from_str(m.group('prompt_eval_duration')),
                prompt_eval_rate=m.group('prompt_eval_rate'),
                eval_count=m.group('eval_count'),
                eval_duration=duration.from_str(m.group('eval_duration')),
                eval_rate=m.group('eval_rate'),
                llm_model=m.group('llm_model'),
                approved=self.request.user.trusted,
                reporter=self.request.user,
            )
        except Exception as err:
            logger.exception(err)
            form.add_error(None, 'Because of technical error your report was not submitted.')
            return super(ReportSendView, self).form_invalid(form)

        if self.request.user.trusted:
            messages.success(self.request, 'Report successfilly submitted. Thank you for cooperation.')
        else:
            messages.success(self.request, 'Report successfilly submitted. We will review your submission and soon update gathered statistics. Thank you for cooperation.')

        return super(ReportSendView, self).form_valid(form)


class ReportPrepareView(TemplateView):
    template_name = 'report/prepare.html'

    @validate_profile_exists
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
