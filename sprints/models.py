from django.db import models
from django.core.exceptions import ValidationError

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    goal = models.TextField(blank=True)

    def clean(self):
        # Ensure start_date <= end_date
        if self.planned_start_date > self.planned_end_date:
            raise ValidationError("Start date must be before or equal to end date.")

        # Check overlapping dates
        overlapping = Sprint.objects.filter(
            planned_start_date__lte=self.planned_end_date,
            planned_end_date__gte=self.planned_start_date
        ).exclude(id=self.id)
        if overlapping.exists():
            raise ValidationError("Sprint dates overlap with another existing sprint.")


    def save(self, *args, **kwargs):
        self.full_clean()

        # Automatically unset current from others
        if self.is_current:
            Sprint.objects.filter(is_current=True).exclude(id=self.id).update(is_current=False)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['planned_start_date']


    def __str__(self):
        return self.name