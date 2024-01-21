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
        # Intel(R) Core(TM) i7-6500U CPU @ 2.50GHz
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
        db_index=True,
    )

    cpu_cores = models.IntegerField(
        # 12
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    ram = models.IntegerField(
        # 16 GB
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    gpu = models.CharField(
        # Intel Corporation Skylake GT2 [HD Graphics 520] (rev 07)
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
        db_index=True,
    )

    vram = models.IntegerField(
        # 4 GB
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    purchase_year = models.IntegerField(
        # 2020
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    purchase_price = models.IntegerField(
        # U.S. $ 1000 
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    operating_system = models.CharField(
        # Ubuntu 22.04.2 LTS
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

    llm_model = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    approved = models.BooleanField(
        default=False,
    )

    reporter = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='reports',
        db_index=True,
    )

    @property
    def ram_formatted(self):
        return '{} GB'.format(self.ram) if self.ram else ''

    @property
    def vram_formatted(self):
        return '{} GB'.format(self.vram) if self.vram else ''

    @property
    def reporter_formatted(self):
        return self.reporter.profile.person_name

    @property
    def report_id(self):
        return self.id


class SampleInput(models.Model):

    text = models.TextField(
        db_index=False,
    )

    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )


class FrequentlyAskedQuestion(models.Model):

    position = models.IntegerField(
        db_index=False,
        null=True,
        blank=True,
        default=None,
    )

    question = models.TextField(
        db_index=False,
    )

    answer = models.TextField(
        db_index=False,
    )

    def save(self, *args, **kwargs):
        if not self.position:
            self.position = FrequentlyAskedQuestion.objects.count() + 1
        return super(FrequentlyAskedQuestion, self).save(*args, **kwargs)
