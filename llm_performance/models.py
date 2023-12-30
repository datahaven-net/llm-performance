from django.db import models

class PerformanceSnapshot(models.Model):

    input = models.TextField(
    )

    cpu = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None,
    )

    gpu = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default=None,
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
