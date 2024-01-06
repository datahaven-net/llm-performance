from django.db import models

from accounts.models import Account


class PerformanceSnapshot(models.Model):

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    input = models.TextField(
        # user@localhost:~$ ollama run llama2 --verbose ...
        db_index=False,
    )

    cpu = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None,
    )

    cpu_brand = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=None,
    )

    ram = models.IntegerField(
        # 16 GB
        null=True,
        blank=True,
        default=None,
        db_index=False,
    )

    gpu = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None,
    )

    gpu_brand = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=None,
    )

    vram = models.IntegerField(
        # 4 GB
        null=True,
        blank=True,
        default=None,
        db_index=False,
    )

    total_duration = models.FloatField(
        # 5m19.747896821s
    )

    load_duration = models.FloatField(
        # 18.043861292s
    )

    prompt_eval_count = models.IntegerField(
        # 27 token(s)
    )

    prompt_eval_duration = models.FloatField(
        # 14.908207s
    )

    prompt_eval_rate = models.FloatField(
        # 1.81 tokens/s
    )

    eval_count = models.IntegerField(
        # 428 token(s)
    )

    eval_duration = models.FloatField(
        # 4m46.792663s
    )

    eval_rate = models.FloatField(
        # 1.49 tokens/s
    )

    llm_model = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        default=None,
    )

    approved = models.BooleanField(
        default=False,
    )

    reporter = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='reports',
    )
