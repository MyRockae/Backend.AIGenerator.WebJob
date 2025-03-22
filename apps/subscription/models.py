from django.db import models
from apps.account.models import User
from django.utils.timezone import now, timedelta


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'SubscriptionPlan'
        verbose_name = 'SubscriptionPlan'
        verbose_name_plural = 'SubscriptionPlans'
    

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One user has one subscription
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def is_active(self):
        """Check if the subscription is still valid."""
        return self.end_date and self.end_date > now()

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'}"

    def save(self, *args, **kwargs):
        """Ensure end_date is set correctly based on the plan duration."""
        if self.plan and not self.end_date:
            self.end_date = now() + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'UserSubscription'
        verbose_name = 'UserSubscription'
        verbose_name_plural = 'UserSubscriptions'