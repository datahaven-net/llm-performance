from django.contrib import admin
from nested_admin import NestedModelAdmin  # @UnresolvedImport

from llm_performance.models import PerformanceSnapshot


class PerformanceSnapshotAdmin(NestedModelAdmin):
    list_display = (
        'timestamp', 'cpu_brand', 'ram', 'gpu_brand', 'vram', 'purchase_year', 'purchase_price',
        'total_duration', 'load_duration',
        'prompt_eval_count', 'prompt_eval_duration', 'prompt_eval_rate',
        'eval_count', 'eval_duration', 'eval_rate',
        'llm_model', 'reporter', 'approved',
    )


admin.site.register(PerformanceSnapshot, PerformanceSnapshotAdmin)
