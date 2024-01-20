from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

from nested_admin import NestedModelAdmin  # @UnresolvedImport

from llm_performance.models import FrequentlyAskedQuestion, PerformanceSnapshot, SampleInput


def approve_snapshot(modeladmin, request, queryset):
    for inst in queryset:
        inst.approved = True
        inst.save()
approve_snapshot.short_description = 'Approve'


def reject_snapshot(modeladmin, request, queryset):
    for inst in queryset:
        inst.approved = False
        inst.save()
reject_snapshot.short_description = 'Reject'


class PerformanceSnapshotAdmin(NestedModelAdmin):

    class Media:
        css = {
            'all': ('css/styles.css', )
        }

    fields = (
        ('get_reporter_link', ),
        ('approved', ),
        ('cpu', ),
        ('gpu', ),
        ('ram', 'vram', ),
        ('operating_system', 'purchase_year', 'purchase_price', ),
        ('total_duration', 'load_duration', ),
        ('prompt_eval_count', 'prompt_eval_duration', 'prompt_eval_rate', ),
        ('eval_count', 'eval_duration', 'eval_rate', ),
        ('llm_model', ),
        ('input', ),
    )

    list_display = (
        'timestamp', 'cpu_brand', 'ram', 'gpu_brand', 'vram',
        'operating_system', 'purchase_year', 'purchase_price',
        'total_duration', 'load_duration',
        'prompt_eval_count', 'prompt_eval_duration', 'prompt_eval_rate',
        'eval_count', 'eval_duration', 'eval_rate',
        'llm_model', 'get_reporter_link', 'get_approve_reject_links',
    )

    readonly_fields = ('get_reporter_link', 'input', 'get_approve_reject_links', )

    search_fields = ('reporter__email', 'reporter__person_name', 'cpu', 'gpu', )

    actions = [approve_snapshot, reject_snapshot, ]

    def get_reporter_link(self, instance):
        link = '{}?q={}'.format(reverse("admin:accounts_account_changelist"), instance.reporter.email)
        return mark_safe(f'<a href="{link}">{instance.reporter.profile.person_name}</a>')
    get_reporter_link.short_description = 'Reporter'

    def get_model_info(self):
        return (self.model._meta.app_label, self.model._meta.model_name)

    def process_approve(self, request, snapshot_id, *args, **kwargs):
        inst = self.get_object(request, snapshot_id)
        inst.approved = True
        inst.save()
        url = reverse("admin:%s_%s_changelist" % self.get_model_info(), current_app=self.admin_site.name)
        return HttpResponseRedirect(url)

    def process_reject(self, request, snapshot_id, *args, **kwargs):
        inst = self.get_object(request, snapshot_id)
        inst.approved = False
        inst.save()
        url = reverse("admin:%s_%s_changelist" % self.get_model_info(), current_app=self.admin_site.name)
        return HttpResponseRedirect(url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:snapshot_id>/approve/',
                self.admin_site.admin_view(self.process_approve),
                name='snapshot-approve',
            ),
            path(
                '<int:snapshot_id>/reject/',
                self.admin_site.admin_view(self.process_reject),
                name='snapshot-reject',
            ),
        ]
        return custom_urls + urls

    def get_approve_reject_links(self, instance):
        t = '<a href="{}" class="grp-button {}" style="opacity: {};">{}</a>'
        l = reverse('admin:snapshot-reject' if instance.approved else 'admin:snapshot-approve', args=[instance.pk])
        if instance.approved:
            return format_html(t.format(l, 'grp-default', '.6', 'approved'))
        else:
            return format_html(t.format(l, 'grp-delete-link', '.9', '&nbsp;rejected&nbsp;'))
    get_approve_reject_links.short_description = 'state'
    get_approve_reject_links.allow_tags = True


class SampleInputAdmin(NestedModelAdmin):

    list_display = ('name', )


class FrequentlyAskedQuestionAdmin(NestedModelAdmin):

    list_display = ('position', 'question', )


admin.site.register(PerformanceSnapshot, PerformanceSnapshotAdmin)
admin.site.register(SampleInput, SampleInputAdmin)
admin.site.register(FrequentlyAskedQuestion, FrequentlyAskedQuestionAdmin)
